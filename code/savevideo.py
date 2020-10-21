import cv2

video = cv2.VideoCapture(0)
if (video.isOpened() == False):
    print("Error reading video file")
frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
result = cv2.VideoWriter('filename.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)
doTheNeedful = True
try:
    while(True):
        ret, frame = video.read()
        doTheNeedful = ret
        if doTheNeedful == True:
            result.write(frame)
        else:
            break
except KeyboardInterrupt:
    pass
video.release()
result.release()
print("The video was successfully saved")

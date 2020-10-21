import cv2
import time

snapshot_interval = 1 #seconds
snapshot_sequence = 1 #increment and use on filename
video_cap = cv2.VideoCapture(0)
if (video_cap.isOpened() == False):
    print("Error opening video stream")
frame_width = int(video_cap.get(3))
frame_height = int(video_cap.get(4))
size = (frame_width, frame_height)
video_out = cv2.VideoWriter('../video/filename.mp4',
                         cv2.VideoWriter_fourcc(*'mp4v'),
                         29.97, size)
do_continue = True
current_time = time.time()
#last_snapshot_time = time.time()
next_snapshot_time = current_time + snapshot_interval
try:
    while(True):
        ret, frame = video_cap.read()
        do_continue = ret
        if do_continue == True:
            current_time = time.time()
            if current_time >= next_snapshot_time:
                next_snapshot_time = current_time + snapshot_interval
                #print("taking snapshot")
                cv2.imwrite('../snapshot/snapshot_' + str(snapshot_sequence) + '.png', frame)
                snapshot_sequence += 1
            video_out.write(frame)
        else:
            break
except KeyboardInterrupt:
    pass
video_cap.release()
video_out.release()
print("Video was saved")

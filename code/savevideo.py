import cv2
import time
import numpy as np

snapshot_interval = 1 #seconds
snapshot_sequence = 1 #increment and use on filename
do_snapshot = False

frame_count = 0

font = cv2.FONT_HERSHEY_PLAIN
text_position = (0,10)
font_scale = 0.8
font_color = (0,0,0)
line_type = 1

video_cap = cv2.VideoCapture(0)
if (video_cap.isOpened() == False):
    print("Error opening video stream")
frame_width = int(video_cap.get(3))
frame_height = int(video_cap.get(4))

#info bar rectangle
x, y, w, h = 0, 0, frame_width, 14
delimiter = '|'

can_data = { 'datetime': '10/25/2020 13:24:22',
             'direction': 'NW',
             'temp': '104F',
             'lat_long': '(38.626550, -90.189260)',
             'mph': '68MPH',
             'g': '0.32 G',
             'id': '104:325239'
           }

placeholder_text = can_data['datetime'] +\
                   delimiter +\
                   can_data['direction'] +\
                   delimiter +\
                   can_data['temp'] +\
                   delimiter +\
                   can_data['lat_long'] +\
                   delimiter +\
                   can_data['mph'] +\
                   delimiter +\
                   can_data['g'] +\
                   delimiter +\
                   can_data['id'] +\
                   delimiter

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
        frame_count += 1

        # put semi-transparent box on top of frame
        sub_img = frame[y:y+h, x:x+w]
        white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
        res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)
        frame[y:y+h, x:x+w] = res

        cv2.putText(frame, placeholder_text + str(frame_count),
            text_position,
            font,
            font_scale,
            font_color,
            line_type)

        do_continue = ret
        if do_continue == True:
            if do_snapshot == True:
                current_time = time.time()
                if current_time >= next_snapshot_time:
                    next_snapshot_time = current_time + snapshot_interval
                    cv2.imwrite('../snapshot/snapshot_' + str(snapshot_sequence) + '.jpg', frame)
                    snapshot_sequence += 1
            video_out.write(frame)
        else:
            break
except KeyboardInterrupt:
    pass
video_cap.release()
video_out.release()
print("Video was saved")

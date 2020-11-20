import sqlite3
import sys
import RPi.GPIO as GPIO
import os
from datetime import datetime
from multiprocessing import Process, Value
import cv2
import time
import numpy as np
import threading
import faulthandler; faulthandler.enable()

#power_on = 1
power_on = True
session_id = 0
debug = True
front_camera_index = -1
rear_camera_index = -1
conn_string = '../db/AutoCAN.db'

def create_video(camera_index, session_id, conn_string):
    conn = sqlite3.connect(conn_string)
    with conn:
        session_active = 1
        frames_per_video = 1000
        next_frame_cut = frames_per_video
        frame_count = 0                     #actual frames being written
        loop_count = 0                      #iterations through the while loop

        do_snapshot = False                 #whether or not to take periodic jpg stills in addition to video
        snapshot_interval = 0.25            #seconds
        snapshot_sequence = 1               #increment and use on filename

        do_video = False

        font = cv2.FONT_HERSHEY_PLAIN
        text_position = (0,10)
        font_scale = 0.8
        font_color = (0,0,0)
        line_type = 1

        video_cap = cv2.VideoCapture(camera_index)
        if (video_cap.isOpened() == False):
            print("Error opening video stream")
        frame_width = int(video_cap.get(3))
        frame_height = int(video_cap.get(4))
        frame_rate = (float(video_cap.get(5))) / 3.0

        #print("LIST PROPS================")
        #for x in range(21):
        #    print(str(video_cap.get(x)))
        #
        #print("END PROPS=================")

        #info bar rectangle
        x, y, w, h = 0, 0, frame_width, 14
        delimiter = '|'

        can_data = { 'datetime': '10/25/2020 13:24:22',
                    'direction': 'NW',
                    'temp': '104F',
                    'lat_long': '(38.626550, -90.189260)',
                    'mph': '68MPH',
                    'g': '0.32 G',
                    'session': '',
                    'datarow': '',
                    'frame': '',
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
        #video_out = cv2.VideoWriter('../video/' + str(session_id) + '_camera_' + str(camera_index) + '.avi', cv2.VideoWriter_fourcc(*'YUYV'), frame_rate, size)
        if do_video:
            video_out = cv2.VideoWriter('../video/' + str(session_id) + '-camera' + str(camera_index) + '-' + str(next_frame_cut) + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, size)
        do_continue = True
        current_time = time.time()
        next_snapshot_time = current_time + snapshot_interval

        c = conn.cursor()
        while(session_active):
            c.execute("SELECT COUNT(*) FROM session WHERE session_id = ? AND sys_session_end IS NULL AND gps_session_end IS NULL", (session_id,))
            result = c.fetchone()
            session_active = result[0]
            if session_active:
                loop_count += 1
                if loop_count % 7 == 0:
                    pass
                ret, frame = video_cap.read()
                #print(str(ret))
                #frame_count += 1

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
                            cv2.imwrite('../snapshot/' + str(session_id) + '-camera' + str(camera_index) + "-" + str(snapshot_sequence) + '.jpg', frame)
                            snapshot_sequence += 1
                    if loop_count % 3 == 0:
                        frame_count += 1
                        if do_video:
                            video_out.write(frame)
                else:
                    break
                
                if frame_count >= next_frame_cut:
                    next_frame_cut = next_frame_cut + frames_per_video
                    if do_video:
                        video_out = cv2.VideoWriter('../video/' + str(session_id) + '-camera' + str(camera_index) + '-' + str(next_frame_cut) + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, size)


        video_cap.release()
        video_out.release()
        print("finishing up on camera " + str(camera_index))

def create_session(conn_string):
    conn = sqlite3.connect(conn_string)
    with conn:
        c = conn.cursor()
        c.execute("INSERT INTO session (sys_session_start) VALUES (?)", (datetime.now(),))
        conn.commit()
        return c.lastrowid

def end_session(conn_string):
    if debug:
        print("Ending Session " + str(session_id))
    conn = sqlite3.connect(conn_string)
    with conn:
        c = conn.cursor()
        c.execute("UPDATE session SET sys_session_end = ? where session_id = ?",  (datetime.now(), session_id))
        conn.commit()

def fetch_can_data():
    print("fetch_can_data() not implemented")

def main():
    global front_camera_index
    global rear_camera_index
    global power_on
    global conn_string
    global session_id

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)

    if len(sys.argv) > 1:
        front_camera_index = int(sys.argv[1])
    if len(sys.argv) > 2:
        rear_camera_index = int(sys.argv[2])

    if debug:
        print("Script updated " + str(time.ctime(os.path.getmtime('AutoCAN.py'))))
        print("Front camera index: " + str(front_camera_index))
        print("Rear camera index: " + str(rear_camera_index))

    
    session_id = create_session(conn_string)
    if debug:
        print("Session ID " + str(session_id))

    jobs = []

    if int(front_camera_index) > -1:
        front_video = Process(target=create_video, args=(front_camera_index,session_id,conn_string))
        jobs.append(front_video)
        front_video.start()

    if int(rear_camera_index) > -1:
        rear_video = Process(target=create_video, args=(rear_camera_index,session_id,conn_string))
        jobs.append(rear_video)
        rear_video.start()

    while power_on:
        try:
            power_on = not GPIO.input(17)
        except KeyboardInterrupt:
            if debug:
                print("")
                print("Goodbye")
            end_session(conn_string)
            sys.exit()

    end_session(conn_string)

    #if internet
        #upload files and delete
    #else
        #save to subfolder

    time.sleep(5)
    power_on = not GPIO.input(17)
    if power_on:
        main()
    else:
        if debug:
            print("Goodnight")
        os.system("sudo shutdown -h now")  

if __name__ == "__main__":
    main()


import sqlite3
import sys
import RPi.GPIO as GPIO
import os
from datetime import datetime
from multiprocessing import Process, Value
import cv2
import time
import numpy as np

#power_on = 1
power_on = True
session_id = 0
debug = True
front_camera_index = -1
rear_camera_index = -1
conn = None

def create_video(camera_index, session_id, conn):
    session_active = 1
    print("creating video - placeholder")
    c = conn.cursor()
    while(session_active):
        #AND (sys_session_end IS NOT NULL OR gps_session_end IS NOT NULL)
        c.execute("SELECT COUNT(*) FROM session WHERE session_id = ? AND sys_session_end IS NULL AND gps_session_end IS NULL", (session_id,))
        result = c.fetchone()
        session_active = result[0]
        print("camera " + str(camera_index) + " sees status of " + str(session_active))
    print("finishing up on camera " + str(camera_index))

def create_session():
    c = conn.cursor()
    c.execute("INSERT INTO session (sys_session_start) VALUES (?)", (datetime.now(),))
    conn.commit()
    return c.lastrowid

def end_session():
    if debug:
        print("Ending Session " + str(session_id))
    c = conn.cursor()
    c.execute("UPDATE session SET sys_session_end = ? where session_id = ?",  (datetime.now(), session_id))
    conn.commit()

def fetch_can_data():
    print("fetch_can_data() not implemented")

def main():
    global front_camera_index
    global rear_camera_index
    global power_on
    global conn
    global session_id

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)

    if len(sys.argv) > 1:
        front_camera_index = sys.argv[1]
        pass
    if len(sys.argv) > 2:
        rear_camera_index = sys.argv[2]

    if debug:
        print("Front camera index: " + str(front_camera_index))
        print("Rear camera index: " + str(rear_camera_index))

    conn = sqlite3.connect('../db/AutoCAN.db')
    session_id = create_session()
    if debug:
        print("Session ID " + str(session_id))


    jobs = []
    front_video = Process(target=create_video, args=(front_camera_index,session_id,conn))
    rear_video = Process(target=create_video, args=(rear_camera_index,session_id,conn))
    jobs.append(front_video)
    jobs.append(rear_video)
    front_video.start()
    rear_video.start()

    while power_on:
        try:
            power_on = not GPIO.input(17)
        except KeyboardInterrupt:
            if debug:
                print("")
                end_session()
                print("Goodbye")
            sys.exit()

    end_session()
    conn.close()



    time.sleep(5)
    power_on = not GPIO.input(17)
    if power_on:
        main()
    else:
        if debug:
            print("Goodnight")
        #os.system("sudo shutdown -h now")  

    #if internet
        #upload files and delete
    #else
        #save to subfolder


if __name__ == "__main__":
    main()


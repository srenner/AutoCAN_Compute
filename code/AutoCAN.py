import sqlite3
import sys
import RPi.GPIO as GPIO
import os
from datetime import datetime

power_on = True
session_id = 0
debug = True
front_camera_index = -1
rear_camera_index = -1
connection = None

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

    while power_on:
        try:
            power_on = not GPIO.input(17)
        except KeyboardInterrupt:
            if debug:
                print("")
                end_session()
                print("Goodbye")
            sys.exit()
    
    if debug:
        print("Goodnight")
    end_session()
    conn.close()

    #if online
        #upload files and delete
    #else
        #save to subfolder

    os.system("sudo shutdown -h now")  

if __name__ == "__main__":
    main()

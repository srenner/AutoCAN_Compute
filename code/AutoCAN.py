import sqlite3
import sys
import RPi.GPIO as GPIO

power_on = True
session_id = 0
debug = True
front_camera_index = -1
rear_camera_index = -1

def create_session(conn):
    c = conn.cursor()
    c.execute("INSERT INTO session DEFAULT VALUES")
    conn.commit()
    return c.lastrowid

def end_session():
    pass

def fetch_can_data():
    print("fetch_can_data() not implemented")

def main():
    global front_camera_index
    global rear_camera_index
    global power_on

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
    session_id = create_session(conn)
    if debug:
        print("Session ID " + str(session_id))

    while power_on:
        power_on = not GPIO.input(17)

    if debug:
        print("Goodbye")
    end_session()
    conn.close()

if __name__ == "__main__":
    main()

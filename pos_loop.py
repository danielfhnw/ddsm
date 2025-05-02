from dotenv import load_dotenv
import os
import serial
import keyboard
import json
import time

if __name__ == "__main__":
    try:
        load_dotenv()
        com_port_motor = os.getenv("COM_PORT_MOTOR")

        ser = serial.Serial(com_port_motor, baudrate=115200, dsrdtr=None, timeout=0.1)
        ser.setRTS(False)
        ser.setDTR(False)

        print("Openend serial port on " + com_port_motor)

        # motor type 210
        command = "{\"T\":11002,\"type\":210}"
        ser.write(command.encode() + b'\n')
        print(f"Sent: {command}")

        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')

        # heartbeat disabled
        command = "{\"T\":11001,\"time\":-1"
        ser.write(command.encode() + b'\n')
        print(f"Sent: {command}")

        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')

        # mode to position control
        command = "{\"T\":10012,\"id\":1,\"mode\":3}"
        ser.write(command.encode() + b'\n')
        print(f"Sent: {command}")

        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')

        command = "{\"T\":10012,\"id\":2,\"mode\":3}"
        ser.write(command.encode() + b'\n')
        print(f"Sent: {command}")

        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')


        pos = 0
        acc = 5
        arrow = 'none'
        old_arrow = 'none'

        pos1 = 0
        pos2 = 0

        while True:
            start = time.time()
            pos = int((pos + 32767/3) % 32767)
            command1 = "{\"T\":10010,\"id\":1,\"cmd\":" + str(pos) + ",\"act\":" + str(acc) + "}"
            command2 = "{\"T\":10010,\"id\":2,\"cmd\":" + str(pos) + ",\"act\":" + str(acc) + "}"

            ser.write(command1.encode() + b'\n')
            time.sleep(0.01)
            data_str = ser.readline().decode('utf-8')
            
            time.sleep(0.01)
            ser.write(command2.encode() + b'\n')
            time.sleep(0.01)
            data_str = ser.readline().decode('utf-8')
            

            print(f"pos1: {pos1},\t pos2: {pos2}")
            sleep_time = 3 - (time.time() - start)
            time.sleep(max(0, sleep_time))
                
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Exiting...")
    finally:
        ser.close()
        print("Serial port closed.")
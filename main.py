from dotenv import load_dotenv
import os
import serial
import keyboard
import time

if __name__ == "__main__":
    try:
        load_dotenv()
        com_port_motor = os.getenv("COM_PORT_MOTOR")

        ser = serial.Serial(com_port_motor, baudrate=115200, dsrdtr=None, timeout=0.05)
        ser.setRTS(False)
        ser.setDTR(False)

        print("Openend serial port on " + com_port_motor)

        command = "{\"T\":11002,\"type\":210}"
        ser.write(command.encode() + b'\n')
        print(f"Sent: {command}")

        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')

        command = "{\"T\":11001,\"time\":-1}"
        ser.write(command.encode() + b'\n')
        print(f"Sent: {command}")

        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')

        vel = 1000
        acc = 5
        arrow = 'none'
        old_arrow = 'none'

        while True:
            if keyboard.is_pressed('up'):
                arrow = 'up'
                command1 = "{\"T\":10010,\"id\":1,\"cmd\":" + str(vel) + ",\"act\":" + str(acc) + "}"
                command2 = "{\"T\":10010,\"id\":2,\"cmd\":-" + str(vel) + ",\"act\":" + str(acc) + "}"
            elif keyboard.is_pressed('down'):
                arrow = 'down'
                command1 = "{\"T\":10010,\"id\":1,\"cmd\":-" + str(vel) + ",\"act\":" + str(acc) + "}"
                command2 = "{\"T\":10010,\"id\":2,\"cmd\":" + str(vel) + ",\"act\":" + str(acc) + "}"
            elif keyboard.is_pressed('left'):
                arrow = 'left'
                command1 = "{\"T\":10010,\"id\":1,\"cmd\":-" + str(vel//2) + ",\"act\":" + str(acc) + "}"
                command2 = "{\"T\":10010,\"id\":2,\"cmd\":-" + str(vel//2) + ",\"act\":" + str(acc) + "}"
            elif keyboard.is_pressed('right'):
                arrow = 'right'
                command1 = "{\"T\":10010,\"id\":1,\"cmd\":" + str(vel//2) + ",\"act\":" + str(acc) + "}"
                command2 = "{\"T\":10010,\"id\":2,\"cmd\":" + str(vel//2) + ",\"act\":" + str(acc) + "}"
            else:
                arrow = 'none'
                command1 = "{\"T\":10010,\"id\":1,\"cmd\":0,\"act\":" + str(acc) + "}"
                command2 = "{\"T\":10010,\"id\":2,\"cmd\":0,\"act\":" + str(acc) + "}"
            
            if arrow != old_arrow:
                old_arrow = arrow
                print(f"Sent: {command1} and {command2}")

            ser.write(command1.encode() + b'\n')
            data = ser.readline().decode('utf-8')
            if data:
                print(f"Received: {data}", end='')
            ser.write(command2.encode() + b'\n')
            data = ser.readline().decode('utf-8')
            if data:
                print(f"Received: {data}", end='')
                

    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        print("Serial port closed.")
import csv
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import serial
import random
import threading

# Input file name
def get_file_name():
    try:
        return input("File name: ").strip()
    except OSError:
        print("Error: Input not allowed in this environment. Using default file name.")
        return "default"

name = get_file_name()
if not name:
    name = "default"

# Ensure Data directory exists
try:
    os.chdir("Data")
except FileNotFoundError:
    os.mkdir("Data")
    os.chdir("Data")

# Create unique directory for the session
while True:
    try:
        os.mkdir(name)
        os.chdir(name)
        break
    except FileExistsError:
        name += str(random.randint(0, 9))

# Create .csv and .txt files
csv_file_path = f"{name}.csv"
txt_file_path = f"{name}.txt"

with open(csv_file_path, "w") as file:
    file.write("count,Time,tear_value[0],tear_value[1],tear_value[2],tear_value[3],tear_value[4],tear_value[5],"
               "ForceInput_x_T[0],ForceInput_x_T[1],ForceInput_x_T[2],ForceInput_x_T[3],ForceInput_x_T[4],ForceInput_x_T[5]\n")

open(txt_file_path, "w").close()

# Plotting function
def me_plot(count, name, var, res):
    if count ==0:
        plt.show()

    if count % res ==0:
        plt.plot(count,)
    for i in range(len(var)):
        plt.plot(count, var[1], "-o", "-l")
    plt.legend(
            loc="upper right",
            labels=[
                f"{name} 1",
                f"{name} 2",
                f"{name} 3",
                f"{name} 4",
                f"{name} 5",
                f"{name} 6",
            ],
        )   
    
    plt.pause(0.0001)

# Define Stewart platform configurations
def define_legs_config_T():
    i = [
        np.array([-0.188, -0.856, 0.481]),
        np.array([0.511, -0.856, -0.078]),
        np.array([-0.323, -0.856, -0.403]),
        np.array([-0.188, -0.856, 0.481]),
        np.array([0.511, -0.856, -0.078]),
        np.array([-0.323, -0.856, -0.403]),
    ]
    b = [
        np.array([77.15, 0.0, 0.0]),
        np.array([-16.97, 0.0, 75.26]),
        np.array([-38.58, 0.0, 66.82]),
        np.array([-56.69, 0.0, -52.33]),
        np.array([-38.58, 0.0, -66.82]),
        np.array([73.66, 0.0, -22.94]),
    ]

    t = np.array([np.concatenate((i[j], np.cross(b[j], i[j]))) for j in range(6)])
    return t

t = define_legs_config_T()

# Serial setup
try:
    ser = serial.Serial("/dev/ttyUSB0", 230400)
    while ser.inWaiting() == 0:
        pass
except serial.SerialException:
    print("Error: Could not open serial port.")
    ser = None

# State handling
def get_state():
    global state, running
    while running:
        try:
            state = input("Enter 't' to tare or 'q' to quit: ").strip()
        except OSError:
            print("Error: Input not allowed. Defaulting state to 'q'.")
            state = "q"
        if state == "q":
            running = False

state = ""
running = True
threading.Thread(target=get_state, daemon=True).start()

# Main loop variables
history = []
tare_val = []
count = 0
history_length = 2
prev_tare_array = np.zeros(6)
write_log = []

# Main loop
try:
    while running and ser:
        try:
            while True:
                data = ser.readline().decode("UTF-8", errors="ignore").strip().split(",")
                if len(data) == 6 and all(map(lambda x: x.replace('.', '', 1).isdigit(), data)):
                    data = list(map(float, data))
                    break
        except ValueError:
            continue

        count += 1
        history.append(data)
        if len(history) > history_length:
            history.pop(0)

        # Calculate moving average
        tear_array = np.mean(history, axis=0)

        if state == "t":
            prev_tare_array = tear_array
            state = ""
            print(f"Tared: {tear_array}")

        data = np.array(data)
        force_vector = np.dot(t, data - prev_tare_array)

        # Log data
        timestamp = time.time()
        write_log.append(f"{timestamp},{count},{','.join(map(str, force_vector))}\n")

        if count % 10 == 0:
            with open(csv_file_path, "a") as file:
                file.writelines(write_log)
            write_log = []

        # Plot data
        me_plot(count, "Force", force_vector, res=10)

        print(f"Force Vector: {force_vector}")

except KeyboardInterrupt:
    pass

# Final notes
try:
    notes = input("Add any notes: ").strip()
except OSError:
    notes = "No notes added."
with open(txt_file_path, "a") as txt_file:
    txt_file.write(f"Notes:\n{notes}\n")

print("Program terminated.")

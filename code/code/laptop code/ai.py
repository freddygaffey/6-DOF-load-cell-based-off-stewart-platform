import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# Serial setup
ser = serial.Serial('/dev/ttyUSB0', 230400)

# Global variables
tear_value = np.zeros(6)
count = 0
plot_res = 2  # higher num means faster plotting less resolution
count_close_open = 0  # make count to open close file
T = None
ForceInput = np.zeros(6)
ForceInput_x_T = np.zeros(6)

# Rolling average setup
average_window = 10
average_ForceInput_x_T_arr = np.zeros((average_window, 6))

def start_files():
    global file, txt_file
    file_name = str(input("File name: "))
    folder_name = file_name
    if os.path.exists("Data") == 0:
        os.mkdir("Data")
    os.chdir("Data")
    os.mkdir(folder_name)
    os.chdir(folder_name)

    if file_name[-4:] != ".csv":
        file_name = file_name + ".csv"
    global file
    file = open(file_name, 'x')
    file.write("count, Time, ForceInput_x_T[0], ForceInput_x_T[1], ForceInput_x_T[2], ForceInput_x_T[3], ForceInput_x_T[4], ForceInput_x_T[5]\n")
    txt_file = file_name[:-4] + " notes" + ".txt"
    txt_file = open(txt_file, 'x')
    txt_file.write("\n")

def ForceInput_x_T_plot(count, ForceInput_x_T):
    if count == 0:
        plt.show()
    if count % plot_res == 0:
        plt.figure("Force Input x T")
        plt.title('Force Input x T')
        plt.legend(loc='upper right', labels=['Force Input 1', 'Force Input 2', 'Force Input 3', 'Force Input 4', 'Force Input 5', 'Force Input 6'])
        for i in range(6):
            if not np.isnan(ForceInput_x_T[i]) and not np.isinf(ForceInput_x_T[i]):
                plt.plot(count, ForceInput_x_T[i], marker='x')
        plt.pause(0.1)

def Force_leg_plot(count, ForceInput):
    if count == 0:
        plt.show()
    if count % plot_res == 0:
        plt.figure("Force Input")
        plt.title('Force Input')
        plt.legend(loc='upper right', labels=['Force Input 1', 'Force Input 2', 'Force Input 3', 'Force Input 4', 'Force Input 5', 'Force Input 6'])
        for i in range(6):
            if not np.isnan(ForceInput[i]) and not np.isinf(ForceInput[i]):
                plt.plot(count, ForceInput[i], marker='x')
        plt.pause(0.1)

def define_legs_config_T():
    # Define the input parameters of these Stewart platform configurations
    i1 = np.array([-0.18802702589737308, -0.8563493948614032, 0.48094859543686896])
    i2 = np.array([0.5105272145216883, -0.8563493948529314, -0.0776381167194588])
    i3 = np.array([-0.32250018854892964, -0.8563493948918757, -0.40331047873099357])
    i4 = np.array([-0.18802702589737308, -0.8563493948614032, 0.48094859543686896])
    i5 = np.array([0.5105272145216883, -0.8563493948529314, -0.0776381167194588])
    i6 = np.array([-0.32250018854892964, -0.8563493948918757, -0.40331047873099357])

    b1 = np.array([77.15154998, 0.0, 0.0])
    b2 = np.array([-16.96943912, 0.0, 75.26220699])
    b3 = np.array([-38.57577499, 0.0, 66.81520222])
    b4 = np.array([-56.69426364, 0.0, -52.32706886])
    b5 = np.array([-38.57577499, 0.0, -66.81520222])
    b6 = np.array([73.66370275, 0.0, -22.93513813])

    # Define the T matrix as in the paper
    global T
    T = np.array([
        np.concatenate((i1, np.cross(b1, i1))),
        np.concatenate((i2, np.cross(b2, i2))),
        np.concatenate((i3, np.cross(b3, i3))),
        np.concatenate((i4, np.cross(b4, i4))),
        np.concatenate((i5, np.cross(b5, i5))),
        np.concatenate((i6, np.cross(b6, i6)))
    ])

def clean_data():
    while ser.inWaiting() == 0:
        pass
    indat = ser.readline().decode('UTF-8', errors='ignore').strip()

    # Remove any nested array structures and extra characters
    indat = indat.replace('[', '').replace(']', '').replace('array(', '').replace(')', '')

    splitInputData = indat.split(',')

    if len(splitInputData) != 6:
        print(f"Warning: Received data with {len(splitInputData)} values instead of 6")
        return np.zeros(6)

    try:
        return np.array([float(value) for value in splitInputData])
    except ValueError as e:
        print(f"Error converting data to float: {e}")
        print(f"Raw data: {indat}")
        return np.zeros(6)

def do_math(ForceInput):
    global ForceInput_x_T, T, tear_value
    ForceInput = ForceInput.reshape(6,)
    raw_force = np.sum(np.multiply(ForceInput[:, np.newaxis], T), axis=1)
    ForceInput_x_T = raw_force + tear_value
    print("Raw Force:", raw_force)
    print("Tared Force (ForceInput_x_T):", ForceInput_x_T)

def write_to_csv():
    global count, file, count_close_open
    count += 1
    Time = time.time()
    string_to_write = f"{count},{Time},{','.join(map(str, ForceInput_x_T))}\n"
    file.write(string_to_write)

    count_close_open += 1
    if count_close_open == 1000:
        file.close()
        file = open(file.name, 'a')  # Reopen the file in append mode
        count_close_open = 0

# def tear():
#     global tear_value, ForceInput_x_T
#     num_samples = 100  # Increase the number of samples for better accuracy
#     accumulated_force = np.zeros(6)

#     print("Taring in progress. Please ensure the platform is unloaded...")

#     for _ in range(num_samples):
#         ForceInput = clean_data()
#         raw_force = np.sum(np.multiply(ForceInput[:, np.newaxis], T), axis=1)
#         accumulated_force += raw_force
#         time.sleep(0.01)  # Short delay between readings

#     average_force = accumulated_force / num_samples
#     tear_value = -average_force

#     print("Taring completed.")
#     print("New tear_value:", tear_value)

def update_average_array(new_data):
    global average_ForceInput_x_T_arr
    average_ForceInput_x_T_arr = np.roll(average_ForceInput_x_T_arr, -1, axis=0)
    average_ForceInput_x_T_arr[-1] = new_data

def end():
    ser.close()
    file.close()
    txt_file_data = input(str("notes: "))
    with open(txt_file.name, 'a') as txt_file:
        txt_file.write(f"notes: {txt_file_data}\n")
    print("Program ended.")

# # Main execution
# start_files()
# define_legs_config_T()

# while True:
#     try:
#         ForceInput = clean_data()
#         do_math(ForceInput)
#         write_to_csv()

#         # Update rolling average array
#         update_average_array(ForceInput_x_T)

#         # Print average and raw values every 10 iterations
#         if count % 10 == 0:
#             average_ForceInput_x_T = np.mean(average_ForceInput_x_T_arr, axis=0)
#             print("Average ForceInput_x_T over last 10 readings:")
#             print(average_ForceInput_x_T)
#             print("Raw ForceInput_x_T values:")
#             print(average_ForceInput_x_T_arr)

#         ForceInput_x_T_plot(count, ForceInput_x_T)
#         Force_leg_plot(count, ForceInput)
#         count += 1

#     except KeyboardInterrupt:
#         user_input = input("Press t to tear and e to exit: ")
#         if user_input == 't':
#             tear()
#         elif user_input == 'e':
#             end()
#             break
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         print(f"ForceInput: {ForceInput}")
#         print(f"ForceInput_x_T: {ForceInput_x_T}")


# [Keep all your import statements and global variables as before]

# [Keep all your functions (start_files, ForceInput_x_T_plot, Force_leg_plot, define_legs_config_T,
#  clean_data, do_math, write_to_csv, update_average_array) as they were in the previous version]

def tear():
    global tear_value, ForceInput_x_T
    num_samples = 100  # Increase the number of samples for better accuracy
    accumulated_force = np.zeros(6)

    print("Taring in progress. Please ensure the platform is unloaded...")

    for _ in range(num_samples):
        ForceInput = clean_data()
        raw_force = np.sum(np.multiply(ForceInput[:, np.newaxis], T), axis=1)
        accumulated_force += raw_force
        time.sleep(0.01)  # Short delay between readings

    average_force = accumulated_force / num_samples
    tear_value = -average_force

    print("Taring completed.")
    print("New tear_value:", tear_value)

def end():
    ser.close()
    file.close()
    print("Program ended.")

# Main execution
print("Starting in 3 seconds. Press Ctrl+C to interrupt.")
for i in range(3, 0, -1):
    print(f"{i}...")
    time.sleep(1)

start_files()
define_legs_config_T()

interrupt_count = 0
last_interrupt_time = 0

while True:
    try:
        ForceInput = clean_data()
        do_math(ForceInput)
        write_to_csv()

        # Update rolling average array
        update_average_array(ForceInput_x_T)

        # Print average and raw values every 10 iterations
        if count % 10 == 0:
            average_ForceInput_x_T = np.mean(average_ForceInput_x_T_arr, axis=0)
            print("Average ForceInput_x_T over last 10 readings:")
            print(average_ForceInput_x_T)
            print("Raw ForceInput_x_T values:")
            print(average_ForceInput_x_T_arr)

        ForceInput_x_T_plot(count, ForceInput_x_T)
        Force_leg_plot(count, ForceInput)
        count += 1

    except KeyboardInterrupt:
        current_time = time.time()
        if current_time - last_interrupt_time < 1:  # If less than 1 second since last interrupt
            interrupt_count += 1
            if interrupt_count >= 3:  # Exit if Ctrl+C pressed 3 times rapidly
                print("\nMultiple interrupts detected. Exiting...")
                break
        else:
            interrupt_count = 1

        last_interrupt_time = current_time

        print("\nInterrupt detected. Taring...")
        tear()

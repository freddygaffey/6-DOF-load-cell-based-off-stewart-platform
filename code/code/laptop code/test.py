import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import threading
# import lists

# // Define the HX711 pins for each load cell
# const int LOADCELL_DOUT_PINS[] = {32, 33, 25, 26, 27, 14};
# const int LOADCELL_SCK_PINS[] = {19, 18, 5, 17, 16, 4};
#  $ sudo chmod 666 /dev/ttyUSB0
# source bin/activate

ser = serial.Serial('/dev/ttyUSB0', 230400)
tear_value = [0, 0, 0, 0, 0, 0]
count = 0
plot_res = 2 # higer num means faster plotting les resolution
count_close_open = 0 # make count to open close file
average_ForceInput_x_T = []
how_ave_tear = 10
average_ForceInput_x_T_arr = np.zeros((how_ave_tear, 6))
print(average_ForceInput_x_T_arr)


def start_files():
    global file
    global txt_file

    # this makes the folder
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
    file.write("count,Time,tear_value[0],tear_value[1],tear_value[2],tear_value[3],tear_value[4],tear_value[5],ForceInput_x_T[0],ForceInput_x_T[1],ForceInput_x_T[2],ForceInput_x_T[3],ForceInput_x_T[4],ForceInput_x_T[5]")
                      # file.write("count, Time, ForceInput_x_T[0], ForceInput_x_T[1], ForceInput_x_T[2], ForceInput_x_T[3], ForceInput_x_T[4], ForceInput_x_T[5] \n")
    txt_file = file_name[:-4] + " notes" + ".txt"
    txt_file = open(txt_file, 'x')
    txt_file.write("\n")

def ForceInput_x_T_plot(count, ForceInput_x_T_plot):
        if count == 0:
            plt.show()
        if count % plot_res == 0:
            plt.figure("Force Input x T")
            plt.title('Force Input x T')
            plt.legend(loc='upper right', labels=['Force Input 1', 'Force Input 2', 'Force Input 3', 'Force Input 4', 'Force Input 5', 'Force Input 6'])
            plt.plot(count, ForceInput_x_T[0], '-o' , '-l')
            plt.plot(count, ForceInput_x_T[1],  marker='x')
            plt.plot(count, ForceInput_x_T[2],  marker='x')
            plt.plot(count, ForceInput_x_T[3],  marker='x')
            plt.plot(count, ForceInput_x_T[4],  marker='x')
            plt.plot(count, ForceInput_x_T[5],  marker='x')
            plt.pause(0.0001)

def Force_leg_plot(count, ForceInput):
    if count == 0:
        plt.show()
    if count % plot_res == 0:
        plt.figure("Force Input")
        plt.title('Force Input')
        plt.legend(loc='upper right', labels=['Force Input 1', 'Force Input 2', 'Force Input 3', 'Force Input 4', 'Force Input 5', 'Force Input 6'])
        plt.plot(count, ForceInput[0],  marker='x')
        plt.plot(count, ForceInput[1],  marker='x')
        plt.plot(count, ForceInput[2],  marker='x')
        plt.plot(count, ForceInput[3],  marker='x')
        plt.plot(count, ForceInput[4],  marker='x')
        plt.plot(count, ForceInput[5],  marker='x')
        plt.pause(0.0001)

def define_legs_config_T():
    # Define the input parameters of these Stewart platform configurations
    #the configurations form my CAD model
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
    T = np.array(
                [np.concatenate((i1, np.cross(b1, i1))),
                np.concatenate((i2, np.cross(b2, i2))),
                np.concatenate((i3, np.cross(b3, i3))),
                np.concatenate((i4, np.cross(b4, i4))),
                np.concatenate((i5, np.cross(b5, i5))),
                np.concatenate((i6, np.cross(b6, i6)))])

def end():
    ser.close()  # to restore the current working directory
    file.close()
    txt_file_data = input(str("notes: "))
    txt_file = open(txt_file_data, 'x')
    txt_file.write(f"notes: {txt_file_data}")
    txt_file.write("testing")

    txt_file.close()
    pass

def clean_data():
    global splitInputData
    while ser.inWaiting() == 0:
        pass
    indat = ser.readline().decode('UTF-8', errors='ignore').strip()
    splitInputData = indat.split(",")

    if len(splitInputData) != 6:
        splitInputData = [0,0,0,0,0,0]

    try:
        # Convert to float and replace any non-numeric values with 0
        # splitInputData = np.array([float(value) if value.replace('.', '').isdigit() else 0 for value in splitInputData])
        splitInputData = [float(value) for value in splitInputData]
        np.array(splitInputData)

    except ValueError:
        # print(f"Warning: Received invalid data: {splitInputData}")
        splitInputData = [0,0,0,0,0,0]
        np.array(splitInputData)


def do_math():
    global splitInputData, ForceInput_x_T, T, tear_value, ForceInput, average_ForceInput_x_T, average_ForceInput_x_T_arr
    ForceInput = np.array(splitInputData)
    ForceInput_x_T = np.sum(np.multiply(ForceInput[:, np.newaxis], T), axis=0)
    np.array(tear_value)
    ForceInput_x_T -= tear_value
    # print("ForceInput:", ForceInput)
    # print("ForceInput_x_T:", ForceInput_x_T)
    if count == 0:
            average_ForceInput_x_T = ForceInput_x_T

    point_in_buffer = count % how_ave_tear

    average_ForceInput_x_T_arr[point_in_buffer-1] = ForceInput_x_T
    average_ForceInput_x_T = np.sum(average_ForceInput_x_T_arr, axis=0) / how_ave_tear
    # print(average_ForceInput_x_T)
    # print("ave tar arr")

        # sum(axis=0)

# if np.prod() >



def write_to_csv():
        global count, file , open, time, tear_value
        count += 1
        Time = time.time()
        # string_to_write = str(count) + "," + str(Time) + "," + str(tear_value[0]) + "," + str(tear_value[0]) + "," + str(tear_value[0]) + "," + str(tear_value[0]) +  "," + str(tear_value[0]) + "," + str(tear_value[0]) + "," + str(ForceInput_x_T[0]) + "," + str(ForceInput_x_T[1]) + "," + str(ForceInput_x_T[2]) + "," + str(ForceInput_x_T[3]) + "," + str(ForceInput_x_T[4]) + "," + str(ForceInput_x_T[5])
        string_to_write = "str(count) + "," + str(Time) + "," + str(tear_value[0]) + "," + str(tear_value[1]) + "," + str(tear_value[2]) + "," + str(tear_value[3]) + "," + str(tear_value[4]) + "," + str(tear_value[5])) + "," str(ForceInput_x_T[0]) + "," + str(ForceInput_x_T[1]) + "," + str(ForceInput_x_T[2]) + "," + str(ForceInput_x_T[3]) + "," + str(ForceInput_x_T[4]) + "," + str(ForceInput_x_T[5])"

        file.write(str(string_to_write))
        file.write("\n")

        count_close_open =+ 1

        if count_close_open == 1000:
            file.close()
            file.open()
            count_close_open = 0

def tear():
    global tear_value, average_ForceInput_x_T

    tear_value = average_ForceInput_x_T
    print(tear_value)

start_files()
define_legs_config_T()



while True:
    try:
        define_legs_config_T()
        clean_data()
        do_math()
        write_to_csv()
        # ForceInput_x_T_plot(count=count, ForceInput_x_T_plot= ForceInput_x_T)
        # Force_leg_plot(count,ForceInput)
        if count % 4 == 0:
            tear()
    except KeyboardInterrupt:
        tear()
        user_input = input("Press t to tear and e to exit: ")
        if user_input == 't':
            print("ran ter")
            tear()
        if user_input == 'e':
            end()



# add time dellays betwn ^C to tear

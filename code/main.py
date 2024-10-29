import time
import serial 
import numpy as np
import matplotlib.pyplot as plt
# import csv
import os
# import threading

# // Define the HX711 pins for each load cell
# const int LOADCELL_DOUT_PINS[] = {32, 33, 25, 26, 27, 14};
# const int LOADCELL_SCK_PINS[] = {19, 18, 5, 17, 16, 4};
# $ sudo chmod 666 ..//..//../../../dev/ttyUSB0

ser = serial.Serial('/dev/ttyUSB0', 230400)
tear_value = [0, 0, 0, 0, 0, 0]
count = 0
plot_res = 100 # higer num means faster plotting les resolution
count_close_open = 0 # make count to open close file


def start_files():
    global file
    global txt_file
    global file_name
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
    file = open(file_name, 'x')
    file.write("count, Time, ForceInput_x_T[0], ForceInput_x_T[1], ForceInput_x_T[2], ForceInput_x_T[3], ForceInput_x_T[4], ForceInput_x_T[5] \n")
    txt_file = file_name[:-4] + " notes" + ".txt"
    txt_file = open(txt_file, 'x')
    txt_file.write("\n")

def ForceInput_x_T_plot():
    if count == 0:
        plt.show()
    if count % plot_res == 0:
        plt.figure("Force Input x T")
        plt.title('Force Input x T')
        plt.legend(loc='upper right', labels=['Force Input 1', 'Force Input 2', 'Force Input 3', 'Force Input 4', 'Force Input 5', 'Force Input 6'])
        plt.plot(count, ForceInput_x_T[0],  marker='x')
        plt.plot(count, ForceInput_x_T[1],  marker='x')
        plt.plot(count, ForceInput_x_T[2],  marker='x')
        plt.plot(count, ForceInput_x_T[3],  marker='x')
        plt.plot(count, ForceInput_x_T[4],  marker='x')
        plt.plot(count, ForceInput_x_T[5],  marker='x')
        plt.pause(0.01)

def Force_leg_plot():
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
        plt.pause(0.01 )



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


def readSerial_writeTOcsv():

    global count, ForceInput_x_T, ForceInput, count_close_open, file

    while ser.inWaiting() == 0:
        pass
    indat = ser.readline().decode('UTF-8', errors='ignore').strip()
    splitInputData = indat.split(",")


    try:
        if len(splitInputData) != 6:
            splitInputData = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        else:
            # Explicitly convert each value to float
            splitInputData = [float(x) for x in splitInputData]
    except ValueError:
        splitInputData = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]



    # Convert the list to a numpy array
    splitInputData = ForceInput = np.array(splitInputData)
    ForceInput_x_T = np.sum(np.multiply(ForceInput[:, np.newaxis], T), axis=1)+tear_value
    print(ForceInput_x_T)
    count += 1
    Time = time.time()
    string_to_write = str(count)  + "," + str(Time) +  str(ForceInput_x_T[0]) + "," + str(ForceInput_x_T[1]) + "," + str(ForceInput_x_T[2]) + "," + str(ForceInput_x_T[3]) + "," + str(ForceInput_x_T[4]) + "," + str(ForceInput_x_T[5])
    file.write(str(string_to_write))
    file.write("\n")
    count_close_open =+ 1

    # if count_close_open % 1000:
    #     file.close()
    #
    #     open(file_name, 'a')
    # count_close_open = 0
    


def tear():
    global tear_value
    i = 0
    average_ForceInput_x_T = 0
    for i in range(10): # amount to average
        average_ForceInput_x_T = float(average_ForceInput_x_T + ForceInput_x_T) / 2
        i += 1
    tear_value = 0 - average_ForceInput_x_T
    print(tear_value)

start_files()
define_legs_config_T()


while True:
    try:
        readSerial_writeTOcsv()
        ForceInput_x_T_plot()
        Force_leg_plot()
    except KeyboardInterrupt:
        user_input = input("Press t to tear and e to exit: ")
        if input() == 't':
            tear()
        if user_input == 'e':
            end()





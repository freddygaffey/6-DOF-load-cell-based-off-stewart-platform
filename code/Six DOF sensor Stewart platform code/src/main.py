import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import threading


ser = serial.Serial('COM6', 230400)
tear_value = [0, 0, 0, 0, 0, 0]
count = 0


def start_files():
    global file
    global txt_file

    file_name = str(input("file name: "))
    folder_name = file_name
    relative_path_to_data = os.chdir(os.path.join("code", "Data"))  # Relative path to the "Data" folder from the current working directory
    starDr = os.getcwd()
    os.mkdir(folder_name)
    os.chdir(folder_name)
    if file_name[-4:] != ".csv":
        file_name = file_name + ".csv"
    global file
    file = open(file_name, 'x')
    file.write("count, Time, ForceInput_x_T[0], ForceInput_x_T[1], ForceInput_x_T[2], ForceInput_x_T[3], ForceInput_x_T[4], ForceInput_x_T[5] \n")
    txt_file = file_name[:-4] + "notes" + ".txt"
    txt_file = open(txt_file, 'x')
    txt_file.write("\n")
start_files()
def force_plot():
    plt.ion()
    plt.figure("Force Input x T")
    plt.plot(count, ForceInput_x_T[0],  marker='x')
    plt.plot(count, ForceInput_x_T[1],  marker='x')
    plt.plot(count, ForceInput_x_T[2],  marker='x')
    plt.plot(count, ForceInput_x_T[3],  marker='x')
    plt.plot(count, ForceInput_x_T[4],  marker='x')
    plt.plot(count, ForceInput_x_T[5],  marker='x')
    plt.legend(loc='upper right', labels=['Force Input 1', 'Force Input 2', 'Force Input 3', 'Force Input 4', 'Force Input 5', 'Force Input 6'])
    plt.pause(0.01)
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
define_legs_config_T()
def end():
    ser.close()  # to restore the current working directory
    file.close()
    txt_file_notes = input(str("notes: "))
    txt_file.write(txt_file_notes)
    txt_file.close()
    ThreadUserInput.join()
    Thread_tear.join()
    Thread_readSerial_writeTOcsv.join()
    Thread_force_plot.join()
    pass
def readSerial_writeTOcsv():
        global ForceInput_x_T
        global ForceInput
        global count
        while ser.inWaiting() == 0:
            pass
        indat = ser.readline().decode('UTF-8', errors='ignore').strip()
        splitInputData = indat.split(",")
        
        # Check if the length of the input data is 6
        if len(splitInputData) != 6:
            splitInputData = [0, 0, 0, 0, 0, 0]
        else:
            splitInputData = [float(value) for value in splitInputData]

        # Convert the list to a numpy array
        splitInputData = ForceInput = np.array(splitInputData)
        ForceInput_x_T = np.sum(np.multiply(ForceInput[:, np.newaxis], T), axis=1)+tear_value
        count += 1
        Time = time.time()
        #string_to_write = count, count, Time, ForceInput, ForceInput_x_T
        string_to_write = str(count)  + "," + str(Time) +  str(ForceInput_x_T[0]) + "," + str(ForceInput_x_T[1]) + "," + str(ForceInput_x_T[2]) + "," + str(ForceInput_x_T[3]) + "," + str(ForceInput_x_T[4]) + "," + str(ForceInput_x_T[5])
        file.write(str(string_to_write))
        file.write("\n")
def tear():
    global tear_value 
    i = 0
    average_ForceInput_x_T = 0
    for i in range(10): # amount to average 
        average_ForceInput_x_T = float(average_ForceInput_x_T + ForceInput_x_T) / 2
        i += 1
    tear_value = 0 - average_ForceInput_x_T
    print(tear_value)
def UserInput():
    global user_input
    user_input = input("Press t to tear and e to exit")
# def start_Threads():
#     ThreadUserInput = threading.Thread(target=UserInput)
#     ThreadUserInput.start()
#     Thread_tear = threading.Thread(target=tear)
#     Thread_tear.start()
#     Thread_readSerial_writeTOcsv = threading.Thread(target=readSerial_writeTOcsv)
#     Thread_readSerial_writeTOcsv.start()
#     Thread_force_plot = threading.Thread(target=force_plot)
#     Thread_force_plot.start()



try:
    while True:
        if KeyboardInterrupt == True:
            next_action = input("Press t to tear and e to exit")
            if input() == 't':
                # TODO: make a function to tear()
                pass 
        readSerial_writeTOcsv()
        force_plot()


except KeyboardInterrupt:
    ser.close()  # to restore the current working directory
    file.close()
    txt_file_notes = input(str("notes: "))
    txt_file.write(txt_file_notes)
    txt_file.close()
    ThreadUserInput.join()
    Thread_tear.join()
    Thread_readSerial_writeTOcsv.join()
    Thread_force_plot.join()
    pass





    
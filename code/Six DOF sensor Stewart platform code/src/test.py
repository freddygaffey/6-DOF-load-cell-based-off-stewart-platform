
import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
ser = serial.Serial('COM6', 230400)

file_name = str(input("file name: "))
folder_name = file_name
relative_path_to_data = os.chdir(os.path.join("code", "Data"))  # Relative path to the "Data" folder from the current working directory
starDr = os.getcwd()
os.mkdir(folder_name)
os.chdir(folder_name)
if file_name[-4:] != ".csv":
    file_name = file_name + ".csv"
file = open(file_name, 'x')
file.write("\n")
txt_file = file_name[:-4] + "notes" + ".txt"
txt_file = open(txt_file, 'x')
txt_file.write("\n")

def force_plot():
    plt.ion()
    plt.figure("Force Input x T")
    plt.plot(Time, ForceInput_x_T[0],  marker='x')
    plt.plot(Time, ForceInput_x_T[1],  marker='x')
    plt.plot(Time, ForceInput_x_T[2],  marker='x')
    plt.plot(Time, ForceInput_x_T[3],  marker='x')
    plt.plot(Time, ForceInput_x_T[4],  marker='x')
    plt.plot(Time, ForceInput_x_T[5],  marker='x')
    plt.legend(loc='upper right', labels=['Force Input 1', 'Force Input 2', 'Force Input 3', 'Force Input 4', 'Force Input 5', 'Force Input 6'])
    plt.pause(0.01)

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
T = np.array(
            [np.concatenate((i1, np.cross(b1, i1))),
            np.concatenate((i2, np.cross(b2, i2))),
            np.concatenate((i3, np.cross(b3, i3))),
            np.concatenate((i4, np.cross(b4, i4))),
            np.concatenate((i5, np.cross(b5, i5))),
            np.concatenate((i6, np.cross(b6, i6)))])

   
datalog = np.zeros((1, 6))
forceLog = np.zeros((1, 6))
startTime = time.time()
timelog = currentTime = time.time()
TimesSinceStartLog = 0   
count = 0
i = 0

try:
    # Main loop to read from the serial port
    while True:
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
        ForceInput_x_T = np.sum(np.multiply(ForceInput[:, np.newaxis], T), axis=1)
        count += 1
        Time = time.time()
        #string_to_write = count, count, Time, ForceInput, ForceInput_x_T
        string_to_write = str(count)  + "," + str(Time) + "," + str(Time) +  str(ForceInput_x_T[0]) + "," + str(ForceInput_x_T[1]) + "," + str(ForceInput_x_T[2]) + "," + str(ForceInput_x_T[3]) + "," + str(ForceInput_x_T[4]) + "," + str(ForceInput_x_T[5])
        file.write(str(string_to_write))
        file.write("\n")

        i +=1
        if i == 50:
            i = 0
            force_plot()

        

            
except KeyboardInterrupt:
    ser.close()  # to restore the current working directory
    file.close()
    txt_file_notes = input("notes: ")
    txt_file.write(txt_file_notes)
    txt_file.close()
    pass
   
   
   
   
       
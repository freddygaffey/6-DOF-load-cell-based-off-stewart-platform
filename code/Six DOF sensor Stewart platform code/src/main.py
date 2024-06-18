import time
import serial
import numpy as np
import matplotlib.pyplot as plt
ser = serial.Serial('COM6', 230400)


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
print("T Matrix:")
print(T)

time.sleep(1)

datalog = np.zeros((1, 6))
forceLog = np.zeros((1, 6))
try:
    # Main loop to read from the serial port
    while True:
        while ser.inWaiting() == 0:
            pass

        # Read a line of data from the serial port
        indat = ser.readline().decode('UTF-8', errors='ignore').strip()
        
        # Split the input data by commas
        splitInputData = indat.split(",")
        
        # Check if the length of the input data is 6
        if len(splitInputData) != 6:
            splitInputData = [0, 0, 0, 0, 0, 0]
        else:
            # Convert the split data to floats
            splitInputData = [float(value) for value in splitInputData]

        # Convert the list to a numpy array
        splitInputData = np.array(splitInputData)
        #print("Split Input Data:", splitInputData)

        datalog = np.vstack((datalog, splitInputData))

        ForceInput = splitInputData
        ForceInput_x_T = np.sum(np.multiply(ForceInput[:, np.newaxis], T), axis=1)

        # Append the new data to the datalog
        forceLog = np.vstack((forceLog, ForceInput_x_T))

        # Print the force input and calculated force vector
        print("Force Input:", ForceInput)
        print("Force Input x T:", ForceInput_x_T)

except KeyboardInterrupt:
    # Handle the keyboard interrupt
    print("Force Log:")
    print(forceLog)
    # Optionally, close the serial port
    ser.close()

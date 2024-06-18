import time
import serial
import numpy as np
import matplotlib.pyplot as plt
ser = serial.Serial('COM6', 230400)


# Define the input parameters of these Stewart platform configurations as in imige in the 
i1 = np.array([-0.18802703, -0.85634939,  0.4809486, ])
i2 = np.array([3, 2, 1])
i3 = np.array([1, 2, 3])
i4 = np.array([3, 2, 1])
i5 = np.array([1, 2, 3])
i6 = np.array([3, 2, 1])

b1 = np.array([1, 2, 3])
b2 = np.array([3, 2, 1])
b3 = np.array([1, 2, 3])
b4 = np.array([3, 2, 1])
b5 = np.array([1, 9, 3])
b6 = np.array([3, 2, 8])


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
        # Wait until data is available in the serial buffer
        while ser.inWaiting() == 0:
            pass

        # Read a line of data from the serial port
        indat = ser.readline().decode('UTF-8', errors='ignore').strip()
        
        # Split the input data by commas
        splitInputData = indat.split(",")
        
        # Check if the length of the input data is 6
        if len(splitInputData) != 6:
            # If not, use a default array of zeros
            splitInputData = [0, 0, 0, 0, 0, 0]
        else:
            # Convert the split data to floats
            splitInputData = [float(value) for value in splitInputData]

        # Convert the list to a numpy array
        splitInputData = np.array(splitInputData)
        #print("Split Input Data:", splitInputData)

        # Append the new data to the datalog
        datalog = np.vstack((datalog, splitInputData))

        # Calculate the force vector
        ForceInput = splitInputData
        ForceInput_x_T = np.sum(np.multiply(ForceInput[:, np.newaxis], T), axis=1)

        # Append the new force data to the forceLog
        forceLog = np.vstack((forceLog, ForceInput_x_T))

        # Print the force input and calculated force vector
        print("Force Input:", ForceInput)
        print("Force Input x T:", ForceInput_x_T)
    

except KeyboardInterrupt:
    # Handle the keyboard interrupt
    print("done")
    print("Force Log:")
    print(forceLog)
    # Optionally, close the serial port
    ser.close()
    

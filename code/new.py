import csv
import os
from posix import chdir, mkdir, write
import time
import matplotlib.pyplot as plt
import numpy as np
from numpy._core.numeric import array
from numpy.random import get_state, rand, random
import serial
import random
import threading


#make files
name = input("File name: ")
if name == "":
    name = " "

try:
    os.chdir("Data")
except FileNotFoundError:
    os.mkdir("Data")
    os.chdir("Data")

try:
    os.mkdir(name)
    os.chdir(name)
    file = open(name  + ".csv", "x")
    file.write("count,Time,tear_value[0],tear_value[1],tear_value[2],tear_value[3],tear_value[4],tear_value[5],ForceInput_x_T[0],ForceInput_x_T[1],ForceInput_x_T[2],ForceInput_x_T[3],ForceInput_x_T[4],ForceInput_x_T[5]")
     
    
    txt_file = open(name + ".txt", "x")
    f = True
except FileExistsError:
    name = name + str(random.random())
    os.mkdir(name)
    os.chdir(name)
    file = open(name + ".csv", "x")

# plot
def me_plot(count,var):
    if count ==0:
        plt.show()

    if count % 10 ==0:
        plt.plot(count,)
    for i in range(len(var)):
        plt.plot(count, var[i], "-o", "-l")
    plt.pause(0.0001)

# define t
def define_t():
    global t
    # Define the input parameters of these Stewart platform configurations
    # the configurations form my CAD model
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
    
    t = np.array(
        [
            np.concatenate((i1, np.cross(b1, i1))),
            np.concatenate((i2, np.cross(b2, i2))),
            np.concatenate((i3, np.cross(b3, i3))),
            np.concatenate((i4, np.cross(b4, i4))),
            np.concatenate((i5, np.cross(b5, i5))),
            np.concatenate((i6, np.cross(b6, i6))),
        ]
    )
    np.array(t,dtype=float)
    return t
define_t()


def data():
    ser = serial.Serial("/dev/ttyUSB0", 230400)
    while ser.inWaiting() == 0:
        pass
    data = ser.readline().decode("UTF-8", errors="ignore").strip()
    data = data.split(",")
    count = 0
    while True:
        try:
            if count == 0:
                  if len(data) != 6:
                    data = [0]*6 
            float(data[count])
            count += 1
        except ValueError:
            data = [0]*6
        except TypeError:
            data = [0]*6
        if count ==5:
            break
    return np.array(data,float)

history =[]
def tear(data,length):
    global history
    if len(history) != length:
        history= [data]*length
        print(history)
    else:
        history.append(data)
    tear_array = [0]*6
    for i in history:
       a = 0
       for j in i:
           float(j)
           temp = float(j)
           temp = tear_array[a] + temp
           tear_array[a] = temp 
           a +=1
    tear_array = np.divide(tear_array,length)
    return tear_array




    

state = ""
def get_state():
    global state, txt_file,true
    while True:
        state = input("t for tear q for quit")
        threading.Thread(target=get_state,daemon=True).start()
        if state == "q":
            break
threading.Thread(target=get_state,daemon=True).start()

pev_tear_array = tear(data(),10)
while True:
    if state == "t":
       pev_tear_array = tear(data(),length = 10)
       state = ""
       print(f"tearred and the tear val is {tear(data=data(),length=10)}")

    t = np.array(t, dtype=float)
    pev_tear_array = np.array(pev_tear_array,dtype=float)
    force_vector = np.dot(t,data())        
    pev_tear_array = np.dot(t,pev_tear_array)
    force_vector = np.subtract(np.array(pev_tear_array,dtype=float),force_vector)
    print(f"{force_vector[0]}    {force_vector[1]}    {force_vector[2]}    {force_vector[3]}    {force_vector[4]}    {force_vector[5]}")


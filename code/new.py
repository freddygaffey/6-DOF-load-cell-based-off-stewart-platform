import csv
import os
from posix import chdir, mkdir
import time
import matplotlib.pyplot as plt
import numpy as np
from numpy._core.numeric import array
from numpy.random import get_state, rand, random
import serial
import random
import threading


name = input("File name: ")
if name == "":
    name = " "
# if name[-4:] != ".csv":
    # name=name + ".csv"

try:
    os.chdir("Data")
except FileNotFoundError:
    os.mkdir("Data")


f = False

while f ==False:
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
        
        file.write("hi")
        file.write("count,Time,ForceInput[0],ForceInput[1],ForceInput[2],ForceInput[3],ForceInput[4],ForceInput[5]")
        file.close()

        txt_file = open(name + ".txt", "x")
        txt_file.close()
        f = True

    
def me_plot(count, name,var,res):
    if count ==0:
        plt.show()
    if count % res ==0:
        plt.plot(count,)
    # for i in range(len(var)):
    plt.plot(count, var[1], "-o", "-l")
    plt.legend(
            loc="upper right",
            labels=[
                f"{name} 1",
                # f"{name} 2",
                # f"{name} 3",
                # f"{name} 4",
                # f"{name} 5",
                # f"{name} 6",
            ],
        )   
    
    plt.pause(0.0001)

def define_legs_config_T():
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
    return t
define_legs_config_T()


ser = serial.Serial("/dev/ttyUSB0", 230400)
while ser.inWaiting() == 0:
    pass

state = ""
get_state_if_running = False
def get_state():
    global state, txt_file,true
    state = input("t for tear q for quit")
    if state == "q":
        true = False
    get_state_if_running = True  
 #    if state == "q":
 #            txt_file = open(f"{txt_file}.txt","a")
 #            txt_file.write("""notes:
 #            """)
 #            write_to_txt = input("add aney notes:")
 #            txt_file.write(write_to_txt)
 #    true = False
 # 
 #    print("-"*10)
# threading.Thread(target=get_state,daemon=True).start()

history = []
tare_val = []
count = 0
history_length = 3

pev_tear_array = [0]*6
true = True
while true == True:
    try:
        while True:
            try:
                data = ser.readline().decode("UTF-8", errors="ignore").strip()
                data = data.split(",")
                if len(data) != 6:
                    float("hi") 
                for i in data:
                    i = float(i)
                break
            except ValueError:
                del data
                
            count += 1 

        history.append(data)
        if len(history) > history_length:
            history.pop(0)

        # history = [[1]*6]*10
        tear_array = [0]*6
        for i in history:
            a = 0
            for j in i:
                float(j)
                temp = 0
                temp = float(j)
                temp = tear_array[a] + temp
                tear_array[a] = temp 
                a +=1
        tear_array = np.divide(tear_array,history_length)
        
        # print(f"tear array: {tear_array}")
        # print(f"data: {data}")
        # print(f"final: {temp}")


        # threading.Thread(target=get_state,daemon=True).start()
        if state == "t" or count >= 3:
            pev_tear_array = tear_array
            state = ""
            print(f"tearred and the tear val is {tear_array}")
        if not get_state_if_running:
            get_state_if_running = True
            threading.Thread(target=get_state,daemon=True).start()
            state = ""

        # if state == "q":
        #     true = False
        #     txt_file = open(f"{txt_file}.txt","a")
        #     txt_file.write("""notes:
        #     """)
        #     write_to_txt = input("add aney notes:")
        #     txt_file.write(write_to_txt)
        data = np.array(data,dtype=float) - np.array(pev_tear_array,dtype=float)
        t = np.array(t, dtype=float)
        me_plot(count=count,var=data,res=2,name="sda")
        force_vector = np.dot(t,data)        
        
        timestamp = time.time()
        # print(timestamp)
        force_str = str(force_vector)
        print(force_str)
        file = open(f"{name}.csv" ,"a" ) 
        file.write(f"{count},{timestamp},{force_str}")
        file.write("""
        """)
        file.close()

    except KeyboardInterrupt:
        break
       # txt_file = open(f"{txt_file}.txt","a")
       # txt_file.write("""notes:
       # """)
       # write_to_txt = input("add aney notes:")
       # txt_file.write(write_to_txt)
       # true = False

txt_file = open(f"{txt_file}.txt","a")
txt_file.write("""notes:
""")
write_to_txt = input("add aney notes:")
txt_file.write(write_to_txt)
true = False





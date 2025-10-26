import csv
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import serial
import random
import tkinter as tk
import threading

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure

class dof6():
    def __init__(self):
        self.t = self.define_t()
        self.dir_name = "6DOF_logs"
        self.curent_log_file_name = str(time.time())
        # self.log_rate = 100 # times per second 
        self.ser = None
        self.logging_state = False
        self.to_plot_buff = []

        
        if self.dir_name not in os.listdir():
            os.mkdir(self.dir_name)
            open(f"{self.curent_log_file_name}/tear_values.csv").close()
        os.chdir(self.dir_name)
        
        self.per_leg_calib = self.get_per_leg_calib()
        self.tear_valus = self.get_per_leg_tears()
        
        
        
    def define_t(self):
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
        t = np.array(t,dtype=float)
        return t
    
    def tk_app(self):
        self.root = tk.Tk()
        # ----- make side bar
        side_bar = tk.Frame(self.root,relief=tk.SUNKEN)
        side_bar.pack(side=tk.RIGHT, fill=tk.Y)

        start_logging_bott = tk.Button(
            side_bar,
            text="Start logging",
            background="green",
            foreground="white",
            borderwidth=4,
            command=lambda:self.start_loging()
        )
        
        start_logging_bott.grid(row=0,column=0,padx=10,pady=10)
        
        stop_logging_bott = tk.Button(
            side_bar,
            text="Stop logging",
            background="red",
            foreground="white",
            borderwidth=4,
            command=lambda:self.stop_loging()
        )
        stop_logging_bott.grid(row=1,column=0,padx=10,pady=10)
        
        
        tear_bott = tk.Button(
            side_bar,
            text="Tear",
            background="lightblue",
            foreground="black",
            borderwidth=4,
            command=lambda: self.tear()
        )
        tear_bott.grid(row=2,column=0,padx=10,pady=10)
        
        remove_all_logs_bott = tk.Button(
            side_bar,
            text="Remove all logfiles",
            background="gray",
            foreground="black",
            borderwidth=4,
            command=lambda:self.remove_all_logs()
        )
        remove_all_logs_bott.grid(row=3,column=0,padx=10,pady=10)
               
        
        self.root.mainloop()
    
        
    def update_plt_auto(self):
        print("ran update_plt_auto") 
        self.root.after(1000, self.update_plt_auto)
        
          
    def start_loging(self):
        self.curent_log_file_name = str(time.time())
        self.curent_log_file = open(f"{self.curent_log_file_name}.csv","x")
        self.curent_log_file.writelines(["Time,ForceInput_x_T[0],ForceInput_x_T[1],ForceInput_x_T[2],ForceInput_x_T[3],ForceInput_x_T[4],ForceInput_x_T[5]\n"]) 
        self.logging_state = True
        self.log_thead = threading.Thread(target=self.log_force,daemon=True)
        self.log_thead.start()

    def stop_loging(self):
        self.logging_state = False
        self.log_thead.join()
        print("logging stoped")
        self.curent_log_file.close()
        del(self.curent_log_file)

    def tear(self,num_samples=10):
        if self.logging_state == True:
            raise ValueError(" you need to stop loggin to tear")
            return 0
        
        self.tear_valus
    
        tear_arr = []
        for i in range(num_samples):
            i = self.get_leg_values_clean()
            for j in range(len(i)):
                i[j] *= self.per_leg_calib[j]
            tear_arr.append(i)
            
        np_arr_for_tear = np.zeros(6)
        for vals in tear_arr:
            np_arr_for_tear += np.array(vals, dtype=float)

        tear_values = np_arr_for_tear / len(tear_arr)
        
        self.tear_valus = tear_values
        
        print(tear_values," these are the tear values")
        with open("tear_values.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for i, val in enumerate(tear_values):
                writer.writerow([f"leg[{i}]", val])
                
    def remove_all_logs(self):
        files = os.listdir()
        for i in files:
            if i == "tear_values.csv" or i == "calibration_factors.csv":
                pass
            else:
                os.remove(i)
                
    def calulate_forces(self,force_on_each_leg: list)->list:
        teared_force_on_each_leg = []
        
        for i in range(len(force_on_each_leg)):
            force_on_each_leg[i] *= self.per_leg_calib[i]
            
        for i in range(len(force_on_each_leg)):
            teared_force_on_each_leg.append(force_on_each_leg[i] - self.tear_valus[i])
        
        teared_force_on_each_leg = np.array(teared_force_on_each_leg)
        forces_teared = np.dot(self.t,teared_force_on_each_leg)
    
        print(forces_teared)
        return forces_teared

    def get_per_leg_tears(self)->list:
        tear_file = open("tear_values.csv","r")
        contence = tear_file.readlines()
        tear_leg_values = []
        for i in contence:
            i = i.strip().split(',')
            i[1] = float(i[1])
            tear_leg_values.append(i[1])
        return tear_leg_values
    
    def get_per_leg_calib(self)->list:
        tear_file = open("calibration_factors.csv","r")
        contence = tear_file.readlines()
        calibration_factors = []
        for i in contence:
            i = i.strip().split(',')
            i[1] = float(i[1])
            calibration_factors.append(i[1])
        return calibration_factors
    
    def log_force(self):
        while self.logging_state:
            force = self.calulate_forces(self.get_leg_values_clean())
            force = list(force)
            self.to_plot_buff.append([time.time()] + force)
            
            force_str = ""
            for i in range(len(force)):
                force_str += str(float(force[i])) + ","
            force_str = force_str[0:-1]
            force_str += "\n"
            force_str = str(time.time()) + "," + force_str
            self.curent_log_file.write(force_str)
        
    
    def get_leg_values_clean(self,port="COM22",baudrate=9600):
        while 1:
            if not self.ser:
                self.ser =  serial.Serial(port, baudrate=baudrate)
            data = self.ser.readline().decode("UTF-8", errors="ignore").strip()
            data = data.split(",")
            for i in range(len(data)):
                try:
                    data[i] = float(data[i])
                except ValueError:
                    continue

            if len(data) != 6:
                continue
            return data
    
    def calibrate_legs(self, known_weight: float, num_samples: int = 50):
        # this is a ai function I did not want to wright it my eslf
        """
        Calibrates each leg of the 6DOF platform using a known weight.

        Parameters:
        - known_weight: float, the weight in kilograms placed on the platform
        - num_samples: int, number of samples to average per leg

        Outputs:
        - Writes 'calibration_factors.csv' with per-leg scale factors
        - Returns a numpy array of the scale factors
        """

        # Step 1: Collect multiple samples like in tear()
        leg_samples = []
        for _ in range(num_samples):
            leg_samples.append(self.get_leg_values_clean())  # returns list of 6 raw readings

        # Step 2: Compute average per leg
        leg_samples = np.array(leg_samples, dtype=float)
        mean_forces = np.mean(leg_samples, axis=0)  # [f1_mean, f2_mean, ..., f6_mean]

        # Step 3: Compute expected per-leg force
        g = 9.81  # m/s^2
        total_expected_force = known_weight * g
        expected_per_leg = total_expected_force / 6

        # Step 4: Compute per-leg scale factors
        scale_factors = expected_per_leg / mean_forces  # array of 6 factors

        # Step 5: Save to CSV
        with open("calibration_factors.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for i, factor in enumerate(scale_factors):
                writer.writerow([f"leg[{i}]", factor])

        print("Calibration complete. Scale factors per leg:", scale_factors)
        return scale_factors

if __name__ == "__main__":
    app = dof6()
    app.tk_app()
    app.update_plt_auto()
    # app.calibrate_legs(4)
    print(app.get_per_leg_tears())
    app.tear(num_samples=100)

    
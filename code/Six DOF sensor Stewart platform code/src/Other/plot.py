# import serial
# import tabulate
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from tabulate import tabulate

# # Set the port and baudrate for the serial communication
# port = 'COM8'  # Replace with your serial port
# baudrate = 230400  # Replace with your baudrate

# # Initialize the serial port
# serial_port = serial.Serial(port, baudrate=baudrate, timeout=1)

# # Initialize the data array with 6 empty arrays
# data = [[] for _ in range(6)]

# import matplotlib.pyplot as plt

# def update_plot(frame):
#     try:
#         line = serial_port.readline().decode().strip()
#         if line:
#             sensor, value = line.split(':')
#             print(f"Raw data received on port {port}: {line}", end='\n')
#             print(f"Decoded data: {sensor}: {value}", end='\n')

#         # table_data = []
#         # for i in range(len(data)):
#         #     if data[i]:  # Check if data[i] is not empty before accessing data[i][-1]
#         #         table_data.append([data[i][-1], f"Sensor {i+1}"])  # Transpose the data for plotting

#         # print(table_data)
#         # table = tabulate(table_data, headers=["Value", "Sensor"], tablefmt="grid")
#         # print(table, end='\n')

#         # Update the plot
#         ax.clear()  # Clear the previous plot
#         for i, d in enumerate(data):
#             if d:
#                 ax.plot(d, label=f"Sensor {i+1}")
#                 ax.set_ylabel('Value', color='black')  # Set the label color to black
#                 ax.tick_params(axis='y', colors='black')  # Set the tick color to black
#         ax.set_xlabel('Time')
#         ax.set_title('Sensor Data')
#         ax.legend()
#         fig.tight_layout()

#     except ValueError as e:
#         print(f"Invalid data received on port {port}: {e}", end='\n')

# # Create an empty figure and axis
# fig, ax = plt.subplots(figsize=(10, 6), dpi=150)  # Adjust the figsize and dpi values as needed

# # Create an animation object
# ani = animation.FuncAnimation(fig, update_plot, interval=1, repeat=True)

# # Show the plot
# plt.show()
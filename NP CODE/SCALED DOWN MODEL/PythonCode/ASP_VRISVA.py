### IMPORTING ALL THE LIBRARIES AND PACKAGES###
import math
import time
import socket
import threading
import numpy as np
import configparser
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import socket
###--###

### GUI RELATED FUNCTIONS ###
# Function to handle slider value changes
def module_frame_creation(frame_text, title_frame_width, title_frame_length, frame_width, frame_length, x_pos, y_pos):
    """
    Create a module frame with a heading and a content frame.

    Parameters:
    frame_text (str): The text to be displayed in the frame heading.
    title_frame_width (int): The width of the frame heading.
    title_frame_length (int): The length of the frame heading.
    frame_width (int): The width of the content frame.
    frame_length (int): The length of the content frame.
    x_pos (int): The x-coordinate of the frame's position.
    y_pos (int): The y-coordinate of the frame's position.
    """
    global root, font_colour

    frame_heading = tk.Frame(root, width=title_frame_width, height=title_frame_length, bg="#EBEBEB")
    frame_heading.pack()
    frame_heading.place(x=x_pos, y=y_pos)
    label = ttk.Label(root, text=frame_text, font=text_font2, foreground=font_colour, background="#EBEBEB")
    label.place(x=x_pos+10, y=y_pos+5)
    frame = tk.Frame(root, width=frame_width, height=frame_length, bg="#EBEBEB")
    frame.pack()
    frame.place(x=x_pos, y=y_pos+30)

def slider_module_creation(slider_label, command_function,text_from, text_to, x_pos, y_pos):
    """
    Creates a slider module in the GUI.

    Parameters:
    slider_label (str): The label for the slider.
    command_function (function): The function to be called when the slider is reset.
    text_from (str): The text to display on the left side of the slider.
    text_to (str): The text to display on the right side of the slider.
    x_pos (int): The x-coordinate of the slider module.
    y_pos (int): The y-coordinate of the slider module.
    """
    global text_font2, slider_length, reset_icon, font_colour, root

    pitch_label = ttk.Label(root, text= slider_label, font=text_font2, foreground=font_colour, background= "#EBEBEB")
    pitch_label.place(x= x_pos, y= y_pos)
    pitch_slider_reset = tk.Button(root, image=reset_icon, bd=0, bg="#EBEBEB", command=command_function)
    pitch_slider_reset.pack()
    pitch_slider_reset.place(x=x_pos+475, y=y_pos)
    pitch_label = ttk.Label(root, text= text_from, font=text_font2, foreground=font_colour, background="#EBEBEB")
    pitch_label.place(x=x_pos+178, y=y_pos+2)
    pitch_label = ttk.Label(root, text= text_to, font=text_font2, foreground=font_colour, background="#EBEBEB")
    pitch_label.place(x=x_pos+443, y=y_pos+2)

def sine_slider_module_creation(slider_label, command_function,text_from, text_to, x_pos, y_pos):
    """
    Create a sine slider module.

    Args:
        slider_label (str): The label for the slider.
        command_function (function): The function to be called when the reset button is clicked.
        x_pos (int): The x-coordinate of the module's position.
        y_pos (int): The y-coordinate of the module's position.
    """
    global text_font2, slider_length, reset_icon, font_colour, root

    pitch_label = ttk.Label(root, text=slider_label, font=text_font2, foreground=font_colour, background="#EBEBEB")
    pitch_label.place(x=x_pos, y=y_pos)
    pitch_slider_reset = tk.Button(root, image=reset_icon, bd=0, bg="#EBEBEB", command=command_function)
    pitch_slider_reset.pack()
    pitch_slider_reset.place(x=x_pos + 240, y=y_pos + 28)
    pitch_label = ttk.Label(root, text= text_from, font=text_font2, foreground=font_colour, background="#EBEBEB")
    pitch_label.place(x=x_pos, y=y_pos+50)
    pitch_label = ttk.Label(root, text= text_to, font=text_font2, foreground=font_colour, background="#EBEBEB")
    pitch_label.place(x=x_pos+213, y=y_pos+50)

def button_creation(button_text, command_function, button_width, button_height, bg_colour, fg_colour, x_pos, y_pos):
    """
    Create a button with the specified properties and place it on the GUI.

    Parameters:
    button_text (str): The text to be displayed on the button.
    command_function (function): The function to be executed when the button is clicked.
    button_width (int): The width of the button.
    button_height (int): The height of the button.
    bg_colour (str): The background color of the button.
    fg_colour (str): The foreground color (text color) of the button.
    x_pos (int): The x-coordinate of the button's position.
    y_pos (int): The y-coordinate of the button's position.
    """
    global text_font, root
    button = tk.Button(root, text=button_text, command=command_function, width=button_width, height=button_height, bg=bg_colour, fg=fg_colour, bd=0, padx=2, pady=2, font=text_font) 
    button.place(x=x_pos, y=y_pos)  # Place the button below the sliders

def button_with_frame_creation(button_text, command_function, button_width, button_height, bg_colour, fg_colour, frame_colour, x_pos, y_pos):
    """
    Create a button with a frame.

    Args:
        button_text (str): The text to be displayed on the button.
        command_function (function): The function to be called when the button is clicked.
        button_width (int): The width of the button.
        button_height (int): The height of the button.
        bg_colour (str): The background color of the button.
        fg_colour (str): The foreground color of the button.
        frame_colour (str): The color of the frame surrounding the button.
        x_pos (int): The x-coordinate of the button's position.
        y_pos (int): The y-coordinate of the button's position.
    """
    global root, text_font
    button_frame = tk.Frame(root, highlightbackground=frame_colour, highlightthickness=2)
    button = tk.Button(button_frame, text=button_text, command=command_function, width=button_width, height=button_height, bg=bg_colour, fg=fg_colour, bd=0, padx=2, pady=2, font=text_font) 
    button.pack()
    button_frame.pack()
    button_frame.place(x=x_pos, y=y_pos)

def slider_changed(event):
    """
    Function to handle the event when a slider is changed.
    It calls the update_slider_values function to update the slider values.
    """
    update_slider_values()

def display_output(output):
    """
    Update the label with the output.

    This function updates the status section with the argument whenever it is called.

    Parameters:
    output (str): The output to be displayed on the label.
    """
    output_label.config(text=output)

# Function to update slider values and display either integer or float values
def update_slider_values():
    """
    Update the slider values and labels with integer values.
    """
    # Get integer values from sliders
    pitch_int = round(pitch_slider.get())
    yaw_int = round(yaw_slider.get())
    roll_int = round(roll_slider.get())
    heave_int = round(heave_slider.get())
    sway_int = round(sway_slider.get())
    surge_int = round(surge_slider.get())
    #frequency_float = float(frequency_slider.get())
    amplitude_int = round(amplitude_slider.get())
    amplitude_vib_int = round(amplitude_vib_slider.get())
    intensity_vib_int = round(intensity_vib_slider.get())
    
    # Update the labels with integer values
    pitch_value.set(pitch_int)
    yaw_value.set(yaw_int)
    roll_value.set(roll_int)
    heave_value.set(heave_int)
    sway_value.set(sway_int)
    surge_value.set(surge_int)
    #frequency_value.set(frequency_float)
    amplitude_value.set(amplitude_int)
    amplitude_vib_value.set(amplitude_vib_int)
    intensity_vib_value.set(intensity_vib_int)

def update_graph():
    """
    Update the graph with the latest positions of the base and platform joints.

    This function calculates the transformation matrix based on the current values of yaw, pitch, roll,
    heave, sway, and surge. It then applies the transformation matrix to the platform joints to obtain
    the transformed positions. The z-coordinate of the transformed positions is corrected by adding a
    constant value. The function plots the original positions of the base and platform joints, as well
    as the transformed positions, using different colors and connecting lines. It also labels the base
    and transformed platform joint points.

    Parameters:
    None

    Returns:
    None
    """
    global ax, fig, base_joints, platform_joints, platform_joints_corrected
    global yaw_current_value, pitch_current_value, roll_current_value, heave_current_value, sway_current_value, surge_current_value
    
    # Calculate rotation matrix
    rotation_matrix = euler_to_rotation_matrix(yaw_current_value, pitch_current_value, roll_current_value)

    # Create transformation matrix by adding translation components
    transformation_matrix = np.zeros((4, 4))
    transformation_matrix[:3, :3] = rotation_matrix
    transformation_matrix[0, 3] = surge_current_value
    transformation_matrix[1, 3] = sway_current_value
    transformation_matrix[2, 3] = heave_current_value
    transformation_matrix[3, 3] = 1

    # Calculate the position of platform joints with respect to base joints and correct for the z axis by adding it to the z coordinates
    platform_joints_transformed = np.dot(transformation_matrix, platform_joints.T).T
    platform_joints_transformed[0][2] += 240
    platform_joints_transformed[1][2] += 240
    platform_joints_transformed[2][2] += 240
    platform_joints_transformed[3][2] += 240
    platform_joints_transformed[4][2] += 240
    platform_joints_transformed[5][2] += 240
    
    ax.clear()

    # Set axis limits to ±500 on all axes
    ax.set_xlim([-200, 200])
    ax.set_ylim([-200, 200])
    ax.set_zlim([0, 400])

    # Plot original positions (x, y, z coordinates) with connecting blue lines
    ax.scatter(base_joints[:, 0], base_joints[:, 1], base_joints[:, 2], color='b', label='Base Joints')
    for i in range(len(base_joints)):
        ax.plot([base_joints[i, 0], base_joints[(i + 1) % len(base_joints), 0]],
                [base_joints[i, 1], base_joints[(i + 1) % len(base_joints), 1]],
                [base_joints[i, 2], base_joints[(i + 1) % len(base_joints), 2]], color='b')

    # Plot transformed positions (x, y, z coordinates) with connecting red lines
    ax.scatter(platform_joints_transformed[:, 0], platform_joints_transformed[:, 1], platform_joints_transformed[:, 2], color='r', label='Platform Joints (Transformed)')
    for i in range(len(platform_joints_transformed)):
        ax.plot([platform_joints_transformed[i, 0], platform_joints_transformed[(i + 1) % len(platform_joints_transformed), 0]],
                [platform_joints_transformed[i, 1], platform_joints_transformed[(i + 1) % len(platform_joints_transformed), 1]],
                [platform_joints_transformed[i, 2], platform_joints_transformed[(i + 1) % len(platform_joints_transformed), 2]], color='r')

    # Plot platform joint positions (x, y, z coordinates) with connecting green lines
    ax.scatter(platform_joints_corrected[:, 0], platform_joints_corrected[:, 1], platform_joints_corrected[:, 2], color='g', label='Platform Joints (Original)')
    for i in range(len(platform_joints_corrected)):
        ax.plot([platform_joints_corrected[i, 0], platform_joints_corrected[(i + 1) % len(platform_joints_corrected), 0]],
                [platform_joints_corrected[i, 1], platform_joints_corrected[(i + 1) % len(platform_joints_corrected), 1]],
                [platform_joints_corrected[i, 2], platform_joints_corrected[(i + 1) % len(platform_joints_corrected), 2]], color='g', alpha=0.3)

    # Plot base joint points (x, y, z coordinates) with connecting yellow lines
    ax.scatter(base_joints[:, 0], base_joints[:, 1], base_joints[:, 2], color='b')
    for i in range(len(base_joints)):
        ax.plot([base_joints[i, 0], platform_joints_corrected[i, 0]],
                [base_joints[i, 1], platform_joints_corrected[i, 1]],
                [base_joints[i, 2], platform_joints_corrected[i, 2]], color='cyan', alpha=0.3)

    # Plot transformed platform joint points (x, y, z coordinates) with connecting brown lines
    ax.scatter(platform_joints_transformed[:, 0], platform_joints_transformed[:, 1], platform_joints_transformed[:, 2], color='r')
    for i in range(len(platform_joints_transformed)):
        ax.plot([base_joints[i, 0], platform_joints_transformed[i, 0]],
                [base_joints[i, 1], platform_joints_transformed[i, 1]],
                [base_joints[i, 2], platform_joints_transformed[i, 2]], color='brown')

    # Label base joint points as B1, B2, B3, B4, B5, B6
    for i, base_point in enumerate(base_joints):
        ax.text(base_point[0], base_point[1], base_point[2], f'B{i+1}', color='b', fontsize=8)

    # Label transformed platform joint points as P1, P2, P3, P4, P5, P6
    for i, transformed_point in enumerate(platform_joints_transformed):
        ax.text(transformed_point[0], transformed_point[1], transformed_point[2], f'P{i+1}', color='r', fontsize=8)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Place the legend lable on the top left corner
    ax.legend(loc='upper left')
    ax.set_box_aspect([1, 1, 1])
    canvas.draw()
    canvas.flush_events()
    del platform_joints_transformed
######
    
### GUI BUTTON CLICK COMMAND FUNCTIONS ###
def pitch_reset_button_click():
    """
    Resets the pitch slider to 0.
    """
    global pitch_slider
    pitch_slider.set(0)

def yaw_reset_button_click():
    """
    Resets the yaw slider to 0.
    """
    global yaw_slider
    yaw_slider.set(0)

def roll_reset_button_click():
    """
    Resets the roll slider to 0.
    """
    global roll_slider
    roll_slider.set(0)

def heave_reset_button_click():
    """
    Resets the heave slider to 0.
    """
    global heave_slider
    heave_slider.set(0)

def sway_reset_button_click():
    global sway_slider
    """
    Resets the sway slider to 0.
    """
    sway_slider.set(0)

def surge_reset_button_click():
    """
    Resets the surge slider to 0.
    """
    global surge_slider
    surge_slider.set(0)

def amplitude_reset_button_click():
    """
    Resets the amplitude slider to 0.
    """
    global amplitude_slider
    amplitude_slider.set(0)

def frequency_reset_button_click():
    """
    Resets the frequency slider to 0.
    """
    global frequency_slider
    frequency_slider.set(0)

def amplitude_vib_reset_button_click():
    """
    Resets the vibration amplitude slider to 0.
    """
    global amplitude_vib_slider
    amplitude_vib_slider.set(0)

def intensity_vib_reset_button_click():
    """
    Resets the vibration intensity slider to 0.
    """
    global intensity_vib_slider
    intensity_vib_slider.set(0)

def reset_all_button_click():
    """
    Resets all the manual control sliders to zero.
    """
    global pitch_slider, roll_slider, yaw_slider, heave_slider, sway_slider, surge_slider
    pitch_slider.set(0)
    yaw_slider.set(0)
    roll_slider.set(0)
    heave_slider.set(0)
    sway_slider.set(0)
    surge_slider.set(0)

def calibration():
    """
    Perform calibration of the platform by sending the 'O' character to the microcontroller.
    This command raises the platform all the way up and then all the way down, setting those two extremes as the new lowest and highest positions.
    This step eliminates any inaccuracies in the platform's positioning.
    """
    global stop_flag, stop_sine_flag, kill_timer, limit
    if disable_flag == True:
        return
    stop_flag = True
    stop_sine_flag = True
    kill_timer = True
    limit = False
    send = 'O'
    command = 'Calibrate Platform'
    send_interface_command_input(send, command)
    display = "Platform is Calibrating Itself."
    display_output(display)



def calibrate_IMU():
    """
    This function calibrates the IMU by setting its current Euler angles as zero.
    It also updates global variables: stop_flag, stop_sine_flag, kill_timer, limit.
    If disable_flag is True, the function returns without performing any calibration.
    The function sends a command 'E' to the interface and displays the output.
    """
    global stop_flag, stop_sine_flag, kill_timer, limit
    stop_flag = True
    stop_sine_flag = True
    kill_timer = True
    limit = False
    if disable_flag == True:
        return
    send = 'E'
    command = 'Calibrate IMU'
    send_interface_command_input(send, command)
    display = "IMU Calibrated."
    display_output(display)

#This function stops the actuator at whatever position it is at until the enable button is clicked. no other command will move the platform until the enable button is clicked
def emergency_stop():
    """
    Stops any ongoing actions such as sine wave, random vibration, oacillation or basic movement of the platform.
    Sends appropriate commands to the microcontroller.
    Updates the status section with the appropriate status text.
    """
    global stop_flag, stop_sine_flag, limit, kill_timer, oscillation_flag, disable_flag
    
    stop_flag = True
    stop_sine_flag = True
    kill_timer = True
    
    if limit == True:
        #This command is sent only if the oscillation, random vibration is being performed
        send = 'E'
        command = 'Stop!'
        send_interface_command_input(send, command)
        return
    
    send = 'Q'
    command = 'Stop!'
    send_interface_command_input(send, command)
    
    if oscillation_flag == True:
        display = "Oscillatory Motion Stopped."
        display_output(display)
        oscillation_flag = False
    else:
        #The disable flag is set to True which disables all the buttons except the enable button
        disable_flag = True
        display = "Platform Movement and GUI Disabled."
        display_output(display)

#This function enables the platform and works only when the Stop! button has been pressed
def enable_button_click():
    """
    Enables the platform movement and GUI.

    This function sets the necessary flags to stop any ongoing actions such as sine wave or random vibration.
    It sends commands to the microcontroller to enable the platform movement and updates the status section with the appropriate text.
    """
    global stop_flag, stop_sine_flag, kill_timer, disable_flag, enable_all

    stop_flag = True
    stop_sine_flag = True
    kill_timer = True

    if enable_all == True:
        disable_flag = False
    
    if limit == True:
        #This command is sent only if the oscillation, random vibration was being performed before disabling the platform
        send = 'N'
        command = 'Enable'
        send_interface_command_input(send, command)
        return
    #The 'H' character is sent to the microcontroller which enables the platform movement
    send = 'H'
    command = 'Enable'
    send_interface_command_input(send, command)

    display = "Platform Movement and GUI Enabled."
    display_output(display)

def level_button_click():
    """
    Perform the leveling sequence in the platform.

    This function sets the necessary flags and values to initiate the leveling sequence in the platform.
    It updates the graph, stops any ongoing actions such as sine wave or random vibration, and sends the command to level the platform.
    After the function is called, the platform starts leveling itself.

    Parameters:
    None

    Returns:
    None
    """
    global stop_flag, stop_sine_flag, limit, kill_timer
    global yaw_current_value, pitch_current_value, roll_current_value, heave_current_value, sway_current_value, surge_current_value
    if disable_flag == True:
        return

    #The 5 DOF values are being set next. these will be used by the update platform to perform the inverse kinematics calculations.
    #Here, heave is not changed here.
    yaw_current_value = 0
    pitch_current_value = 0
    roll_current_value = 0
    sway_current_value = 0
    surge_current_value = 0
    #The graph and print flag are asssigned for the update platform arguements
    #These flags determine weather the update platfoem should update the graph and send the movement 
    #signal to the platform or not. Here the platform will not be moved, only the graph will be updated.
    print_flag = False
    graph_flag = True
    #The stop flags are made True which stops any actions such as sine wave or random vibration if they are currently being executed
    #It is just a precautionary measure
    stop_flag = True
    stop_sine_flag = True
    kill_timer = True
    #The 'S' character is sent only if the vibration is being executed. This first stops the vibration before sending the level command
    if limit == True:
        send = 'S'
        command = ' '
        send_interface_command_input(send, command)
    limit = False
    #The 'I' character initiates the leveling sequence in the platform. The microcontroller performs the leveling calculations on itself. only the command has to be sent
    send = 'I'
    command = 'Level Platform'
    send_interface_command_input(send, command)
    #The status section is updated after the function is called with the appropriate status text
    display = "Platform is leveling itself now."
    display_output(display)
    #Finally the update_platform is called
    update_platform(graph_flag, print_flag)

def exit_button_click():
    """
    Function to handle the click event of the exit button.
    Stops any ongoing actions such as sine wave or random vibration.
    Sends a command to the interface to stop the vibration if it is running.
    Sends the 'S' character to the microcontroller after which it executes the exit command and brings the platform to its base position
    Closes the GUI window.
    """
    global stop_flag, stop_sine_flag, limit, kill_timer
    stop_flag = True
    stop_sine_flag = True
    kill_timer = True
    if limit == True:
        #This command is sent only if the oscillation, random vibration is being performed
        send = 'S'
        command = 'Exit App'
        send_interface_command_input(send, command)
    limit = False
    root.destroy()

#This function brings the platfom to its base positon
def base_position_button_click():
    """
    Moves the platform to its base position by sending commands to the microcontroller.
    Stops any ongoing actions such as sine wave or random vibration.
    Updates the platform's 6 DOF values and calls the update_platform function.
    """
    global yaw_current_value, pitch_current_value, roll_current_value, heave_current_value, sway_current_value, surge_current_value, limit
    global stop_sine_flag, stop_flag, kill_timer
    if disable_flag == True:
        return

    #The stop flags are made True which stops any actions such as sine wave or random vibration if they are currently being executed
    #It is just a precautionary measure
    stop_sine_flag = True
    stop_flag = True
    kill_timer = True
    #The 'S' character is sent only if the vibration is being executed. This first stops the vibration if it is running before sending the platform to base position.
    if limit == True:
        send = 'S'
        command = ' '
        send_interface_command_input(send, command)
    #The 'F' character is sent to the microcontroller which brings back to its base position
    send = 'F'
    command = 'Base Position'
    send_interface_command_input(send, command)
    limit = False
    #The graph and print flag are asssigned for the update platform arguements
    #These flags determine weather the update platfoem should update the graph and send the movement 
    #signal to the platform or not. Here the platform will not be moved, only the graph will be updated.
    graph_flag = True
    print_flag = False
    #The 6 DOF values are being set next. these will be used by the update platform to perform the inverse kinematics calculations.
    #Here, heave is set to -300 which indicates that the platform is being set to the base position.
    yaw_current_value = 0
    pitch_current_value = 0
    roll_current_value = 0
    heave_current_value = 0
    sway_current_value = 0
    surge_current_value = 0
    #The status section is updated after the function is called with the appropriate status text
    display = "Going To Base Position."
    display_output(display)
    #Finally the update_platform is called
    update_platform(graph_flag, print_flag)

def home_position_button_click():
    """
    Function to move the platform to the home position.
    This function sets the 6 DOF values to 0, indicating that the platform is being set to the home position.
    It also updates the graph and sends the movement signal to the platform.
    """
    global yaw_current_value, pitch_current_value, roll_current_value, heave_current_value, sway_current_value, surge_current_value, limit
    global stop_sine_flag, stop_flag, kill_timer
    if disable_flag == True:
        return

    stop_sine_flag = True
    stop_flag = True
    kill_timer = True
    if limit == True:
        send = 'S'
        command = ' '
        send_interface_command_input(send, command)
    limit = False

    graph_flag = True
    print_flag = True

    yaw_current_value = 0
    pitch_current_value = 0
    roll_current_value = 0
    heave_current_value = 25
    sway_current_value = 0
    surge_current_value = 0

    display = "Going To Home Position."
    display_output(display)

    update_platform(graph_flag, print_flag)

# Function to handle button click event
def update_button_click():
    """
    Function to handle the click event of the update button.
    This function updates the platform position based on the current slider values.
    It also stops any ongoing actions such as sine wave or random vibration.
    """
    global yaw_current_value, pitch_current_value, roll_current_value, heave_current_value, sway_current_value, surge_current_value
    global stop_sine_flag, stop_flag, limit, kill_timer
    if disable_flag == True:
        return

    #The stop flags are made True which stops any actions such as sine wave or random vibration if they are currently being executed
    #It is just a precautionary measure
    stop_sine_flag = True
    stop_flag = True
    kill_timer = True
    #The graph and print flag are asssigned for the update platform arguements
    #These flags determine weather the update platfoem should update the graph and send the movement 
    #signal to the platform or not. here, both are true which means that the platform will be moved and accordingly the graph will be updated.
    graph_flag = True
    print_flag = True
    if limit == True:
        send = 'S'
        command = ' '
        send_interface_command_input(send, command)
    limit = False
    # Get current values of sliders
    yaw_current_value = int(yaw_slider.get())
    pitch_current_value = int(pitch_slider.get())
    roll_current_value = int(roll_slider.get())
    heave_current_value = int(heave_slider.get())
    sway_current_value = int(sway_slider.get())
    surge_current_value = int(surge_slider.get())

    #The status section is updated after the function is called with the appropriate status text
    display = "Updating Platform Position."
    display_output(display)

    # Update_platform function is called
    update_platform(graph_flag, print_flag)

def set_start_button_click():
    """
    Sets the starting position of the platform for the cyclic motion.

    This function takes the current actuator lengths and assigns them as the starting position of the platform for the cyclic motion.
    The 'J' character is sent to the microcontroller, indicating that the next inputs will be treated as the starting position.
    The starting position is then sent to the microcontroller via a socket connection.
    The function also updates the status section with the appropriate status text.
    """
    global start_pos
    if disable_flag == True:
        return

    start_pos = []
    start_pos = int_actuator_lengths
    send = 'J'
    command = 'Start Pos'
    send_interface_command_input(send, command)
    time.sleep(0.3)
    output = ' '.join(map(str, start_pos))
    #s.sendall(output.encode())
    print(f"Starting position sent: {output}")
    display = "Starting position sent."
    display_output(display)

def set_end_button_click():
    """
    Sets the ending position of the platform for cyclic motion.

    This function takes the current actuator lengths and assigns them as the ending position of the platform for the cyclic motion.
    The 'K' character is sent to the microcontroller, indicating that the next inputs will be considered as the ending position.
    The status section is updated with the appropriate status text.
    """
    global end_pos
    if disable_flag == True:
        return

    end_pos = []
    end_pos = int_actuator_lengths
    send = 'K'
    command = 'End Pos'
    send_interface_command_input(send, command)
    time.sleep(0.3)
    output = ' '.join(map(str, end_pos))
    #s.sendall(output.encode())
    print(f"Ending position sent: {output}")
    display = "Ending position sent."
    display_output(display)

def oscilate_button_click():
    """
    Starts the oscillatory motion.

    This function initiates the oscillatory motion by sending a command to the interface.
    the 'L' character is sent to the microcontroller which starts the oscillatory motion.
    It also starts a countdown timer in a separate thread.

    """
    global oscillation_flag, kill_timer

    if disable_flag == True:
        return
    
    kill_timer = False
    oscillation_flag = True
    send = 'L'
    command = 'Oscilate'
    send_interface_command_input(send, command)
    display = "Oscillatory Movement Initiated."
    display_output(display)
    threading.Thread(target=countdown_timer).start()

def stop_random_vibration():
    """
    Stops the random vibration if it is currently being performed.

    This function sets the 'limit' variable to False and the 'kill_timer' variable to True,
    indicating that the random vibration should be stopped. It also sends the 'S' command
    to the appropriate destination using the 's' socket object. After stopping the random
    vibration, it updates the status section with the appropriate status text.
    """
    global limit, kill_timer
    if disable_flag == True:
        return
    limit = False
    kill_timer = True
    send = 'S'
    output = ' '.join(map(str, send))
    #s.sendall(output.encode())
    display = "Random Vibration Stopped."
    display_output(display)

def start_sine_wave():
    """
    Starts the sine wave motion in the platform by calling the update_sine_wave function in a separate thread.
    If the disable_flag is True, the function returns without starting the sine wave.
    If the limit is False, it starts the update_sine_wave function and a countdown_timer function in separate threads.
    The display is updated with the status text "Sine Wave Started."
    """
    global stop_sine_flag, limit, kill_timer
    if disable_flag == True:
        return
    stop_sine_flag= False
    kill_timer = False
    if limit == False:
        threading.Thread(target=update_sine_wave).start()
        threading.Thread(target=countdown_timer).start()
    display = "Sine Wave Started."
    display_output(display)
    limit = True

def stop_sine_wave():
    """
    Stops the execution of the sine wave if it is currently being executed.
    Updates the status section with the appropriate status text.
    """
    if disable_flag == True:
        return

    global stop_sine_flag, int_actuator_lengths, limit, kill_timer
    global yaw_current_value, pitch_current_value, roll_current_value, heave_current_value, sway_current_value, surge_current_value
    #The stop flags are made True which stops the sine wave if it is currently being executed
    stop_sine_flag = True
    #The status section is updated after the function is called with the appropriate status text
    display = "Sine Wave Stopped."
    display_output(display)
    limit = False
    kill_timer = True

def start_random_vibration():
    """
    Starts the random vibration process based on the selected vibration mode and slider values.

    The function sets the vibration mode based on the toggle count, where:
    - toggle_count = 1: ALL
    - toggle_count = 2: YAW
    - toggle_count = 3: PITCH
    - toggle_count = 4: ROLL

    The current slider values of amplitude and intensity of vibration are taken from the sliders.
    The amplitude and intensity values are then sent to the microcontroller.
    The vibration mode is also sent to the microcontroller.
    The status section is updated with the appropriate status text.
    A countdown timer is started in a separate thread.

    Note: The function will not start the vibration process if the disable_flag is True.
    """
    global limit, kill_timer, vibration_mode, toggle_count
    kill_timer = False
    if disable_flag == True:
        return

    if toggle_count == 1:
        # ALL
        vibration_mode = 10
    elif toggle_count == 2:
        # YAW
        vibration_mode = 20
    elif toggle_count == 3:
        # PITCH
        vibration_mode = 30
    elif toggle_count == 4:
        # ROLL
        vibration_mode = 40

    # the current slider values of amplitude and intensity of vibration are taken from the sliders
    amplitude_vib_current_value = int(amplitude_vib_slider.get())
    intensity_vib_current_value = int(intensity_vib_slider.get())
    # the amplitude and intensity are sent accordingly to the microcontroller
    if limit == False:
        send1 = 'W'
        update1 = amplitude_vib_current_value
        send_vib_user_input(send1, update1)
        send2 = 'R'
        update2 = intensity_vib_current_value
        send_vib_user_input(send2, update2)
        send3 = 'Y'
        update3 = vibration_mode
        send_vib_user_input(send3, update3)
        # The status section is updated after the function is called with the appropriate status text
        display = "Random Vibration Started."
        display_output(display)
        threading.Thread(target=countdown_timer).start()
    limit = True

def set_vibration_mode():
    """
    Sets the vibration mode based on the toggle count.

    The toggle count is incremented by 1 each time this function is called.
    If the toggle count exceeds 4, it is reset to 1.

    The vibration mode label is updated based on the toggle count:
    - 1: "All"
    - 2: "Yaw"
    - 3: "Pitch"
    - 4: "Roll"
    """
    global toggle_count
    toggle_count = toggle_count + 1
    if toggle_count > 4:
        toggle_count = 1

    if toggle_count == 1:
        vibration_mode_label.config(text="All")
    elif toggle_count == 2:
        vibration_mode_label.config(text="Yaw")
    elif toggle_count == 3:
        vibration_mode_label.config(text="Pitch")
    elif toggle_count == 4:
        vibration_mode_label.config(text="Roll")
######

### COMMAND FUNCTIONS TO THE PLATFORM ###

def send_user_input(update):
    """
    Sends user input to the microcontroller.

    Args:
        update (list): List of actuator lengths.

    Returns:
        None
    """
    #the 'A' character is sent to the microcontroller after which it waits for the actuator lengths to be sent
    send = 'A'
    #s.sendall(send.encode())
    time.sleep(0.3)
    # Get 6 actuators positions and construct the output string with positions and send the formatted output to Arduino
    output = ' '.join(map(str, update))
    #s.sendall(output.encode())
    print(f"Actuator lengths sent to Arduino: {output}")

def send_vib_user_input(send, update):
    """
    Sends user input to the microcontroller.

    Args:
        send (str): The input command to be sent.
        update (int): The corresponding value to be sent.

    Returns:
        None
    """
    # The send variable sends causes the microcontroller to wait for the next input which is the corresponding value
    #s.sendall(send.encode())
    # Now the value is sent 
    update = str(update)
    #s.sendall(update.encode())

def send_interface_command_input(send, command):
    """
    Sends the specified command to the interface.

    Args:
        send (str): The command to send.
        command (str): The name of the command.

    Returns:
        None
    """
    #s.sendall(send.encode())
    print(f"Command For {command}: {send}")
######

### CALCULATION FUNCTIONS ###
#This function calculates the rotation matrix for the inverse kinematics
def euler_to_rotation_matrix(yaw, pitch, roll):
    """
    Converts Euler angles (yaw, pitch, roll) to a rotation matrix.

    Parameters:
    - yaw (float): Yaw angle in degrees.
    - pitch (float): Pitch angle in degrees.
    - roll (float): Roll angle in degrees.

    Returns:
    - rotation_matrix (numpy.ndarray): 3x3 rotation matrix.
    """
    rotation_matrix = []
    # Convert angles from degrees to radians
    yaw_rad = np.radians(yaw)
    pitch_rad = np.radians(pitch)
    roll_rad = np.radians(roll)

    # Calculate rotation matrix
    yaw_matrix = np.array([[np.cos(yaw_rad), -np.sin(yaw_rad), 0],
                        [np.sin(yaw_rad), np.cos(yaw_rad), 0],
                        [0, 0, 1]])

    pitch_matrix = np.array([[np.cos(pitch_rad), 0, np.sin(pitch_rad)],
                            [0, 1, 0],
                            [-np.sin(pitch_rad), 0, np.cos(pitch_rad)]])

    roll_matrix = np.array([[1, 0, 0],
                            [0, np.cos(roll_rad), -np.sin(roll_rad)],
                            [0, np.sin(roll_rad), np.cos(roll_rad)]])
    
    # Combine rotation matrices
    rotation_matrix = np.dot(yaw_matrix, np.dot(pitch_matrix, roll_matrix))
    return rotation_matrix

#This function starts a continuous while loop which keeps sending the actuator lengths to the platform which intern induces a sine wave in it
def update_sine_wave():
    """
    Updates the sine wave motion of the platform based on the current amplitude value.
    The platform is moved using a sine wave motion.
    """
    global yaw_current_value, pitch_current_value, roll_current_value, heave_current_value, sway_current_value, surge_current_value, stop_flag, root
    if disable_flag == True:
        return

    #frequency_current_value = float(frequency_slider.get())
    amplitude_current_value = int(amplitude_slider.get())
    frequency_current_value = np.interp(amplitude_current_value, (0, 25), (1.8, 0.2))
    sleep_time = np.interp(amplitude_current_value, (0, 25), (1, 3))
    timestamp = 0
    #The graph and print flag are asssigned for the update platform arguements
    #These flags determine weather the update platfoem should update the graph and send the movement 
    #signal to the platform or not. Here the platform will be moved, and the graph will not be updated.
    graph_flag = False  
    print_flag = True
    while not stop_sine_flag:
        # Define sine wave properties
        frequency = frequency_current_value  # Hz
        amplitude = amplitude_current_value    # Units
        phase_difference1 = 0  # Degrees
        phase_difference2 = math.pi/2
        
        # Calculate new actuator lengths using a sine wave
        pitch_current_value = amplitude * np.sin(2 * np.pi * frequency * timestamp + phase_difference1)
        roll_current_value = amplitude * np.sin(2 * np.pi * frequency * timestamp + phase_difference2)
        timestamp+=0.1
        # Update GUI and graph
        update_platform(graph_flag, print_flag)
        time.sleep(sleep_time)
        del pitch_current_value
        del roll_current_value
        pitch_current_value = 0
        roll_current_value = 0

# this function updates the platform position. it performs the necessary inverse kinematics 
def update_platform(graph_flag, print_flag):
    """
    Updates the platform based on the input angles and sends the input to a microcontroller.
    This function is the heart of the code. It performs the inverse kinematics calculations and sends the input to the microcontroller.

    Args:
        graph_flag (bool): Flag indicating whether to update the graph in the GUI.
        print_flag (bool): Flag indicating whether to send the input to the microcontroller.

    Returns:
        None
    """
    global yaw_current_value, pitch_current_value, roll_current_value, heave_current_value, sway_current_value, surge_current_value, int_actuator_lengths
    if disable_flag == True:
        return
    
    # Taking inputs for yaw, pitch, roll, heave, sway, and surge angles
    pitch = pitch_current_value
    yaw = yaw_current_value
    roll = roll_current_value
    heave = heave_current_value
    sway = sway_current_value
    surge = surge_current_value

    # Calculate rotation matrix
    rotation_matrix = euler_to_rotation_matrix(yaw, pitch, roll)

    # Create transformation matrix by adding translation components
    transformation_matrix = np.zeros((4, 4))
    transformation_matrix[:3, :3] = rotation_matrix
    transformation_matrix[0, 3] = surge
    transformation_matrix[1, 3] = sway
    transformation_matrix[2, 3] = heave
    transformation_matrix[3, 3] = 1

    # Calculate the position of platform joints with respect to base joints and correct for the z axis by adding it to the z coordinates
    platform_joints_transformed = np.dot(transformation_matrix, platform_joints.T).T
    platform_joints_transformed[0][2] += 240
    platform_joints_transformed[1][2] += 240
    platform_joints_transformed[2][2] += 240
    platform_joints_transformed[3][2] += 240
    platform_joints_transformed[4][2] += 240
    platform_joints_transformed[5][2] += 240

    #print(platform_joints_transformed)
    # Calculate the actuators' lengths using the formula L = sqrt(x^2 + y^2 + z^2)
    actuator_lengths = np.sqrt(np.sum(np.square(platform_joints_transformed[:, :3] - base_joints[:, :3]), axis=1))

    # Take the absolute values of all actuator lengths
    actuator_lengths -= (240)
    actuator_lengths = np.interp(actuator_lengths, [12, 60], [0, 50])

    actuator_lengths = np.abs(actuator_lengths)
    int_actuator_lengths = [int(round(x)) for x in actuator_lengths]
    int_actuator_lengths = np.round (int_actuator_lengths)

    # Send input to microcontroller
    if (print_flag == True):
        send_user_input(int_actuator_lengths)
    # Update the graph in the GUI
    if (graph_flag == True):
        update_graph()
    del actuator_lengths
    del transformation_matrix
    del rotation_matrix

def countdown_timer():
    """
    Performs a countdown timer operation and initiates a cooldown sequence.

    This function starts a countdown timer for a specified time period and then initiates a cooldown sequence.
    The countdown timer displays the remaining time in minutes and seconds.
    The cooldown sequence displays the remaining time in minutes and seconds until completion.

    Global Variables:
    - stop_sine_flag: A flag indicating whether to stop a sine wave operation.
    - disable_flag: A flag indicating whether to disable certain functionality.
    - enable_all: A flag indicating whether to enable all functionality.
    """
    global stop_sine_flag, disable_flag, enable_all
    time_allowed = 300
    cooldown_time = 900
    while (time_allowed > 0):
        if kill_timer == True:
            return
        if time_allowed <= 180:
            for i in range(time_allowed, 0, -1):
                sec = i%60
                min = i/60
                min = int(min)
                display = f"Operation Time Remaining: {min}:{sec}"
                display_output(display)
                time.sleep(1)
                if kill_timer == True:
                    return
            break
        time.sleep(1)
        time_allowed = time_allowed - 1
    display = "Cooldown Sequence Initiated."
    display_output(display)

    if stop_sine_flag == False:
        stop_sine_flag = True

    disable_flag = True
    enable_all = False
    while (cooldown_time > 0):
        if cooldown_time <= 895:
            for i in range(cooldown_time, 0, -1):
                sec = i%60
                min = i/60
                min = int(min)
                display = f"Cooldown Sequence Timer: {min}:{sec}"
                display_output(display)
                time.sleep(1)
            break
        time.sleep(1)
        cooldown_time = cooldown_time - 1
    disable_flag = False
    enable_all = True
    display = "Cooldown sequence complete."
    display_output(display)
######

### START AND STOP FUNCTIONS ###
#This function is called when the GUI is opened, it does not move the platform.
#This function sends a command to the microcontroller after which it opens the ethernet communication.
#This function also updates the fraph and sends it to the base position.
def startup():
    """
    Initializes the global variables and flags for the platform control.

    This function sets the initial values for the 6 degrees of freedom (DOF) variables
    and flags used for controlling the platform. It also stops any ongoing actions
    such as sine wave or random vibration. The update platform function is then called
    to perform inverse kinematics calculations and update the platform accordingly.
    """
    global yaw_current_value, pitch_current_value, roll_current_value, heave_current_value, sway_current_value, surge_current_value, limit
    global stop_sine_flag, stop_flag

    stop_sine_flag = True
    stop_flag = True
    kill_timer == True
    limit = False

    graph_flag = True
    print_flag = False

    yaw_current_value = 0
    pitch_current_value = 0
    roll_current_value = 0
    heave_current_value = 0
    sway_current_value = 0
    surge_current_value = 0

    update_platform(graph_flag, print_flag)
    calibrate_IMU()

#This function is called after the GUI is closed and it also brings the platform to the base position
def close_application_click():
    """
    Function to handle the close application button click event.
    Stops any ongoing actions such as sine wave or random vibration.
    Sends commands to the microcontroller to bring it back to its base position.
    """
    global stop_flag, stop_sine_flag, limit
    stop_flag = True
    stop_sine_flag = True
    kill_timer == True
    if limit == True:
        send = 'S'
        command = ' '
        send_interface_command_input(send, command)
    limit = False
    send = 'F'
    command = 'Closing Sequence'
    send_interface_command_input(send, command)
######


# #setting the IP and port variables
# ip = "192.168.137.177"
# port = 80

# # Create a socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     # Connect to Arduino
#     s.connect((ip, port))

# except socket.error as e:
#     print(f"Error: {e}")

# Define base joint coordinates (B1 to B6)
base_joints = np.array([[180, -65, 0, 1],
                        [-34, -188, 0, 1],
                        [-146, -123, 0, 1],
                        [-146, 123, 0, 1],
                        [-34, 188, 0, 1],
                        [180, 65, 0, 1]])

# Define platform joint coordinates with respect to platform coordinate system (P1 to P6)
platform_joints = np.array([[108, -95, 0, 1],
                            [28, -141, 0, 1],
                            [-137, -46, 0, 1],
                            [-137, 46, 0, 1],
                            [28, 141, 0, 1],
                            [108, 95, 0, 1]])

# Define platform joint coordinates with respect to the base coordinate system (P1 to P6)
platform_joints_corrected = np.array([[108, -95, 240, 1],
                                      [28, -141, 240, 1],
                                      [-137, -46, 240, 1],
                                      [-137, 46, 240, 1],
                                      [28, 141, 240, 1],
                                      [108, 95, 240, 1]])

# Variables to store the current values of sliders
yaw_current_value           = 0
pitch_current_value         = 0
roll_current_value          = 0
heave_current_value         = 0
sway_current_value          = 0
surge_current_value         = 0
frequency_current_value     = 0
amplitude_current_value     = 0
amplitude_vib_current_value = 0
intensity_vib_current_value = 0
vibration_mode              = 0
toggle_count                = 0

stop_sine_flag   = False
stop_flag        = False
limit            = False
kill_timer       = False
disable_flag     = False
oscillation_flag = False
enable_all       = False

pitch_max = 25
pitch_min = -25
yaw_max = 25
yaw_min = -25
roll_max = 25
roll_min = -25
heave_max = 300
heave_min = -300
sway_max = 200
sway_min = -200
surge_max = 200
surge_min = -200
# pitch_max = 10
# pitch_min = -10
# yaw_max = 10
# yaw_min = -10
# roll_max = 10
# roll_min = -10
# heave_max = 50
# heave_min = 0
# sway_max = 25
# sway_min = -25
# surge_max = 25
# surge_min = -25
amplitude_max = 0
amplitude_min = 25
frequency_max = 0
frequency_min = 2
amplitude_vib_max = 0
amplitude_vib_min = 25
intensity_vib_max = 0
intensity_vib_min = 10

# Create main window
root = tk.Tk()
root.title("Adbuta Stewart Platform")
root.geometry("1440x900")  # Set window size
root.resizable(width=False, height=False)
root.configure(bg="#f9f9f9")
style = ttk.Style()
style.theme_use("clam")

#defining all the different fonts and text sizes
text_font     = ("Helvetica", 11, "bold")
text_font2    = ("Helvetica", 10, "bold")
text_font3    = ("Helvetica", 12, "bold")
text_font4    = ("Helvetica", 14, "bold")
heading_font1 = ("Helvetica", 16, "bold")
heading_font2 = ("Helvetica", 15, "italic")
heading_font3 = ("Helvetica", 15)
font_colour   = "#00184B"

# These are the X and Y coordinates of all the modules on the GUI. changing these values wil change the position of these modules
manual_controle_module_x = 40
manual_controle_module_y = 150
sine_module_x            = 580
sine_module_y            = 150
vibration_module_x       = 40
vibration_module_y       = 600
presets_module_x         = 580
presets_module_y         = 400
other_buttons_x          = 900
other_buttons_y          = 740
status_module_x          = 900
status_module_y          = 150
graph_x                  = 900
graph_y                  = 210

# Create sliders and labels with specified value ranges
slider_length = 230

# Load the logo image
logo_image = PhotoImage(file="E:\\Vrisva Space\\Documents\\GitHub\\Nidhi_prayas_small_model_code\\NP CODE\\SCALED DOWN MODEL\\PythonCode\\icons\\icon1.png")
logo_image = logo_image.subsample(7, 7)

#icon for reset sliders
reset_icon1 = PhotoImage(file="E:\\Vrisva Space\\Documents\\GitHub\\Nidhi_prayas_small_model_code\\NP CODE\\SCALED DOWN MODEL\\PythonCode\\icons\\reset_icon.png")
reset_icon = reset_icon1.subsample(5,5)
reset_all_icon = reset_icon1.subsample(3,3)

# Create a label to display the image
logo_label = tk.Label(root, image=logo_image)
logo_label.pack(padx=10, pady=10)
logo_label.place(x=40, y=10)
title_label1 = ttk.Label(root, text="Adbuta", font=heading_font1, background= "#f9f9f9", foreground= font_colour)
title_label1.place(x=210, y=45)
title_label2 = ttk.Label(root, text="Stewart Platform", font=heading_font1, background= "#f9f9f9", foreground= font_colour)
title_label2.place(x=165, y=70)
title_label3 = ttk.Label(root, text="3-Axis Dynamic Motion Stand", font=heading_font3, background= "#f9f9f9", foreground= font_colour)
title_label3.place(x=560, y=55)
title_label4 = ttk.Label(root, text="Adbuta Motion Interface V1.1", font=heading_font2, background= "#f9f9f9", foreground= font_colour)
title_label4.place(x=1145, y=55)

#heading line on top which separates the logo and headings with the contents of the GUI
heading_line = tk.Frame(root, width=1363, height=2, bg="#00184B")
heading_line.pack()
heading_line.place(x=40, y=133)

module_frame_creation("Manual Control", 120, 30, 510, 310, manual_controle_module_x, manual_controle_module_y)

# Pitch Slider
pitch_value = tk.StringVar()
pitch_display = ttk.Spinbox(root, textvariable= pitch_value, width = 5, from_=pitch_min, to=pitch_max)
pitch_display.place(x= manual_controle_module_x+110, y= manual_controle_module_y+45)
pitch_slider = ttk.Scale(root, from_= pitch_min, to= pitch_max, orient=tk.HORIZONTAL, command = slider_changed, length = slider_length, variable = pitch_value)
pitch_slider.place(x=manual_controle_module_x+220, y=manual_controle_module_y+50)
slider_module_creation("Pitch (x,deg):", pitch_reset_button_click, f"  {pitch_min}", f"{pitch_max}", manual_controle_module_x+10, manual_controle_module_y+45)

# Yaw Slider
yaw_value = tk.StringVar()
yaw_display = ttk.Spinbox(root, textvariable=yaw_value, width = 5, from_=yaw_min, to=yaw_max)
yaw_display.place(x=manual_controle_module_x+110, y=manual_controle_module_y+95)
yaw_slider = ttk.Scale(root, from_= yaw_min, to=yaw_max, orient=tk.HORIZONTAL, command=slider_changed, length=slider_length, variable= yaw_value)
yaw_slider.place(x=manual_controle_module_x+220, y=manual_controle_module_y+100)
slider_module_creation("Yaw (z,deg):", yaw_reset_button_click, f"  {yaw_min}", f"{yaw_max}", manual_controle_module_x+10, manual_controle_module_y+95)

# Roll Slider
roll_value = tk.StringVar()
roll_display = ttk.Spinbox(root, textvariable=roll_value, width = 5, from_=roll_min, to=roll_max)
roll_display.place(x=manual_controle_module_x+110, y=manual_controle_module_y+145)
roll_slider = ttk.Scale(root, from_=roll_min, to=roll_max, orient=tk.HORIZONTAL, command=slider_changed, length=slider_length, variable= roll_value)
roll_slider.place(x=manual_controle_module_x+220, y=manual_controle_module_y+150)
slider_module_creation("Roll (y,deg):", roll_reset_button_click, f"  {roll_min}", f"{roll_max}", manual_controle_module_x+10, manual_controle_module_y+145)

# Heave Slider
heave_value = tk.StringVar()
heave_display = ttk.Spinbox(root, textvariable=heave_value, width = 5, from_=heave_min, to=heave_max)
heave_display.place(x=manual_controle_module_x+110, y=manual_controle_module_y+195)
heave_slider = ttk.Scale(root, from_= heave_min, to= heave_max, orient=tk.HORIZONTAL, command=slider_changed, length=slider_length, variable= heave_value)
heave_slider.place(x=manual_controle_module_x+220, y=manual_controle_module_y+200)
slider_module_creation("Heave (z,mm):", heave_reset_button_click, f"{heave_min}", f"{heave_max}", manual_controle_module_x+10, manual_controle_module_y+195)

# Sway Slider
sway_value = tk.StringVar()
sway_display = ttk.Spinbox(root, textvariable=sway_value, width = 5, from_=sway_min, to=sway_max)
sway_display.place(x=manual_controle_module_x+110, y=manual_controle_module_y+245)
sway_slider = ttk.Scale(root, from_=sway_min, to=sway_max, orient=tk.HORIZONTAL, command=slider_changed, length=slider_length, variable= sway_value)
sway_slider.place(x=manual_controle_module_x+220, y=manual_controle_module_y+250)
slider_module_creation("Sway (x,mm):", sway_reset_button_click, f"{sway_min}", f"{sway_max}", manual_controle_module_x+10, manual_controle_module_y+245)

# Surge Slider
surge_value = tk.StringVar()
surge_display = ttk.Spinbox(root, textvariable=surge_value, width = 5, from_=surge_min, to=surge_max)
surge_display.place(x=manual_controle_module_x+110, y=manual_controle_module_y+295)
surge_slider = ttk.Scale(root, from_=surge_min, to=surge_max, orient=tk.HORIZONTAL, command=slider_changed, length=slider_length, variable= surge_value)
surge_slider.place(x=manual_controle_module_x+220, y=manual_controle_module_y+300)
slider_module_creation("Surge (y,mm):", surge_reset_button_click, f"{surge_min}", f"{surge_max}", manual_controle_module_x+10, manual_controle_module_y+295)     

# Button to update values (larger size)
button_creation("Update Position", update_button_click, 15, 2, "#2e8b57", "#FFFFFF", manual_controle_module_x, manual_controle_module_y+360)

# Button to update values (larger size)
button_creation("Start Pos", set_start_button_click, 8, 2, "#D9D9D9", "#000000", manual_controle_module_x+160, manual_controle_module_y+360)

# Button to update values (larger size)
button_creation("End Pos", set_end_button_click, 8, 2, "#D9D9D9", "#000000", manual_controle_module_x+260, manual_controle_module_y+360)

# Button to update values (larger size)
button_creation("Oscilate", oscilate_button_click, 8, 2, "#2e8b57", "#FFFFFF", manual_controle_module_x+360, manual_controle_module_y+360)

slider_reset_all = tk.Button(root, image=reset_all_icon, bd=0, bg="#f9f9f9", command=reset_all_button_click)
slider_reset_all.pack()
slider_reset_all.place(x=manual_controle_module_x+470, y=manual_controle_module_y+363)

# Create a Frame widget for the specific region
module_frame_creation("Sine Wave Generator", 160, 30, 290, 110, sine_module_x, sine_module_y)

# amplitude Slider
amplitude_value = tk.StringVar()
amplitude_display = ttk.Spinbox(root, textvariable=amplitude_value, width = 5, from_=amplitude_min, to=amplitude_max)
amplitude_display.place(x= sine_module_x + 140, y=sine_module_y + 55)
amplitude_slider = ttk.Scale(root, from_=amplitude_min, to=amplitude_max, orient=tk.HORIZONTAL, command=slider_changed, length=230, variable= amplitude_value)
amplitude_slider.place(x= sine_module_x + 20, y=sine_module_y + 90)
sine_slider_module_creation("Amplitude (deg):", amplitude_reset_button_click,f"{amplitude_min}",f"{amplitude_max}", sine_module_x + 20, sine_module_y + 57)

# Add Sine Wave button to the GUI
button_creation("Start Wave", start_sine_wave, 13, 2, "#2e8b57", "#FFFFFF", sine_module_x, sine_module_y+160)

# Add Stop button to the sine wave
button_creation("Stop Wave", stop_sine_wave, 13, 2, "#cd5c5c", "#FFFFFF", sine_module_x+165, sine_module_y+160)

# Create a Frame widget for the specific region
module_frame_creation("Presets", 70, 30, 290, 370, presets_module_x, presets_module_y)

# Home button to bring the platform to home position
button_with_frame_creation("Home Position", home_position_button_click, 15, 2, "#D9D9D9", "#000000", "#2e8b57", presets_module_x+70, presets_module_y+40)

# base position button to bring the platform to zero position
button_with_frame_creation("Base Position", base_position_button_click, 15, 2, "#D9D9D9", "#000000", "#2e8b57", presets_module_x+70, presets_module_y+110)

# button to level the platform
button_with_frame_creation("Level Platform", level_button_click, 15, 2, "#D9D9D9", "#000000", "#2e8b57", presets_module_x+70, presets_module_y+180)

# button to calibrate the platform
button_with_frame_creation("Calibrate Platform", calibration, 15, 2, "#D9D9D9", "#000000", "#2e8b57", presets_module_x+70, presets_module_y+250)

# button to calibrate the IMU sensor data
button_with_frame_creation("Calibrate IMU", calibrate_IMU, 15, 2, "#D9D9D9", "#000000", "#2e8b57", presets_module_x+70, presets_module_y+320) 

# Create a Frame widget for the specific region
module_frame_creation("Random Vibration Generator", 205, 30, 510, 104, vibration_module_x, vibration_module_y)

# amplitude Slider
amplitude_vib_value = tk.StringVar()
amplitude_vib_display = ttk.Spinbox(root, textvariable=amplitude_vib_value, width = 5, from_=amplitude_vib_min, to=amplitude_vib_max)
amplitude_vib_display.place(x=vibration_module_x+120, y=vibration_module_y+45)
amplitude_vib_slider = ttk.Scale(root, from_=amplitude_vib_min, to=amplitude_vib_max, orient=tk.HORIZONTAL, command=slider_changed, length=slider_length, variable= amplitude_vib_value)
amplitude_vib_slider.place(x=vibration_module_x+220, y=vibration_module_y+50) 
slider_module_creation("Amplitude (deg):", amplitude_vib_reset_button_click, f"    {amplitude_vib_min}", f"{amplitude_vib_max}", vibration_module_x + 10, vibration_module_y + 47)

# intensity Slider
intensity_vib_value = tk.StringVar()
intensity_vib_display = ttk.Spinbox(root, textvariable=intensity_vib_value, width = 5, from_=0, to=10)
intensity_vib_display.place(x=vibration_module_x+120, y=vibration_module_y+95)
intensity_vib_slider = ttk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL, command=slider_changed, length=slider_length, variable=intensity_vib_value)
intensity_vib_slider.place(x=vibration_module_x+220, y=vibration_module_y+100)
slider_module_creation("Intensity (level):", intensity_vib_reset_button_click, f"    {intensity_vib_min}", f"{intensity_vib_max}", vibration_module_x + 10, vibration_module_y + 97)

# stop random vibration button
button_creation("Start Vibration", start_random_vibration, 13, 2, "#2e8b57", "#FFFFFF", vibration_module_x, vibration_module_y+150)

# stop random vibration button
button_creation("Stop Vibration", stop_random_vibration, 13, 2, "#cd5c5c", "#FFFFFF", vibration_module_x+140, vibration_module_y+150)

button_creation("Vib Mode", set_vibration_mode, 13, 2, "#D9D9D9", "#000000", vibration_module_x+290, vibration_module_y+150)

# Create a label to display the output
vibration_mode_label = tk.Label(root, text="", font=text_font4, width=6, height=2, background="#FFFFFF", foreground=font_colour)
vibration_mode_label.place(x=vibration_module_x+430, y=vibration_module_y+150)

# button_creation("reconnect", establish_ethernet_communication, 16, 2, "#4169e1", "#FFFFFF", other_buttons_x, other_buttons_y)

# stop button
stop_button = tk.Button(root, text="Stop!", command=emergency_stop, width=15, height=2, bg="#FF0000", fg="#FFFFFF", font=("Helvetica", 13, "bold"), bd=0, padx=2, pady=2)
stop_button.place(x=other_buttons_x, y=other_buttons_y+80)  # Adjust placement accordingly

# enable button
button_creation("Enable", enable_button_click, 15, 2, "#008000", "#FFFFFF", other_buttons_x+180, other_buttons_y+80)

# Button to exit the application 
button_with_frame_creation("Exit App", exit_button_click, 15, 2, "#EBEBEB", "#FF0000", "#FF0000", other_buttons_x+350, other_buttons_y+80)

# Create a label to display the output
Status_label = ttk.Label(root, text="Status:", font=text_font3, foreground=font_colour, background= "#f9f9f9")
Status_label.place(x=status_module_x, y=status_module_y)
output_label = tk.Label(root, text="", font=text_font4, width=38, height=1, background="#f9f9f9", foreground=font_colour)
output_label.place(x=status_module_x+55, y=status_module_y)

# Call the function to constantly update slider values and display integer values
update_slider_values()

# Create a Tkinter canvas to embed the Matplotlib plot
canvas = tk.Canvas(root)
canvas.place(x=graph_x, y=graph_y)  # Adjust the placement of the canvas accordingly

# Visualize the original and transformed positions of the base and platform joints with connecting lines
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')

# Create a FigureCanvasTkAgg object
canvas = FigureCanvasTkAgg(fig, master=canvas)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

set_vibration_mode()
startup()

# Start the main loop
root.mainloop()
#Send the closing command to the microcontroller once the GUI is closed
#close_application_click()
#close the ethernet communication
#s.close()
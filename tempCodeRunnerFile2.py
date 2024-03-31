import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import subprocess
import time

# Create a VideoCapture object
cap = cv2.VideoCapture(0)  # Change the index to select the correct camera

# Set the resolution
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(3, 3840)  # Set the width to 320 pixels
cap.set(4, 2160)  # Set the height to 240 pixels

# Check if the resolution was correctly set
width = cap.get(3)
height = cap.get(4)
print(f'Resolution is set to: {width}x{height}')

# Create a tkinter app
root = tk.Tk()
root.title("Hoopster")
root.geometry("1024x600")
root.configure(bg="white")

# Create a Label widget for the live feed
live_feed = tk.Label(root)
live_feed.pack()

def update_frame():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Resize the frame
    frame = cv2.resize(frame, (360, 240))  # Set the dimensions as needed

    # Convert the image from OpenCV BGR format to PIL RGB format
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)

    # Convert the Image object to a TkPhoto object
    tk_image = ImageTk.PhotoImage(image)

    # Update the Label image
    live_feed.config(image=tk_image)
    live_feed.image = tk_image

    # Repeat this function after 20 milliseconds
    live_feed.after(20, update_frame)

# Start the frame update process
update_frame()

pady1 = Box(window, height = 30, width = 30)
gif = Picture(window, image = "GUI/swish.gif", width = 600, height = 400)
pady = Box(window, height = 30, width = 30)
box = Box(window, layout = "grid")

suc = 0
fail = 0
total = 0
rateval = 0

set_trig = False
launched = False

def success_shot():
    global suc
    suc += 1
    app.show()
    update_stats()
    abort_fun()
    window.hide()

def fail_shot():
    global fail
    fail += 1
    app.show()
    update_stats()
    abort_fun()
    window.hide()

def run_move_menu():
    try:
        # Replace 'path/to/your/script.py' with the actual path to your Python script
        app.hide()
        process = subprocess.Popen(['python', 'MobilityDisplay.py'])
        # Continue with the rest of the parent script without waiting for the subprocess
        
        process.wait()
        print("Parent script continues running...")
        # Display the application again    
        app.show()

    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")

def run_manual_menu():
    try:
        # Replace 'path/to/your/script.py' with the actual path to your Python script
        app.hide()
        process = subprocess.Popen(['python', 'ManualDisplay.py'])
        # Continue with the rest of the parent script without waiting for the subprocess
        
        process.wait()
        print("Parent script continues running...")
        # Display the application again    
        app.show()


    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")

menubar = MenuBar(app,
                  toplevel=["Displays"],
                  options=[
                      [ ["Manual Input", run_manual_menu], ["Mobility", run_move_menu] ]                     
                  ])

#success = PushButton(box,text="Success",  width=10, height = 2, grid=[0,0], command=success_shot)
success = PushButton(box, image="GUI/Success.png",  width=215, height = 95, grid=[0,0], command=success_shot)
success.bg = "green"
buffer = Box(box,  height=20, width=30, grid=[1,0])
#failure = PushButton(box, text="Fail", width=10, height = 2, grid=[2,0], command=fail_shot)
failure = PushButton(box, image="GUI/Fail.png", width=215, height = 95, grid=[2,0], command=fail_shot)
failure.bg="#CC6600";
#success.bg="green"
#failure.bg="red"

app.font="Arial Black"
app.text_size=16;
#box_main = Box(app, grid=[0,0], width=35,height=25)
#box_main.bg="green"
#logo = PushButton(app, image="logo.png",  grid=[0,0], align="left", command=run_move_menu, width=165, height=165)
#logo = PushButton(app, image="GUI/logo.png",  grid=[0,0], align="left", command=run_move_menu, width=200, height=200)

# Create the status labels
status_frame = tk.Frame(root)
status_frame.grid(row=1, column=0, sticky="nsew")

hoop_status = tk.Label(status_frame, text="HOOP DETECTED")
hoop_status.grid(row=0, column=0)

pos_status = tk.Label(status_frame, text="POSITION SET")
pos_status.grid(row=1, column=0)

dis_status = tk.Label(status_frame, text="DISTANCE CALCULATED")
dis_status.grid(row=2, column=0)

ang_status = tk.Label(status_frame, text="LAUCH ANGLE CALCULATED")
ang_status.grid(row=3, column=0)

vel_status = tk.Label(status_frame, text="VELOCITY CALCULATED")
vel_status.grid(row=4, column=0)

anom_status = tk.Label(status_frame, text="ANOMALY DETECTED")
anom_status.grid(row=5, column=0)

ready_status = tk.Label(status_frame, text="READY FOR LAUNCH")
ready_status.grid(row=6, column=0)
# Rest of the code is omitted for brevity. You can replace the guizero widgets with the corresponding tkinter widgets.
# For example, you can replace PushButton with tk.Button, Text with tk.Label, and so on.



root.mainloop()

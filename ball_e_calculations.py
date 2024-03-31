import numpy as np
from scipy.integrate import solve_ivp
import math


import cv2  # openCV library


# Drag coefficient, projectile radius (m), area (m2) and mass (kg).
C_d = 0.47
D = 0.2413  # m
R = D / 2  # m
A = np.pi * R**2
m = 0.624
# Air density (kg.m-3), acceleration due to gravity (m.s-2).
rho_air = 1.28
g = 9.81
# For convenience, define  this constant.
k = 0.5 * C_d * rho_air * A
y_goal = 3.05  # m


def deriv(t, u):
    x, v_x, y, v_y = u
    speed = np.hypot(v_x, v_y)
    dv_x_dt = -k/m * speed * v_x
    dv_y_dt = -k/m * speed * v_y - g
    return v_x, dv_x_dt, v_y, dv_y_dt




# Integrate up to tf unless we hit the target sooner.
t0, tf = 0, 50


def hit_target(t, u):
    # We've hit the target if the y-coordinate is 0.
    return u[2]
# Stop the integration when we hit the target.
hit_target.terminal = True
# We must be moving downwards (don't stop before we begin moving upwards!)
hit_target.direction = -1


def max_height(t, u):
    # The maximum height is obtained when the y-velocity is zero.
    return u[3]


def calculate_auto(x_goal):
    theta_arr = []
    v_i_arr = []
    angle2 = []
    x_arr = []
    y_arr = []


    theta = 0.87
   
    while theta < 1.38:
        v_i = 6.8
        while v_i < 10.3:
            # Initial conditions: x0, v0_x, y0, v0_.
            u0 = 0, v_i * np.cos(theta), 1, v_i * np.sin(theta)
           
            # call diff eq solver
            soln = solve_ivp(deriv, (t0, tf), u0, dense_output=True,
                 events=(hit_target, max_height))
            # A fine grid of time points from 0 until impact time.
            t = np.linspace(0, soln.t_events[0][0], 100)


            # Retrieve the solution for the time grid and plot the trajectory.
            sol = soln.sol(t)
            x, y = sol[0], sol[2]
            check = 0


            # loop through trajectory and compare coordinates to coordinate of hoop
            for i in range(0, len(t)):
                # if too close to rim the shot is unlikely to make it -> break loop
                if (abs(x_goal-0.2286-x[i])**2 + abs(y[i]-y_goal)**2)**(1/2) <= 0.12065:
                    break
                # condition of making a shot: center of ball within 5cm of center of hoop
                elif abs(x_goal-x[i]) < 0.05 and abs(y_goal-y[i]) < 0.05 and y[i] < y[i - 1]:
                    theta_arr.append(theta)
                    v_i_arr.append(v_i)
                    angle2.append(math.atan((y[i - 1] - y[i]) / (x[i] - x[i - 1])))   # entrance angle
                    x_arr.append(x)
                    y_arr.append(y)
                    check = 1
                    break
            if check == 1:
                break
            v_i += 0.1
        theta += 0.01
   
    min_v = min(v_i_arr)
    index = v_i_arr.index(min_v)
    return x_arr[index], y_arr[index], theta_arr[index], round(min_v, 2)




def get_rpm(v_b):
    omega_b = 5  # rad/s
    r_w = 0.15  # m
    r_b = 0.12065  # m
    omega_a = (v_b - omega_b * r_b) / r_w  # rad/s
    omega_c = omega_b * 2 * r_b / r_w + omega_a  # rad/s
    rpm_a = omega_a * 60 / (2 * math.pi)  # rpm
    rpm_c = omega_c  * 60 / (2 * math.pi) # rpm


    return rpm_a, rpm_c


def calculate_manual(theta, v_i):
    u0 = 0, v_i * np.cos(theta), 1, v_i * np.sin(theta)
           
    soln = solve_ivp(deriv, (t0, tf), u0, dense_output=True,
        events=(hit_target, max_height))
    # A fine grid of time points from 0 until impact time.
    t = np.linspace(0, soln.t_events[0][0], 100)


    # Retrieve the solution for the time grid and plot the trajectory.
    sol = soln.sol(t)
    x, y = sol[0], sol[2]
    return x, y


# distance from camera to hoop measured
# centimeter
Known_distance = (457.2**2 + 305**2)**(1/2)


# width of face in the real world or Object Plane
# centimeter
Known_width = 24.13


# focal length finder function
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
    # finding the focal length
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length






def hoop_width(imageFrame):
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)


    # Set range for orange color and define mask
    orange_lower = np.array([0, 100, 0], np.uint8)
    orange_upper = np.array([10, 255, 255], np.uint8)
    orange_mask = cv2.inRange(hsvFrame, orange_lower, orange_upper)


    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")


    # For red color
    orange_mask = cv2.dilate(orange_mask, kernal)


    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(orange_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)


    largest = [0,0, 1]
    w = 0
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 200):
            x, y, w, h = cv2.boundingRect(contour)
            if (w > largest[0]):
                largest = [w, h, contour]
               
    # bound hoop in image with rectangle and label with "hoop"
    if largest != [0, 0, 1]:
        contour = largest[2]
        x, y, w, h = cv2.boundingRect(contour)
        imageFrame = cv2.rectangle(imageFrame, (x, y),
                                (x + w, y + h),
                                (0, 0, 255), 2)


        cv2.putText(imageFrame, "hoop", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                    (0, 0, 255))
   
    return w




# reading reference_image from directory
ref_image = cv2.imread("hoop21.png")


# find the face width(pixels) in the reference_image
ref_image_hoop_width = hoop_width(ref_image)


# get the focal by calling "Focal_Length_Finder"
# width in reference(pixels),
# Known_distance(centimeters),
# known_width(centimeters)
Focal_length = Focal_Length_Finder(
    Known_distance, Known_width, ref_image_hoop_width)




# distance estimation function
def distance_finder(face_width_in_frame):
    distance = (Known_width * Focal_length)/face_width_in_frame
    distance = (distance / 100 + 1.9054) / 1.1392
    return distance
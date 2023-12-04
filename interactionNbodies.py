# Libraries:

import sys  # Package to use the exit() command that allows stopping the program at that line.
import numpy as np
import os  # Package to create a file.
import time  # Package for calculating execution time.
import math  # Package for rounding numbers.
import random as rd  # Package for generating random numbers.


# Functions:

def accelerations(t, r, m):

    # Initialize a vector to store accelerations; r contains the coordinates of the n bodies.
    a = np.zeros(len(r), np.longdouble) 

    # Calculate gravitational interaction among the n bodies.
    i, j = 0, 0

    while i < len(m):  # Loop to obtain the acceleration of body i.

        while j < len(m):  # Loop to sum interactions between body i and bodies j.

            if i == (len(m) - 1) and i == j:  # Condition to end loops if we have reached the last body and the last interaction.
                break

            elif i == j:  # Condition to avoid calculating the interaction of body i with itself.
                j += 1

            # Equation for gravitational interaction per unit mass i.
            a[3*i:3*i+3] += -G * m[j] * (r[3*i:3*i+3] - r[3*j:3*j+3]) / (np.linalg.norm(r[3*i:3*i+3] - r[3*j:3*j+3])**3 + epsilon)

            j += 1
            
        i += 1
        j = 0
        
    return a



def randomBodies(bodyMass, numBodies):

    mAlt = np.array([bodyMass])
    rAlt = np.array([rd.uniform(-1, 1), rd.uniform(-1, 1), rd.uniform(-1, 1)])
    vAlt = np.array([rd.uniform(-1, 1), rd.uniform(-1, 1), rd.uniform(-1, 1)])

    for i in range(numBodies - 1):
        rAlt = np.concatenate((rAlt, [rd.uniform(-1, 1), rd.uniform(-1, 1), rd.uniform(-1, 1)]))
        vAlt = np.concatenate((vAlt, [rd.uniform(-1, 1), rd.uniform(-1, 1), rd.uniform(-1, 1)]))
        mAlt = np.concatenate((mAlt, [bodyMass]))

    return mAlt, rAlt, vAlt * 0.1



# Initial conditions :

epsilon = 0 # Smoothing factor, used in acceleration to avoid machine zero.
G = 1 
Gc = 6.6743e-11
folder = "dataBodies"

# Unit conversion factors.
distanceUnit = float(0.378e9) # m
timeUnit = float(86400) # s



# Simulation time.
t0 = 0 / timeUnit

# System 
# tf = 10 * 27.3217 * 24 * 60 * 60 / timeUnit 
# tf = 10 * 365 * 24 * 60 * 60 / timeUnit 
# N = 512000

# Random bodies
tf = 1 * 1 * 24 * 60 * 60 / timeUnit  
N = 140 * 2**13

dt = (tf - t0)/N 


# System
# # Sun.

# mS = 1988500e24 * (Gc *  timeUnit**2 / distanceUnit**3)

# x0_S = 0 / distanceUnit
# y0_S = 0 / distanceUnit
# z0_S = 0 / distanceUnit

# vx0_S = 0 * (timeUnit/distanceUnit)
# vy0_S = 0 * (timeUnit/distanceUnit)
# vz0_S = 0 * (timeUnit/distanceUnit)

# pS_0 = np.array([x0_S, y0_S, z0_S], np.longdouble)
# vS_0 = np.array([vx0_S, vy0_S, vz0_S], np.longdouble)




# # Earth at apogee to the sun.

# mE = 5.9722e24 * (Gc * timeUnit**2 / distanceUnit**3) 

# x0_E = 152.1e9 / distanceUnit
# y0_E = 0 / distanceUnit
# z0_E = 0 / distanceUnit

# vx0_E = 0 * (timeUnit/distanceUnit)
# vy0_E = 29.29e3 * (timeUnit/distanceUnit)
# vz0_E = 0 * (timeUnit/distanceUnit)

# pE_0 = np.array([x0_E, y0_E, z0_E], np.longdouble)
# vE_0 = np.array([vx0_E, vy0_E, vz0_E], np.longdouble) 



# # Moon at apogee to the earth.

# mM = 0.07346e24 * (Gc * timeUnit**2 / distanceUnit**3) 

# x0_M = (152.1e9 + 0.4055e9) / distanceUnit
# y0_M = 0 / distanceUnit
# z0_M = 0 / distanceUnit

# vx0_M = 0 * (timeUnit/distanceUnit)
# vy0_M = (29.29e3 + 0.97e3) * (timeUnit/distanceUnit)
# vz0_M = 0 * (timeUnit/distanceUnit)

# pM_0 = np.array([x0_M, y0_M, z0_M], np.longdouble)
# vM_0 = np.array([vx0_M, vy0_M, vz0_M], np.longdouble) 


# masses = np.array([mS, mE, mM])
# r0 = np.concatenate((pS_0, pE_0, pM_0), dtype = np.longdouble)
# v0 = np.concatenate((vS_0, vE_0, vM_0), dtype = np.longdouble)
# nameBodies = ('Sun', 'Earth', 'Moon')
# planets = 'SEM'



# Random bodies
rd.seed(9)
bodyMass = 5
numBodies = 5
masses, r0, v0 = randomBodies(bodyMass, numBodies)




print("Calculating positions and writing them to a file...")

st = time.time()  # Initial time.

# Calculation of the trajectory with RK order 4 for n bodies in 3D.
# fileName = f"{planets}_RK4_dt={dt}_N={N}"  # System.
fileName = f"{numBodies}_m={bodyMass}_RK4_dt={dt}_N={N}"  # Random bodies.



# We will separate the trajectories of the bodies into different files, parts = 1,2,3,..
# We will do this for cases where we fill the files with our data or if we do not
# want to have very heavy files. We will use two variables:
#
# part: It will identify which part of the trajectory is saved in the file, it will also help us in the exit condition
#       of the file writing (used in the for loop below).
# numData: It will be the amount of data that will be saved in each file.
# tfPart: Time interval that will be saved in each part.
# totalParts: Total number of parts.

numData = 1000000

# See how much the interval will be worth, if N < numData then we will only need one file, therefore
# the interval will be the entire time tfPart = tf.
# If the total points are greater than the required points in each part then we divide the total time into
# the number of parts needed, rounding up so that all the data is saved in one file.

if N / numData <= 1:
    totalParts = 1
    tfPart = tf
else:
    totalParts = math.ceil(N / numData)
    tfPart = tf / totalParts


# Initialize the vectors where the values to be plotted will be stored.

t = t0
r = r0
v = v0
     

for part in range(1, 1 + totalParts) : # The + 1 is because of how the range function works.

    # Create a file to save time and positions, if it already exists, it replaces it.
    with open(f"{folder}/{fileName}_P{part}Of{totalParts}_POS.txt", 'w') as posFile:

        # Create a file to save time and velocities, if it already exists, it replaces it.
        with open(f"{folder}/{fileName}_P{part}Of{totalParts}_VEL.txt", 'w') as velFile: 

            # Names of the columns.
            posFile.write("Time    ")
            velFile.write("Time     ")


            # Random bodies :
            posFile.write(f"Positions of {len(masses)} bodies: ") 
            velFile.write(f"Velocities of {len(masses)} bodies: ") 


            # System :
            # for j in range(len(masses)) :
                
            #     posFile.write(nameBodies[j]  + "(x,y,z)     ")    
            #     velFile.write(nameBodies[j]  + "(x,y,z)     ") 


            posFile.write(os.linesep)
            velFile.write(os.linesep)
                    
            posFile.write(" " + os.linesep)
            velFile.write(" " + os.linesep)



            # npoint indicates in the value of N where we stayed in the previous file, which is numData for
            # the part of the file where we are, we put part - 1 because in the for loop of the writing
            # we start with part = 1.

            npoints = numData * (part - 1)

            # We subtract part in the final value because when changing the file the last point is written in the 
            # file that is and in the next one, this will happen every time we change the file so
            # we will subtract those repeated values ​​from the final value. We subtract 1 from part because it starts at 1.

            for points in range( npoints, N - (part-1) ) : 

                # Writing positions to the file.

                posFile.write(str(t)  + "       ") # Time.
                velFile.write(str(t)  + "       ") # Time.

                for j in range(3*len(masses)) :

                    posFile.write(str(r[j])  + "       ") # Positions
                    velFile.write(str(v[j])  + "       ") # Velocities.

                posFile.write(os.linesep)
                velFile.write(os.linesep)



                # Calculating the dynamics of the N bodies.

                # 4 order RK for velocities and positions:

                # Kiv : Velocities' ks.
                # Kir : Positions' ks

                k1v = dt*accelerations(t, r, masses)
                k1r = dt*v

                k2v = dt*accelerations(t + dt/2, r + k1r/2, masses)
                k2r = dt*(v + k1v/2)

                k3v = dt*accelerations(t + dt/2, r + k2r/2, masses)
                k3r = dt*(v + k2v/2)

                k4v = dt*accelerations(t + dt, r + k3r, masses)
                k4r = dt*(v + k3v)

                r += (k1r + 2*k2r + 2*k3r + k4r)/6
                v += (k1v + 2*k2v + 2*k3v + k4v)/6

                t += dt


                # Condition for file change.
                # To change the file, the iterated variable (points) must be equal to the number of data per file
                # (numData) for the part where we are (part).

                if (points == numData*part) :

                    break
                

et = time.time() # Final time.

time_elapsed = et - st # Execution time.

print(f"File: {fileName} has {totalParts} parts.")
print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(time_elapsed)))

# Libraries:

import sys  # Package to use the exit() command that allows stopping the program at that line.
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Package for 3D axes.
from matplotlib import animation  # Package for animation.
import pandas as pd  # Package used for reading files.
import time  # Package for calculating execution time.
import math  # Package for rounding numbers.



# Functions.

def nBodies_Animation3D(num, fps, time, Bodies, data, nameBodies, colorBodies):

    ax.clear()  # Clears the figure to update the line, points, title, and axes.

    j = 0
    while j < Bodies:  # While loop to plot the trajectories of different masses.

        # loc creates a dataframe from the existing one. to_numpy converts a pandas dataframe to a numpy array.
        # loc is inclusive with the indices.
        rg = data.loc[:, 1 + 3*j : 3*j + 3].astype(float).to_numpy()

        # Update trajectory line (num+1 due to how indices work in python).
        # fps * num would mean drawing every fps plots, which speeds up the animation if there are too many points.

        ax.plot3D(rg[:(fps * num) + 1, 0], rg[:(fps * num) + 1, 1], rg[:(fps * num) + 1, 2], \
                  linewidth=2, color=colorBodies[j])

        # Update end point.

        ax.scatter(rg[(fps * num), 0], rg[(fps * num), 1], rg[(fps * num), 2], \
                   marker='o', s=20, color=colorBodies[j])

        j += 1

    # Axis limits (optional).
    # Set it to +- 10 in case the orbits are in a plane. For example, if they are in the x,y plane,
    # then the limits of z would be (0,0), which cannot be plotted.
    # To animate the sun-earth-moon system is better to use this.

    # if np.amin(rg[:, 0 :: 3]) == np.amax(rg[:, 0 :: 3]):  # Check if it's in the y,z plane.

    #     ax.set_xlim3d([-10, 10])
    #     ax.set_ylim3d([np.amin(rg[:, 1 :: 3]), np.amax(rg[:, 1 :: 3])])
    #     ax.set_zlim3d([np.amin(rg[:, 2 :: 3]), np.amax(rg[:, 2 :: 3])])

    # elif np.amin(rg[:, 1 :: 3]) == np.amax(rg[:, 1 :: 3]):  # Check if it's in the x,z plane.

    #     ax.set_xlim3d([np.amin(rg[:, 0 :: 3]), np.amax(rg[:, 0 :: 3])])
    #     ax.set_ylim3d([-10, 10])
    #     ax.set_zlim3d([np.amin(rg[:, 2 :: 3]), np.amax(rg[:, 2 :: 3])])

    # elif np.amin(rg[:, 2 :: 3]) == np.amax(rg[:, 2 :: 3]):  # Check if it's in the x,y plane.

    #     ax.set_xlim3d([np.amin(rg[:, 0 :: 3]), np.amax(rg[:, 0 :: 3])])
    #     ax.set_ylim3d([np.amin(rg[:, 1 :: 3]), np.amax(rg[:, 1 :: 3])])
    #     ax.set_zlim3d([-10, 10])
    # else:  # Not in one of the main planes; none of the coordinates are 0 throughout the trajectory.

    #     ax.set_xlim3d([np.amin(rg[:, 0 :: 3]), np.amax(rg[:, 0 :: 3])])
    #     ax.set_ylim3d([np.amin(rg[:, 1 :: 3]), np.amax(rg[:, 1 :: 3])])
    #     ax.set_zlim3d([np.amin(rg[:, 2 :: 3]), np.amax(rg[:, 2 :: 3])])


    # Graph labels.
    ax.set_title(str(format(time[fps * num], ".4g")) + ' days', fontsize=17, pad=0)
    ax.set_xlabel(r'$x$ $(M_l)$', fontsize=10)
    ax.set_ylabel(r'$y$ $(M_l)$', fontsize=10)
    ax.set_zlabel(r'$z$ $(M_l)$', fontsize=10)
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.05), ncol=3)

    # Remove grid, axes, or ticks.
    plt.grid(False)
    plt.axis('off')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])



# Read file.

print("Reading the file and plotting...")
st = time.time()  # Initial time.


# Reading and plotting information

# System
# numberBodies = 3
# folderData = "dataBodies"
# folderPlot = "plotBodies"
# fileName = "SEM_RK4_dt=0.00712890625_N=512000_exaggeratedMoon" 
# N = 512000
# totalParts = 1
# nameBodies = ('Sun', 'Earth', 'Moon')
# colorBodies = ('orange', 'blue', 'gray')

# Random bodies
numberBodies = 5
folderData = "dataBodies"
folderPlot = "plotBodies"
fileName = "5_m=5_RK4_dt=8.719308035714285e-07_N=1146880" 
N = 1146880
totalParts = 2
nameBodies = ('1', '2', '3','4', '5')
colorBodies = ('orange', 'navy', 'red', 'blue', 'gray')

part = tuple(i for i in range(1,1 + totalParts))
dir = (folderData, fileName, totalParts, part)



# Plotting.

fig = plt.figure(figsize=(12, 12), dpi=180)  # figsize: inches by inches.
ax = plt.axes(projection='3d')
ax.set_xlabel(r'$x$ $(M_l)$')
ax.set_ylabel(r'$y$ $(M_l)$')
ax.set_zlabel(r'$z$ $(M_l)$')



# System
# ax.set_xlim3d([-400, 400])
# ax.set_ylim3d([-400, 400])

# Ransom bodies
ax.set_xlim3d([-1, 1])
ax.set_ylim3d([-1, 1])
ax.set_zlim3d([-1, 1])

# Change the camera when first viewing the plot and when saving.
# The first number indicates the degrees with respect to the z+ axis, and the second with the x+ axis.

ax.view_init(30, 310) 
# ax.view_init(80, 270) 

for part in range(1, 1 + totalParts):  # The +1 is because of how the range function works.

    # The first argument is the name of the file to read.
    #
    # sep: the format of separation between the data \s+ means it is a quantity of spaces.
    #
    # header: Whether we will take some title for the columns to put in the dataframe.
    #
    # skiprows: How many columns will be skipped to start reading.
    #
    # dtype: Data type to read.

    data = pd.read_csv(f"{folderData}\{fileName}_P{part}Of{totalParts}_POS.txt", sep='\s+', \
                        header=None, skiprows=1, dtype='float')            
    data = pd.DataFrame(data)

    for j in range(numberBodies):  # While loop to plot the trajectories of different masses.

        # loc creates a dataframe from the existing one. to_numpy converts a pandas dataframe to a numpy array.
        # 1 + at the beginning because the first column is time.

        rg = data.loc[:, 1 + (3 * j): 1 + (3 * j + 3)].astype(float).to_numpy()

        # System.
        # ax.plot3D(rg[:, 0], rg[:, 1], rg[:, 2], color=colorBodies[j])  

        # Random bodies.
        ax.plot3D(rg[:, 0], rg[:, 1], rg[:, 2])  

        if (part == totalParts):

            # System:
            # ax.scatter(rg[(len(rg) - 1), 0], rg[(len(rg) - 1), 1], rg[(len(rg) - 1), 2], \
            #             marker='o', label=nameBodies[j], color=colorBodies[j])
            # ax.scatter(rg[(len(rg) - 1), 0], rg[(len(rg) - 1), 1], rg[(len(rg) - 1), 2], \
            #             marker='o', color=colorBodies[j])

            # Random bodies:
            ax.scatter(rg[(len(rg) - 1), 0], rg[(len(rg) - 1), 1], rg[(len(rg) - 1), 2], \
                        marker='o')



# Place the legends on the graphs.
# loc: Places the legends on the part of the plot you indicate.
# bbox_to_anchor: If the legends overlap with the plot, this can be used to adjust their position (x, y)
# ncol: Specifies the number of columns that the legend will have where the plot names will be.

# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.05), ncol=4)

plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

# Remove grid, axes, or ticks.
plt.grid(False)
plt.axis('off')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])

# Save the plot.
plt.savefig(f"{folderPlot}\{fileName}.pdf", bbox_inches="tight", pad_inches=0)

plt.close()

et = time.time()  # Final time.

time_elapsed = et - st  # Execution time.

print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(time_elapsed)))






# Plotting the animation.

print("Creating the animation...")

st = time.time()  # Initial time.

fig = plt.figure(figsize=(6.5, 6), dpi=120)  # figsize: inches per inch, (6.5, 6)
                                             # dpi: dots per inch (resolution).

ax = plt.axes(projection='3d')

# Remove some of the white space from the plot.
fig.subplots_adjust(left=-0.05, bottom=-0.3, right=0.95, top=0.95, wspace=None, hspace=None)

# Move the view of the plot.
# ax.view_init(80, 270) 
ax.view_init(30, 310) 

# Create a data frame where the information from all files is stored in one.

for part in range(1, 1 + totalParts):  # The + 1 is due to how the range function works.

    # The first argument is the name of the file to be read.
    #
    # sep: the format of separation between the data \s+ means it is a certain number of spaces.
    #
    # header: If we will take some title for the columns to put in the dataframe.
    #
    # skiprows: How many columns will be skipped to start reading.
    #
    # dtype: Data type to read.

    if part == 1:

        finalDataAnimation = pd.read_csv(f"{folderData}\{fileName}_P{part}Of{totalParts}_POS.txt", sep='\s+', \
                                        header=None, skiprows=1, dtype='float')            
        finalDataAnimation = pd.DataFrame(finalDataAnimation)

    else:

        dataAnimation = pd.read_csv(f"{folderData}\{fileName}_P{part}Of{totalParts}_POS.txt", sep='\s+', \
                                    header=None, skiprows=1, dtype='float')            
        dataAnimation = pd.DataFrame(dataAnimation)

        # axis = 0 concatenates by row and = 1 by column. 
        # ignore_index=True makes the indices run.

        finalDataAnimation = pd.concat([finalDataAnimation, dataAnimation], axis=0, ignore_index=True)

# Choose which bodies and up to what time we are going to plot.

# System
# times = finalDataAnimation.loc[:70000, 0]
# positions = finalDataAnimation.loc[:70000, 1:]

# Random bodies
times = finalDataAnimation.loc[:, 0]
positions = finalDataAnimation.loc[:, 1:]



# Call the function for the animation.

# fig: Canvas.
# nBodies_Animation3D: Function that plots each frame.

# fargs: Arguments of the function where it is plotted, in this case nBodies_Animation3D. This function
# cannot take any arguments, even if defined with an argument, that is an iterative variable that
# the animation.FuncAnimation function itself uses to plot all the frames.

# interval: time in milliseconds between each frame.

# frames: Number of plots that will be used in the animation. If you want the entire trajectory or plot
# that you have, you must set it equal to the number of plots that will be painted throughout the animation.

# When the animation has too many points, it takes a long time to see the evolution of the animation. Therefore,
# instead of plotting the points one by one, we plot every fps points.


# fps = 600 # System 
fps = 1080*5 # Random bodies

numPoints = int(len(times)/fps)


# Arguments of fargs: (num,fps,time,bodies,data,nameBodies,colorBodies)

varAnimation = animation.FuncAnimation(fig, nBodies_Animation3D, \
                                    fargs=(fps, times, numberBodies, positions, nameBodies, colorBodies), \
                                    interval=60, frames=numPoints)


# Save animation.

writer_gif = animation.PillowWriter(fps=fps)  # Function that will write the animation to be saved.
varAnimation.save(f"{folderPlot}\{fileName}.gif", writer=writer_gif) 


et = time.time()  # Final time.

time_elapsed = et - st  # Execution time.

print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(time_elapsed)))

plt.close()

# Libraries:

import sys  # Package to use the exit() command that allows stopping the program at that line.
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Package for 3D axes.
from matplotlib import animation  # Package for animation.
import pandas as pd  # Package I will use to read files.
import time  # Package for calculating execution time.
import math  # Package for rounding numbers.
import os  # Package to create a file.

# Read file.

print("Reading the file and creating a file...")
st = time.time()  # Initial time.

numberBodies = 3
folderData = "dataBodies"
fileName = "SEM_RK4_dt=0.00712890625_N=512000"
totalParts = 1
nameBodies = ('Sun', 'Earth', 'Moon')
colorBodies = ('orange', 'blue', 'gray')


part = tuple(i for i in range(1, 1 + totalParts))
dir = (folderData, fileName, totalParts, part)

for part in range(1, 1 + totalParts):  # the + 1 is because of how the range function works.

    # First argument is the name of the file to read.
    #
    # sep : the format of separation between the data \s+ means it's a number of spaces.
    #
    # header : Whether we will take any title for the columns to put in the dataframe.
    #
    # skiprows : How many columns will be skipped to start reading.
    #
    # dtype : Data type to read.

    data = pd.read_csv(f"{folderData}\{fileName}_P{part}Of{totalParts}_POS.txt", sep='\s+', \
                       header=None, skiprows=1, dtype='float')
    data = pd.DataFrame(data)

    t = data.loc[:, 0].astype(float).to_numpy()
    sol = data.loc[:, 1:3].astype(float).to_numpy()
    tierra = data.loc[:, 4:6].astype(float).to_numpy()
    luna = data.loc[:, 7:9].astype(float).to_numpy()

    diff = luna - tierra

    luna = tierra + diff * 50

    positions = [sol, tierra, luna]

    # Create a file to save the time and exaggerated moon positions.
    with open(f"{folderData}\{fileName}_exaggeratedMoon_P{part}Of{totalParts}_POS.txt", 'w') as posFile:

        # Names of the columns.

        posFile.write("Time     ")

        # Systems :

        for j in range(numberBodies):
            posFile.write(nameBodies[j] + "(x,y,z)     ")

        posFile.write(os.linesep)

        posFile.write(" " + os.linesep)

        # Writing the positions in the file.

        for i in range(len(t)):

            posFile.write(str(t[i]) + "       ")  # Time.

            for j in range(numberBodies):

                for k in range(3):
                    posFile.write(str(positions[j][i][k]) + "       ")  # Positions.

            posFile.write(os.linesep)


et = time.time()  # Final time.

time_taken = et - st  # Execution time.

print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(time_taken)))

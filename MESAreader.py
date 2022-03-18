# author: Mathieu Renzo

# Author: Mathieu Renzo <mathren90@gmail.com>
# Keywords: files

# Copyright (C) 2019-2022 Mathieu Renzo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

__author__ = "Mathieu Renzo"

import numpy as np
import os
import sys
import glob
import time
import math
import subprocess
# import re
# for log_scrubber
import sys
import shlex

# imports below are optional #
try:
    from termcolor import colored
except ModuleNotFoundError:
    print("no pretty colors, install termcolor for that")
    def colored(string, color):
        print(string)
try:
    import socket
    if socket.gethostname() == "ccalin010.flatironinstitute.org":
        sys.path.insert(0, "/mnt/home/mrenzo/codes/python_stuff/")
    import mesaPlot as mp
    mmm = mp.MESA()
    ppp = mp.plot()
except ModuleNotFoundError:
    print(colored("Failed loading MESA plot, I'll continue anyways","red"))
    pass
try:
    import socket
    if socket.gethostname() == "ccalin010.flatironinstitute.org":
        sys.path.insert(0, "/mnt/home/mrenzo/codes/python_stuff/pyMESA")
    import pyMESA as pym
except ModuleNotFoundError:
    print("pyMESA not found, available at https://github.com/rjfarmer/pyMesa")
    pass

# constants -------------------------------------------------------------------------------
# TODO: import these from pyMESA or astropy
#try:
"""read constants from MESA, requires pyMESA and MESA """
print(colored("reading constants from pyMesa", "blue"))
const_lib, const_def = pym.loadMod("const")
global dayyer
dayyer = const_def.dayer.value
global secyer
secyer = const_def.secyer.value
global G_cgs
G_cgs = const_def.standard_cgrav.value
global Lsun
Lsun = const_def.Lsun.value
global Msun
Msun = const_def.Msun.value
global Rsun_cm
Rsun_cm = const_def.Rsun.value
global clight
clight = const_def.clight.value
# except:
    # # if pyMESA not available, define by hand
    # global dayyer
    # dayyer = 365.25
    # global secyer
    # secyer = dayyer * 24 * 60 * 60
    # global G_cgs
    # G_cgs =  6.67430e-8  # in cgs
    # global Lsun
    # mu_sun = 1.3271244e26
    # Lsun = 3.828e33
    # global Msun
    # Msun = mu_sun / G_cgs
    # global Rsun_cm
    # Rsun_cm = 6.957e10  # in cm
    # global clight
    # clight = 2.99792458e10 # cm/s
# load files -------------------------------------------------------------------------------

def reader(myfile, ncols, nhead):
    """ This example shows how to read a large regular ascii file (consisting of ncolumns), store it in binary format.
    This provides a great speed up when reading larger files created with binary_c or MESA or whateve
    SdM  March 12, 2015
    """

    """15.04.2016 Mathieu: modified to fit my needs for binary_c as well"""

    # The new binary file will be stored with the same name but with the extention.npy
    mybinfile = str(myfile[:-4]) + ".npy"
    # Just for fun... time the routine
    start_time = time.time()
    if not os.path.isfile(mybinfile):  # Check if .databin exists already...
        print("...    reading ascii file ", myfile)
        print("...    and storing it for you in binary format")
        print("...    patience please, next time will be way faster ")
        print("...    I promise")
        # If binary does not exist, read the original ascii file:
        if not os.path.isfile(myfile):
            print("File does not exist ", myfile)
            return
        # Read the first "ncol" columns of the file after skipping "nhead" lines, store in a numpy.array
        data = np.genfromtxt(myfile, skip_header=nhead)  # , usecols=range(ncols))
        # Save the numpy array to file in binary format
        np.save(mybinfile, data)
        # print "...    That took ", time.time() - start_time, "second"
    else:
        # print "... Great Binary file exists, reading data directly from ", mybinfile
        # If binary file exists load it directly.
        data = np.load(mybinfile)
        # print "   That took ", time.time() - start_time, "second"
    return data


def getSrcCol(f, clean=True, convert=True):
    """Returns the header of a MESA output file `f` as a list, and the
    data in that file as a numpy array of shape (number of timesteps,
    number of columns).  If convert is True the file f is saved to
    binary format for faster reading in the future, If clean is True
    use log_scrubber to remove retry steps before converting to binary
    and parsing the output

    """
    # TODO: maybe one day I'll update this to be a pandas dataframe
    # should work both for history and profiles
    # read header
    with open(f, "r") as P:
        for i, line in enumerate(P):
            if i == 5:
                col = line.split()
                break
    # check if binary exists
    mybinfile = str(f[:-4]) + ".npy"
    if os.path.isfile(mybinfile):
        # read the column and binary
        src = reader(f, len(col), 6)
    else:  # binary file does not exist
        print("... Binary file does not yet exist")
        if ("history" in f) and clean:
            scrub(f)
        if convert:
            src = reader(f, len(col), 6)
        else:
            src = np.genfromtxt(f, skip_header=6)
    return src, col

# plotting useful things ---------------------------------------------------------------------
def make2Dmap(x, y, z, x1=0, x2=1, y1=0, y2=1, res=20):
    minx = min(min(x), x1)
    maxx = min(max(x), x2)
    miny = min(min(y), y1)
    maxy = min(max(y), y2)

    x_int = np.linspace(minx, maxx, res)
    y_int = np.linspace(miny, maxy, res)

    mat = np.zeros([len(x_int), len(y_int)])
    for i in range(0, len(x_int) - 1):
        for j in range(0, len(y_int) - 1):
            mat[j, i] = np.sum(
                z[(x >= x_int[i]) * (x < x_int[i + 1]) * (y >= y_int[j]) * (y < y_int[j + 1])]
            )
    return x_int, y_int, mat


def writePreliminary(ax):
    ax.text(
        0.5,
        0.5,
        r"{\bf PRELIMINARY}",
        color="#808080",
        alpha=0.4,
        fontsize=74,
        ha="center",
        va="center",
        rotation=45,
        transform=ax.transAxes,
    )


def my_mark_inset(parent_axes, inset_axes, loc1a=1, loc1b=1, loc2a=2, loc2b=2, **kwargs):
    from mpl_toolkits.axes_grid1.inset_locator import TransformedBbox, BboxPatch, BboxConnector

    rect = TransformedBbox(inset_axes.viewLim, parent_axes.transData)

    pp = BboxPatch(rect, fill=False, **kwargs)
    parent_axes.add_patch(pp)

    p1 = BboxConnector(inset_axes.bbox, rect, loc1=loc1a, loc2=loc1b, **kwargs)
    inset_axes.add_patch(p1)
    p1.set_clip_on(False)
    p2 = BboxConnector(inset_axes.bbox, rect, loc1=loc2a, loc2=loc2b, **kwargs)
    inset_axes.add_patch(p2)
    p2.set_clip_on(False)
    return pp, p1, p2


def read_MESA_header(fname):
    """ reader for the header of MESA profile or history files.
    Parameters:
    ----------
    fname : `string`, path to the file to open
    Returns:
    src : `list` values, some cannot be converted to float
    col : `list`, columns names
    """
    with open(fname, "r") as f:
        for i, line in enumerate(f):
            if i==1:
                col = line.split()
            if i==2:
                src = line.split()
                break
    return src, col


# miscellanea ---------------------------------------------------------------------------------------------

def max_array(a, b):
    # given two arrays of the same length
    # returns an array containing the max in each element
    if len(a) == len(b):
        c = np.zeros(len(a))
        for i in range(len(a)):
            c[i] = max(a[i], b[i])
        return c
    else:
        print("you gave me two array of lengths:", len(a), "=/=", len(b))
        print(colored("can't work with this...going home!", "red"))


def min_array(a, b):
    # given two arrays of the same length
    # returns an array containing the max in each element
    if len(a) == len(b):
        c = np.zeros(len(a))
        for i in range(len(a)):
            c[i] = min(a[i], b[i])
        return c
    else:
        print("you gave me two array of lengths:", len(a), "=/=", len(b))
        print(colored("can't work with this...going home!", "red"))


def SB_law(r, t):
    # given radius and temperature in solar radii and kelvin, returns the luminosity in solar units
    sigma = 5.67051e-5  # cgs units
    Rsun = 6.99e10  # cm
    Lsun = 4e33  # erg/s
    r *= Rsun  # convert to cm
    l = 4 * math.pi * sigma * t ** 4 * r ** 2
    l = l / Lsun
    return l


def tail(f, n):
    # read the last n lines of f (modified from somewhere on the internet)
    n = str(n)
    p = subprocess.Popen(["tail", "-n", n, f], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    lines = stdout.splitlines()
    # convert bytes to strings
    lines = [l.decode("utf-8") for l in lines]
    return lines


def binarySortM1(folder):
    M1 = float(folder.split("M1_")[-1].split("M2_")[0])
    return M1


def scrub(logName):
    # this uses the log_scrubber.py script from Bill Wolf
    # which is available here: https://zenodo.org/record/2619282
    print("... let me scrub this for you")
    # dirty fix for PPI ejecta files
    if "ejecta.data" in sys.argv[1]:
        dataStart = 1
    else:
        dataStart = 6
    ###################################################################
    # THIS SHOULDN'T NEED TO BE TOUCHED UNLESS YOU ARE SPEEDING IT UP #
    ###################################################################
    # Pull original data from history file
    f = open(logName, "r")
    fileLines = f.readlines()
    f.close()
    headerLines = fileLines[:dataStart]
    dataLines = fileLines[dataStart:]
    # Determine which column is the model_number column
    headers = shlex.split(headerLines[dataStart - 1])
    modelNumberCol = headers.index("model_number")
    # Get list of model numbers
    modelNumbers = [-1] * len(dataLines)
    for i in range(len(dataLines)):
        data = shlex.split(dataLines[i])
        modelNumbers[i] = int(float(data[modelNumberCol]))
    # Pick "good" data points from the end to the beginning
    modelNumbers.reverse()
    dataLines.reverse()
    dataOut = []
    for i in range(len(modelNumbers)):
        if len(dataOut) == 0:
            dataOut.append(dataLines[i])
            lastGoodModelNumber = modelNumbers[i]
            #        print 'model_number = ', modelNumbers[i], ': Accepted!'
        elif modelNumbers[i] < lastGoodModelNumber:
            dataOut.append(dataLines[i])
            lastGoodModelNumber = modelNumbers[i]
            #        print 'model_number = ', modelNumbers[i], '<', lastGoodModelNumber, ': Accepted!'
            # else:
            #        print 'model_number = ', modelNumbers[i], '>=', lastGoodModelNumber, ': REJECTED!'
    # Properly reorder data and make combined output list of lines
    dataOut.reverse()
    fileLinesOut = headerLines + dataOut
    # Output ordered data back into history file
    f = open(logName, "w")
    for line in fileLinesOut:
        f.write(line)
    f.close()
    print("Data in", logName, "has been scrubbed.")

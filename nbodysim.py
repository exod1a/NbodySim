### @file   nbodysim.py
### @author Chandler Ross
### @date   March 17, 2020
### @brief  The main driver file to execute code from all the modules in this directory for the N body simulation
import ctypes
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import math as m
import timeit

from init_cond import *
from runPlot import *

# Parameters for simulation			
dt = 0.05																   # default time step (arbitrary)
n = 1																	   # Lowers the time step for each call to A1 and A2. Also more calls
numSteps = 1000															   # default number of time steps to take (arbitrary)
fileName = "particleInfo1.txt"											   # file to read initial conditions from
File = open(fileName, "r")
lines = File.readlines()
numParticles = len(lines) - 1 										       # number of particles in simulation
File.close()
nullVec = np.array([0,0,0])
r = np.array([nullVec for i in np.arange(numParticles)], dtype=np.double)  # array to hold positions of particles
v = np.array([nullVec for i in np.arange(numParticles)], dtype=np.double)  # array to hold velocities of particles
m = np.array([0 for i in np.arange(numParticles)], dtype=np.double)        # array to hold masses of particles

# set ICs
r, v, m = initial_Conditions(r, v, m, fileName)

# make plot output
runPlot(r, v ,m, numSteps, numParticles, dt, n)

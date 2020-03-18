### @file   nbodysim.py
### @author Chandler Ross
### @date   March 17, 2020
### @brief  The main driver file to execute code from all the modules in this directory for the N body simulation
import ctypes
import numpy as np
from init_cond import *
drift = ctypes.CDLL('./A1.so')
kickA = ctypes.CDLL('./A2.so')

# Parameters for simulation			
dt = 0.05																   # default time step (arbitrary)
numSteps = 50															   # default number of time steps to take (arbitrary)
fileName = "particleInfo1.txt"											   # file to read initial conditions from
File = open(fileName, "r")
lines = File.readlines()
numParticles = len(lines) - 1 										       # number of particles in simulation
File.close()
nullVec = np.array([0,0,0])
r = np.array([nullVec for i in np.arange(numParticles)], dtype=np.double)  # array to hold positions of particles
v = np.array([nullVec for i in np.arange(numParticles)], dtype=np.double)  # array to hold velocities of particles
m = np.array([0 for i in np.arange(numParticles)], dtype=np.double)        # array to hold masses of particles

r, v, m = initial_Conditions(r, v, m, fileName)

drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
		 ctypes.c_double(dt), ctypes.c_uint(numParticles))

# parameters to put into A2 loop to avoid re-allocating every time
r_eff = np.array([r[0],[0,0,0]], dtype=np.double)					       # array to hold posn of part_0 and part_i 
dirvec = np.array([0,0,0], dtype=np.double)								   # array to find direction vector along part_i to part_0
acc = np.array([0 for i in np.arange(numParticles)], dtype=np.double)	   # array to hold acceleration on part_0 due to part_i

kickA.A2(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
         m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(dt), ctypes.c_uint(numParticles),  \
		 r_eff.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
		 acc.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

print(r)
print(v)
print(r)

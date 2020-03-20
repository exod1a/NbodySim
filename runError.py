### @file   runError.py
### @author Chandler Ross
### @date   March 19, 2020
### @brief  Plots the error for the method as well as the run time.

import ctypes
import math as M
import numpy as np
import matplotlib.pyplot as plt
import timeit

drift = ctypes.CDLL('./A1.so')
kickA = ctypes.CDLL('./A2.so')
kickB = ctypes.CDLL('./B.so')
nrg   = ctypes.CDLL('./energy.so')
nrg.energy.restype = ctypes.c_double  												# so that it returns a double

# parameters
time = 1																			# total time to run for each of the time steps
dirvec = np.array([0,0,0], dtype=np.double)											# array to find direction vector along particle j to particle i
timeStep_iter = np.linspace(0.00001,1,100)											# loop over time steps
numSteps = np.array([time/i for i in timeStep_iter], dtype=np.double)				# number of steps to reach the total time
rel_err = np.array([0 for i in np.arange(len(timeStep_iter))], dtype=np.double)		# largest relative error
start = np.array([0 for i in np.arange(len(timeStep_iter))], dtype=np.double)		# for where we start the run time clock
stop = np.array([0 for i in np.arange(len(timeStep_iter))], dtype=np.double)		# for where we end the run time clock
runTime = np.array([0 for i in np.arange(len(timeStep_iter))], dtype=np.double)		# the total run time

### @brief Module computes the error and run time and plots the output.
### @param      r         A 2D array: 1st dimension is the number of particles, 2nd is their positions in 3D space.
### @param      v         A 2D array: 1st dimension is the number of particles, 2nd is their velocities in 3D space.
### @param      m         A 1D array: contains the masses for particle 0, 1, ..., N-1.
### @param    numSteps    Integer > 0... The number of times the loop iterates. Sets how long the simulation runs.
### @param  numParticles  The number of particles ie. the size of the first index of r and v.
### @param      n         Integer > 0... Lower the timestep and how many times you call A1 and A2.
def runError(r, v, m, numParticles, n):
	
	# initial energy
	E0 = nrg.energy(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
					m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_uint(numParticles))                                                                 

	for i in np.arange(len(timeStep_iter)):
        
		# Holds relative error for each time step
		rel_err_iter = np.array([0 for k in np.arange(int(M.ceil(numSteps[i])))], dtype=np.double)
                                
		start[i] = timeit.default_timer()

		for j in np.arange(int(M.ceil(numSteps[i]))):
        
			# one full time step
			for k in np.arange(n):
				drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
                    	 ctypes.c_double(timeStep_iter[i]/(n*4.)), ctypes.c_uint(numParticles))

				kickA.A2(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
                    	 m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(timeStep_iter[i]/(n*2.)), ctypes.c_uint(numParticles),  \
                    	 dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

				drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
                    	 ctypes.c_double(timeStep_iter[i]/(n*4.)), ctypes.c_uint(numParticles))

			# dirvec will now hold the direction vector along particle j to particle i

			kickB.B(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
               	    m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(timeStep_iter[i]), ctypes.c_uint(numParticles),  \
               	    dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

			for k in np.arange(n):
				drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
                     	 ctypes.c_double(timeStep_iter[i]/(n*4.)), ctypes.c_uint(numParticles))

				kickA.A2(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
                  	     m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(timeStep_iter[i]/(n*2.)), ctypes.c_uint(numParticles),  \
                    	 dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

				drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
                    	 ctypes.c_double(timeStep_iter[i]/(n*4.)), ctypes.c_uint(numParticles))

			E = nrg.energy(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
                           m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_uint(numParticles))
			
			rel_err_iter[j] = abs((E0 - E) / E0)

		stop[i] = timeit.default_timer()
		runTime[i] = stop[i] - start[i]
    
		rel_err[i] = max(rel_err_iter)

	return runTime, rel_err

### @file   nbodysim.py
### @author Chandler Ross
### @date   March 19, 2020
### @brief  Plots the error for the method as well as the run time.

import ctypes
import math as M
import numpy as np
import matplotlib.pyplot as plt
import timeit

from energy import *
drift = ctypes.CDLL('./A1.so')
kickA = ctypes.CDLL('./A2.so')
kickB = ctypes.CDLL('./B.so')

### @brief Module computes the method and plots the output.
### @param      r         A 2D array: 1st dimension is the number of particles, 2nd is their positions in 3D space.
### @param      v         A 2D array: 1st dimension is the number of particles, 2nd is their velocities in 3D space.
### @param      m         A 1D array: contains the masses for particle 0, 1, ..., N-1.
### @param    numSteps    Integer > 0... The number of times the loop iterates. Sets how long the simulation runs.
### @param  numParticles  The number of particles ie. the size of the first index of r and v.
### @param     time       Total time simulation will run for e.g. dt=0.05, time=1 then numSteps = 1/0.05 = 20.
### @param      n         Integer > 0... Lower the timestep and how many times you call A1 and A2.
def runError(r, v, m, numParticles, time, n):

	# array to find direction vector along particle j to particle i
	dirvec = np.array([0,0,0], dtype=np.double)
	
	# Loop over time steps
	timeStep_iter = np.linspace(0.00001,1,100)

	numSteps = np.array([time/i for i in timeStep_iter], dtype=np.double)

	# Largest relative error
	rel_err = np.array([0 for i in np.arange(len(timeStep_iter))], dtype=np.double)

	# For run time
	start = np.array([0 for i in np.arange(len(timeStep_iter))], dtype=np.double)
	stop = np.array([0 for i in np.arange(len(timeStep_iter))], dtype=np.double)

	# To hold the run time for each time step
	runTime = np.array([0 for i in np.arange(len(timeStep_iter))], dtype=np.double)

	# Initial energy
	E0 = energy(r,v,m)

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
			
			rel_err_iter[j] = abs((E0-energy(r,v,m))/E0)

		stop[i] = timeit.default_timer()
		runTime[i] = stop[i] - start[i]
    
		rel_err[i] = max(rel_err_iter)

	plt.figure(2)   
	plt.loglog(timeStep_iter,rel_err,label='HR')
	plt.legend(loc='best')
	plt.xlabel('Time Step')
	plt.ylabel('Relative Error')    
    
	plt.figure(3)    
	plt.loglog(runTime,rel_err,label='HR')
	plt.legend(loc='best')
	plt.xlabel('Run Time')
	plt.ylabel('Relative Error')
    
	plt.show()

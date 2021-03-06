### @file   nbodysim.py
### @author Chandler Ross
### @date   March 17, 2020
### @brief  The main driver file to execute code from all the modules in this directory for the N body simulation
import ctypes
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import math as M
import timeit

np.set_printoptions(formatter={'float': lambda x: "{0:0.15f}".format(x)})

from init_cond import initial_Conditions
from runPlot import runPlot
from runLFPlot import runLFPlot
from runError import runError
from runLFError import runLFError

# Parameters for simulation
flag = "-"								   				# decide what part of program to execute... -p = plot, -e = error			
dt = 0.05									   			# default time step (arbitrary)
n = 1													# Lowers the time step for each call to A1 and A2. Also more calls
numSteps = 500											# default number of time steps to take (arbitrary)
fileName = "particleInfo2.txt"			 	 			# file to read initial conditions from
File = open(fileName, "r")
lines = File.readlines()
numParticles = len(lines) - 1 			       			# number of particles in simulation
File.close()
r = np.zeros((numParticles,3))				  			# array to hold positions of particles
v = np.zeros((numParticles,3))  						# array to hold velocities of particles
m = np.zeros(numParticles)	        					# array to hold masses of particles
dirvec = np.zeros(3)						  			# array to find direction vector along particle j to particle i
timeStep_iter = np.logspace(-4,0,100)                   # loop over time steps
runTime = np.zeros(len(timeStep_iter))     				# the total run time
rel_err = np.zeros(len(timeStep_iter))     				# largest relative error
runTimeLF = np.zeros(len(timeStep_iter))   				# the total run time for LF
rel_errLF = np.zeros(len(timeStep_iter))   				# largest relative error for LF

# set ICs
r, v, m = initial_Conditions(r, v, m, fileName)

if flag == "-p":
	r, v, m = initial_Conditions(r, v, m, fileName)
	# make plot output
	runPlot(r, v ,m, numSteps, numParticles, dt, n)

elif flag=="-pLF":
    r, v, m = initial_Conditions(r, v, m, fileName)
    runLFPlot(r, v, m, numSteps, numParticles, dt, n)

elif flag == "-e":
	# make error and run time plot
	runTime, rel_err = runError(r, v, m, numParticles, n)
	
	plt.figure(2)
	plt.loglog(timeStep_iter,rel_err, label='HR')
	plt.legend(loc='best')
	plt.xlabel('Time Step')
	plt.ylabel('Relative Error')

	plt.figure(3)
	plt.loglog(runTime,rel_err, label='HR')
	plt.legend(loc='best')
	plt.xlabel('Run Time')
	plt.ylabel('Relative Error')

	plt.show()

elif flag == "-LFc":
	# compare Hanno's method to LF
	runTime, rel_err = runError(r, v, m, numParticles, n)
	r, v, m = initial_Conditions(r, v, m, fileName)
	runTimeLF, rel_errLF = runLFError(r, v, m, numParticles, n)

	plt.figure(2)
	plt.loglog(timeStep_iter,rel_err, label='HR')
	plt.loglog(timeStep_iter,rel_errLF, label='LF')
	plt.legend(loc='best')
	plt.xlabel('Time Step')
	plt.ylabel('Relative Error')

	plt.figure(3)
	plt.loglog(runTime,rel_err, label='HR')
	plt.loglog(runTime,rel_errLF, label='LF')
	plt.legend(loc='best')
	plt.xlabel('Run Time')
	plt.ylabel('Relative Error')

	plt.show()

drift = ctypes.CDLL('./A1.so')
kickA = ctypes.CDLL('./A2.so')
kickB = ctypes.CDLL('./B.so')
	
for i in np.arange(numSteps):
	for k in np.arange(n):
		drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
				 ctypes.c_double(dt/(n*4.)), ctypes.c_uint(numParticles))

		#print("After A1")
		#print("r\n")
		#print(r)

		kickA.A2(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
				 m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(dt/(n*2.)), ctypes.c_uint(numParticles),  \
				 dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

		#print("After A2")
		#print("v\n")
		#print(v)

		drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
				 ctypes.c_double(dt/(n*4.)), ctypes.c_uint(numParticles))

		#print("After A1")
		#print("r\n")
		#print(r)

		# dirvec will now hold the direction vector along particle j to particle i

	kickB.B(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
			m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(dt), ctypes.c_uint(numParticles),  \
			dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

	#print("After B")
	#print("v\n")
	#print(v)

	for k in np.arange(n):
		drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
				 ctypes.c_double(dt/(n*4.)), ctypes.c_uint(numParticles))

		#print("After A1")
		#print("r\n")
		#print(r)
		kickA.A2(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
				 m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(dt/(n*2.)), ctypes.c_uint(numParticles),  \
				 dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

		#print("After A2")
		#print("v\n")
		#print(v)
		drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
				 ctypes.c_double(dt/(n*4.)), ctypes.c_uint(numParticles))

		#print("After A1")
		#print("r\n")
		#print(r)

#print("After {} time step(s):".format(numSteps))
#print("r")
#print(r)
#print("v")
#print(v)

#print(numParticles % 32)

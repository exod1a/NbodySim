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
drift = ctypes.CDLL('./A1.so')
kickA = ctypes.CDLL('./A2.so')
kickB = ctypes.CDLL('./B.so')

# Parameters for simulation			
dt = 0.05																   # default time step (arbitrary)
numSteps = 1															   # default number of time steps to take (arbitrary)
fileName = "particleInfo1.txt"											   # file to read initial conditions from
File = open(fileName, "r")
lines = File.readlines()
numParticles = len(lines) - 1 										       # number of particles in simulation
File.close()
nullVec = np.array([0,0,0])
r = np.array([nullVec for i in np.arange(numParticles)], dtype=np.double)  # array to hold positions of particles
v = np.array([nullVec for i in np.arange(numParticles)], dtype=np.double)  # array to hold velocities of particles
m = np.array([0 for i in np.arange(numParticles)], dtype=np.double)        # array to hold masses of particles

# parameters to put into A2 loop to avoid re-allocating every time
r_eff = np.array([r[0],[0,0,0]], dtype=np.double)                          # array to hold posn of part_0 and part_i
dirvec = np.array([0,0,0], dtype=np.double)                                # array to find direction vector along part_i to part_0

# set ICs
r, v, m = initial_Conditions(r, v, m, fileName)

def runPlot(r, v, m, numSteps, numParticles):

	acc = np.array([0 for i in np.arange(numParticles)], dtype=np.double)      # array to hold acceleration on part_0 due to part_i

	# Store the updated values 
	# Format: Rx = [x01,x11,...,xN1,x02,x12,...,xN2,...]
	# First digit is the particle, second is the time step
	Rx = np.zeros(numSteps*numParticles,dtype=float)
	Ry = np.zeros(numSteps*numParticles,dtype=float)
	Rz = np.zeros(numSteps*numParticles,dtype=float)

	for i in np.arange(numSteps):
		for j in np.arange(numParticles):            
			# x,y and z components of each planet 
			# for each time step
			Rx[numParticles*i+j] = r[j][0]
			Ry[numParticles*i+j] = r[j][1]
			Rz[numParticles*i+j] = r[j][2]

		drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
				 ctypes.c_double(dt/4.), ctypes.c_uint(numParticles))

		kickA.A2(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
         	 	 m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(dt/2.), ctypes.c_uint(numParticles),  \
		 	 	 r_eff.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
		 	 	 acc.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

		"""drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
             	 ctypes.c_double(dt/4.), ctypes.c_uint(numParticles))

		# r_eff will now hold the posn of particle i and particle j
		# dirvec will now hold the direction vector along particle j to particle i
		# acc will now be 2D and hold all the accelerations on every particle that isn't
		# particle 0 due to the presence of the other particles.

		acc = np.array([nullVec for i in np.arange(numParticles)], dtype=np.double)

		kickB.B(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
         		m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(dt), ctypes.c_uint(numParticles),  \
         		r_eff.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
        		acc.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

		drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
             	 ctypes.c_double(dt/4.), ctypes.c_uint(numParticles))

		acc = np.array([0 for i in np.arange(numParticles)], dtype=np.double)

		kickA.A2(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
             	 m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(dt/2.), ctypes.c_uint(numParticles),  \
             	 r_eff.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
             	 acc.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

		drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
             	 ctypes.c_double(dt/4.), ctypes.c_uint(numParticles))
		
	fig = plt.figure(1)
	ax = fig.add_subplot(111,projection='3d')
	for i in np.arange(numParticles):
		ax.plot(Rx[i::numParticles],Ry[i::numParticles],Rz[i::numParticles])
	plt.title("Real Space N Body Problem")
	ax.set_xlabel('x')
	ax.set_ylabel('y')    
	ax.set_zlabel('z')    

	plt.show()"""
	print(v)

runPlot(r, v ,m, numSteps, numParticles)

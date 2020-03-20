# runLFPlot.py
import ctypes
import numpy as np
import matplotlib.pyplot as plt

drift = ctypes.CDLL('./A1.so')
LFkick = ctypes.CDLL('./LF_U.so')

def runLFPlot(r, v, m, numSteps, numParticles, dt, n):
	# Store the updated values
	# Format: Rx = [x01,x11,...,xN1,x02,x12,...,xN2,...]
	# First digit is the particle, second is the time step
	Rx = np.zeros(numSteps*numParticles, dtype=np.double)
	Ry = np.zeros(numSteps*numParticles, dtype=np.double)
	Rz = np.zeros(numSteps*numParticles, dtype=np.double)

	# array to find direction vector along particle j to particle i
	dirvec = np.array([0,0,0], dtype=np.double)

	for i in np.arange(numSteps):
		for j in np.arange(numParticles):
			# x,y and z components of each planet
			# for each time step
			Rx[numParticles*i+j] = r[j][0]
			Ry[numParticles*i+j] = r[j][1]
			Rz[numParticles*i+j] = r[j][2]

		# one full time step
		for k in np.arange(n):
			drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
             	     ctypes.c_double(dt/(n*2.)), ctypes.c_uint(numParticles))

		# dirvec will now hold the direction vector along particle j to particle i
		LFkick.LF_U_Op(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
             	       m.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), ctypes.c_double(dt), ctypes.c_uint(numParticles), \
                 	   dirvec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

		for k in np.arange(n):
			drift.A1(r.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), v.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), \
             	     ctypes.c_double(dt/(n*2.)), ctypes.c_uint(numParticles))

	fig = plt.figure(1)
	ax = fig.add_subplot(111, projection='3d')
	for i in np.arange(numParticles):
		ax.plot(Rx[i::numParticles],Ry[i::numParticles],Rz[i::numParticles])
	plt.title("Real Space N Body Problem: Leap Frog")
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')

	plt.show()


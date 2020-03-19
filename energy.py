### @file   energy.py
### @author Chandler Ross
### @date   March 19, 2020
### @brief  Calculate the energy of an N body system in gravitational potential.
import numpy as np
from numpy import linalg as LA  # for norm

### @brief Calculate the energy of an N body system in gravitational potential.
### @param  r  
### @param  v  
### @param  m  
def energy(r,v,m):
    
	# T = kinetic energy, U = potential energy
	T = np.array([0 for i in np.arange(len(r))], dtype=np.double)
	U = np.array([0 for i in np.arange(len(r))], dtype=np.double)
    
	# Calculate kinetic energy
	for i in np.arange(len(r)):
		T[i] = 0.5*m[i]*LA.norm(v[i])**2
    
	# Calculate potential energy
	for i in np.arange(len(r)):
		for j in np.arange(len(r)):
			if j > i:
				eff_r = r[i:j+1:j-i]
				U[i] -= m[i]*m[j]/(LA.norm(eff_r[0]-eff_r[1]))
			else:
				continue
	# Total energy
	E = np.sum(T)+np.sum(U)
    
	return E

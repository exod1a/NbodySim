import math

def LFnew(r, v, m, numParticles, dt):

	x,y,z,vx,vy,vz=[],[],[],[],[],[]	
	for i in range(numParticles):
		x.append(r[i][0])
		y.append(r[i][1])
		z.append(r[i][2])
		vx.append(v[i][0])
		vy.append(v[i][1])
		vz.append(v[i][2])	

	for i in xrange(numParticles):
		x[i] += vx[i] * dt/2.
		y[i] += vy[i] * dt/2.
		z[i] += vz[i] * dt/2.
	for i in xrange(numParticles):
		ax = 0.
		ay = 0.
		az = 0.
		for j in xrange(numParticles):
			if i!=j:
				dx = x[i] - x[j]
				dy = y[i] - y[j]
				dz = z[i] - z[j]
				r = math.sqrt(dx * dx + dy * dy + dz * dz)
				a = m[j]/(r*r)
				ax += a/r * dx
				ay += a/r * dy
				az += a/r * dz
		vx[i] += ax * dt
		vy[i] += ay * dt
		vz[i] += az * dt
	for i in xrange(numParticles):
		x[i] += vx[i] * dt/2.
		y[i] += vy[i] * dt/2.
		z[i] += vz[i] * dt/2.

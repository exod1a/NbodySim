// B.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Compute the B step
void B(double r[][3], double v[][3], double m[], double dt, int numParticles, double r_eff[2][3], double dirvec[], double acc[][3])
{
	for (int i = 1; i < numParticles; i++)
    {
		// i th particle position
		for (int j = 0; j < 3; j++)
		{
			r_eff[0][j] = r[i][j];
        }
		// j th particle position, direction vector and sum of accelerations
		for (int j = i+1; j < numParticles; j++)
        {
			for (int k = 0; k < 3; k++)
			{
            	r_eff[1][k] = r[j][k];
				dirvec[k] = r[i][k] - r[j][k];
        	
				acc[i][k] -= m[j] / (pow(pow(dirvec[0],2) + pow(dirvec[1], 2) + pow(dirvec[2],2), 3./2.)) * dirvec[k]; 
				acc[j][k] += (acc[i][k] / m[j]) * m[i];
			}
		}
	}
	// update velocities of particles i -> N
    for (int i = 1; i < numParticles; i++)
    {
		for (int j = 0; j < 3; j++)
		{
        	v[i][j] += acc[i][j] * dt;
    	}
	}
}

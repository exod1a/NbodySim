// A2.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Compute the A2 step
void A2(double r[][3], double v[][3], double m[], double dt, int numParticles, double r_eff[2][3], double dirvec[], double acc[])
{
	for (int i = 1; i < numParticles; i++)
	{
		for (int j = 0; j < 3; j++)
		{
			r_eff[1][j] = r[i][j];
			dirvec[j] = r[0][j] - r[i][j];
		}
		// update particles 1 -> N		
		for (int j = 0; j < 3; j++)
		{
			v[i][j] += m[0] / (pow(pow(dirvec[0],2) + pow(dirvec[1], 2) + pow(dirvec[2],2), 3./2.)) * dirvec[j];

			// -1 to accound for direction along 0 to 1 instead of 1 to 0
			acc[j] -= (v[i][j] / m[0]) * m[i];				
		}
	}
	// update particle 0
	for (int i = 0; i < 3; i++)
	{
		v[0][i] += acc[i] * dt;
	}
}

#include <stdio.h>
#include "energy.h"

int main()
{
    int E;
    float r[4] = {1,2,3,4};
    float v[4] = {4,3,2,1};
    float m[4] = {1,1,1,1};    

    E = energy(r, v, m);

    return 0;
}

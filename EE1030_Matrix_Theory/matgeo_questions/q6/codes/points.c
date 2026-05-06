#include <stdlib.h>
#include <math.h>
#include "../../c_code/funcs.h"

float **pointsGet(){
    float **pts = (float **) malloc(sizeof(float *) * 3); 

    for (int i = 0; i < 3; i++) {
        pts[i] = (float *) malloc(sizeof(float) * 3 * 2);
    }

    // A
    pts[0][0] = (float) 5/2;
    pts[0][1] = (float) 5*sqrt(3)/2;
    // B
    pts[1][0] = 0;
    pts[1][1] = 0;
    // C 
    pts[2][0] = 6;
    pts[2][1] = 0;

    return pts; 
}
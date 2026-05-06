#include <stdlib.h>
#include <math.h>
#include "../../c_code/funcs.h"

float **pointsGet(){
    float **pts = (float **) malloc(sizeof(float *) * 1); 

    for (int i = 0; i < 1; i++) {
        pts[i] = (float *) malloc(sizeof(float) * 2);
    }

    // O
    pts[0][0] = 0;
    pts[0][1] = 0;

    return pts; 
}
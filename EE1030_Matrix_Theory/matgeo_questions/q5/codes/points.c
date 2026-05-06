#include <stdlib.h>
#include "../../c_code/funcs.h"

float **pointsGet(){
    float **pts = (float **) malloc(sizeof(float *) * 3); 

    for (int i = 0; i < 3; i++) {
        pts[i] = (float *) malloc(sizeof(float) * 3);
    }


    pts[0][0] = 2;
    pts[0][1] = -1;
    pts[0][2] = 2;

    pts[1][0] = (float) 2/3;
    pts[1][1] = (float) -1/3;
    pts[1][2] = (float) 2/3;

    pts[2][0] = 0; 
    pts[2][1] = 0; 
    pts[2][2] = 0; 

    return pts; 
}

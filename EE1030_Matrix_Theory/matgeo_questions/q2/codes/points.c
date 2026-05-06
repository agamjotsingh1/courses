#include <stdlib.h>

float **pointsGet(){
    float **pts = (float **) malloc(sizeof(float *) * 2); 

    for (int i = 0; i < 2; i++) {
        pts[i] = (float *) malloc(sizeof(float) * 2 * 2);
    }

    pts[0][0] = 1;
    pts[0][1] = 2;
    pts[1][0] = 7;
    pts[1][1] = 0;

    return pts; 
}

float **lineGet(int n, float x1, float x2, float a, float b, float c) {
    float **pts = (float **) malloc(sizeof(float *) * n); 

    for(int i = 0; i < n; i++){
        pts[i] = (float *) malloc(sizeof(float) * 2 * n);
        pts[i][0] = x1 + ((x2 - x1)*i)/n; 
        pts[i][1] = -(c + a*pts[i][0])/b; 
    }

    return pts;
}

void free_multi_memory(float **arr, int n){
    for (int i = 0; i < n; i++){
        free(arr[i]);
    }

    free(arr);
}
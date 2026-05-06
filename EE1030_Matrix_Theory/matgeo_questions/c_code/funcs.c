#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "funcs.h"

#define PI 3.14159265358979323846 

float **lineFromPts3D(int n, float x1, float y1, float z1, float x2, float y2, float z2) {
    float **pts = (float **) malloc(sizeof(float *) * n); 

    for(int i = 0; i < n; i++){
        pts[i] = (float *) malloc(sizeof(float) * 3);
        pts[i][0] = x1 + ((x2 - x1)*i)/n; 
        pts[i][1] = y1 + ((y2 - y1)*i)/n; 
        pts[i][2] = z1 + ((z2 - z1)*i)/n; 
    }

    return pts;
}


float **lineFromPts2D(int n, float x1, float y1, float x2, float y2) {
    float **pts = (float **) malloc(sizeof(float *) * n); 

    for(int i = 0; i < n; i++){
        pts[i] = (float *) malloc(sizeof(float) * 2);
        pts[i][0] = x1 + ((x2 - x1)*i)/n; 
        pts[i][1] = y1 + ((y2 - y1)*i)/n; 
    }

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

float **circleGet(int n, float x, float y, float r) {
    float **pts = (float **) malloc(sizeof(float *) * n); 
    float theta = 0;
    for(int i = 0; i < n; i++){
        pts[i] = (float *) malloc(sizeof(float) * 2 * n);
        pts[i][0] = x + r*cos(theta);
        pts[i][1] = y + r*sin(theta);
        theta += 2*PI/n;
    }
    return pts;
}

float **normPlot(int n, int p, float x, float y, float r) {
    float **relpts = (float **) malloc(sizeof(float *) * n); 
    float dx = r/n;

    for(int i = 0; i < n; i++){
        relpts[i] = (float *) malloc(sizeof(float) * 2);

        relpts[i][0] = i*dx; 
        relpts[i][1] = pow(pow(r, p) - pow(i*dx, p), (double) 1/p); 
    }

    return relpts;
}

float **triGet(int n, float x1, float y1, float x2, float y2, float x3, float y3) {
    float **pts = (float **) malloc(sizeof(float *) * 3*n); 
    float **linePts1 = lineFromPts2D(n, x1, y1, x2, y2); 
    float **linePts2 = lineFromPts2D(n, x3, y3, x2, y2); 
    float **linePts3 = lineFromPts2D(n, x1, y1, x3, y3); 

    for(int i = 0; i < 3*n; i++){
        pts[i] = (float *) malloc(sizeof(float *) * 2);
        if(i < n){
            pts[i][0] = linePts1[i][0];
            pts[i][1] = linePts1[i][1];
        }
        else if(i >= n & i < 2*n){
            pts[i][0] = linePts2[i - n][0];
            pts[i][1] = linePts2[i - n][1];
        }
        else {
            pts[i][0] = linePts3[i - 2*n][0];
            pts[i][1] = linePts3[i - 2*n][1];
        }
    }

    return pts;
}

void free_multi_memory(float **arr, int n){
    for (int i = 0; i < n; i++){
        free(arr[i]);
    }

    free(arr);
}




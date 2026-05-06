#ifndef FUNCS_H_
#define FUNCS_H_

float **lineGet(int, float, float, float, float, float);
float **triGet(int, float, float, float, float, float, float);
float **lineFromPts3D(int, float, float, float, float, float, float);
float **lineFromPts2D(int, float, float, float, float);
float **pointsGet();
float **normPlot(int, int, float, float, float);
float **circleGet(int, float, float, float);
void free_multi_memory(float**, int);

#endif

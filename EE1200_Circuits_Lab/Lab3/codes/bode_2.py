import numpy as np
import matplotlib.pyplot as plt

def bode_amp(R, C, w_start, w_end, h):
    w = np.linspace(w_start, w_end, int((w_end - w_start)/h))
    log_w = np.log10(w)
    log_amp = -(np.log10((1-(w*R*C)**2)**2+9*(w*R*C)**2))/2
    return log_w, log_amp

def bode_phase(R, C, w_start, w_end, h):
    w = np.linspace(w_start, w_end, int((w_end - w_start)/h))
    log_w = np.log10(w)
    phase = -np.arctan((3*w*R*C)/(1-(w*R*C)**2))
    return log_w, phase

R = 1e3
C = 88*1e-9
h = 10
w_start = 1
w_end = 1e7

#plt.figure()
#plt.plot(*bode_amp(R, C, w_start, w_end, h))

with open("./vals_2.txt", "r") as file:
    lines = file.readlines()
    lines.pop(0)
    for l in lines:
        f, v, dt = l.split()
        f = float(f)
        v = float(v)
        if dt == "0":
            continue
        dt = float(dt)*(1e-6)
        
        #plt.scatter(np.log10(2*(np.pi)*f), np.log10(v), color="orange")
        plt.scatter(np.log10(2*np.pi*f), np.arctan(np.tan(-2*np.pi*f*dt)), color="orange")
        #plt.scatter(np.log10(2*np.pi*f), (-2*np.pi*f*dt), color="orange")

#plt.show()
#plt.scatter(np.log10(2*np.pi*10), -2*np.pi*10*0.2*1e-3)
#plt.scatter(np.log10(2*np.pi*50), -2*np.pi*50*0.2*1e-3)
#plt.scatter(np.log10(2*np.pi*100), -2*np.pi*100*0.08*1e-3)

#plt.figure()
plt.plot(*bode_phase(R, C, w_start, w_end, h))
plt.show()


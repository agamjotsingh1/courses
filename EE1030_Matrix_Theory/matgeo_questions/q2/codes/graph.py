import sys                                          #for path to external scripts
sys.path.insert(0, './CoordGeo')        #path to my scripts
import numpy as np
import mpmath as mp
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import ctypes

#dll linking
dll = ctypes.CDLL('./points.so')

dll.pointsGet.argtypes = None
dll.pointsGet.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_float))

n = 1000 #no of points to plot for given line
dll.lineGet.argtypes = [ctypes.c_int] + [ctypes.c_float] * 5
dll.lineGet.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_float))
pts = dll.pointsGet() 

#local imports
from line.funcs import *
from triangle.funcs import *
from conics.funcs import circ_gen

#Given Points
A = np.array([[pts[0][0], pts[0][1]]]).reshape(-1,1) 
B = np.array([[pts[1][0], pts[1][1]]]).reshape(-1,1) 

#Line parameters
x1 = -2.5
x2 = 10
a = 1
b = 3
c = -7

#Generating Lines
line_pts = dll.lineGet(n, x1, x2, a, b, c)

#Plotting all lines
coords = []
for pt in line_pts[:n]:
    coords.append(np.array([[pt[0], pt[1]]]).reshape(-1, 1))

coords = np.block(coords)
plt.scatter(coords[0,:], coords[1,:], marker=".")

#Labeling the coordinates
tri_coords = np.block([A, B])
plt.scatter(tri_coords[0,:], tri_coords[1,:])
vert_labels = ['A', 'B']
for i, txt in enumerate(vert_labels):
    plt.annotate(f'{txt}\n({tri_coords[0,i]:.0f}, {tri_coords[1,i]:.0f})',
                 (tri_coords[0,i], tri_coords[1,i]), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(-10,-5), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center


dll.free_multi_memory(line_pts, n)
dll.free_multi_memory(pts, 2)

# use set_position
ax = plt.gca()
ax.spines['top'].set_color('none')
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
'''
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
plt.xlabel('$x$')
plt.ylabel('$y$')
'''
plt.legend(loc='best')
plt.grid() # minor
plt.axis('equal')
plt.savefig('../figs/graph.png')
plt.show()
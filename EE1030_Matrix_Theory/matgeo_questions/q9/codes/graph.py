import sys                                          #for path to external scripts
sys.path.insert(0, './CoordGeo')        #path to my scripts
import numpy as np
import mpmath as mp
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import ctypes
import math

#dll linking
dll = ctypes.CDLL('./points.so')

dll.pointsGet.argtypes = None
dll.pointsGet.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_float))

n = 1000 #no of points to plot for given line

dll.lineGet.argtypes = [ctypes.c_int] + [ctypes.c_float] * 5
dll.lineGet.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_float))

dll.circleGet.argtypes = [ctypes.c_int] + [ctypes.c_float] * 3
dll.circleGet.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_float))

pts = dll.pointsGet() 

#local imports
from line.funcs import *
from triangle.funcs import *
from conics.funcs import circ_gen

#Given Points
O = np.array([[pts[0][0], pts[0][1]]]).reshape(-1,1) 

#Circle and line parameters
x = O[0]
y = O[1]
r = 2

k1 = -7
k2 = 1
a = 1
b = 3
c = 0

#Generating Lines and Circles
circle_pts = dll.circleGet(n, x, y, r)
line_pts = dll.lineGet(n, k1, k2, a, b, c)

#Shading the region
plt.fill_between([sub[0] for sub in circle_pts[:int(n/2)]], [sub[1] for sub in circle_pts[:int(n/2)]], [0]*int(n/2), color="orange", label="D")

#Plotting the circle
coords = []
for pt in circle_pts[:n]:
    coords.append(np.array([[pt[0], pt[1]]]).reshape(-1, 1))

coords_plot = np.block(coords)
plt.scatter(coords_plot[0,:], coords_plot[1,:], marker=".", label = "Circle", color="royalblue")

#Labeling the coordinates
tri_coords = np.block([O])
plt.scatter(tri_coords[0,:], tri_coords[1,:])
vert_labels = ['O']
for i, txt in enumerate(vert_labels):
    plt.annotate(f'{txt}\n({tri_coords[0,i]:.0f}, {tri_coords[1,i]:.0f})',
                 (tri_coords[0,i], tri_coords[1,i]), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(10,-20), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center


dll.free_multi_memory(circle_pts, n)
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
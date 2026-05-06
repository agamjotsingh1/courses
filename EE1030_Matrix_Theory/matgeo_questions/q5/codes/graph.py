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
dll.lineFromPts.argtypes = [ctypes.c_int] + [ctypes.c_float] * 6
dll.lineFromPts.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_float))
pts = dll.pointsGet() 

#local imports
from line.funcs import *
from triangle.funcs import *
from conics.funcs import circ_gen

#Given Points
A = np.array([[pts[0][0], pts[0][1], pts[0][2]]]).reshape(-1,1) 
B = np.array([[pts[1][0], pts[1][1], pts[1][2]]]).reshape(-1,1) 
O = np.array([[pts[2][0], pts[2][1], pts[2][2]]]).reshape(-1,1) 

#Generating Lines
line_pts = dll.lineFromPts(n, pts[0][0], pts[0][1], pts[0][2], pts[2][0], pts[2][1], pts[2][2])

# Create a figure and a 3D Axes
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

#Plotting all lines
coords = []
for pt in line_pts[:n]:
    coords.append(np.array([[pt[0], pt[1], pt[2]]]).reshape(-1, 1))

coords = np.block(coords)
ax.scatter(coords[0,:], coords[1,:], coords[2,:], marker=".")

#Labeling the coordinates
tri_coords = np.block([A, B, O])
ax.scatter(tri_coords[0,:], tri_coords[1,:], tri_coords[2,:])
vert_labels = ['A', 'B', 'O']
for i, txt in enumerate(vert_labels):
    # Annotate each point with its label and coordinates
    ax.text(tri_coords[0, i], tri_coords[1, i], tri_coords[2, i], f'{txt}\n({tri_coords[0, i]:.2f}, {tri_coords[1, i]:.2f}, {tri_coords[2, i]:.2f})',
             fontsize=12, ha='center', va='bottom')

dll.free_multi_memory(line_pts, n)
dll.free_multi_memory(pts, 3)

# use set_position
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
plt.grid() # minor
plt.axis('equal')

plt.savefig('../figs/graph.png')
plt.show()
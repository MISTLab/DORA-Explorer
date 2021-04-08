###
# Comparison between the radiation beacons positions and the data collected in
# the DBM
###

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import json

### Parameters
result_file = "../results/result.txt"
radiation_sources_file = "../data/radiation_sources.json"
###

# Initialize figure
fig = plt.figure()
ax = fig.gca(projection='3d')

# Read radiation results.
result_X = np.array([])
result_Y = np.array([])
result_Z = np.array([])
result_W = np.array([])
f = open(result_file, "r")
lines = f.readlines()
for line in lines:
    elems = line.split()
    result_X = np.append(result_X,int(elems[0]))
    result_Y = np.append(result_Y,int(elems[1]))
    result_Z = np.append(result_Z,float(elems[2]))
    result_W = np.append(result_W,float(elems[3]))

# Plot the results.
results_points = ax.scatter(result_X,result_Y,result_Z, color="blue")

# Read the radiation sources
radiation_X = np.array([])
radiation_Y = np.array([])
radiation_Z = np.array([])
with open(radiation_sources_file) as json_file:
    data = json.load(json_file)
    for r in data:
        radiation_X = np.append(radiation_X,float(r['x']))
        radiation_Y = np.append(radiation_Y,float(r['y']))
        radiation_Z = np.append(radiation_Z,float(r['intensity']))

# Plot the radiation sources
radiation_points = ax.scatter(radiation_X,radiation_Y,radiation_Z, color="red")

# Show plot
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Radiation level")
ax.set_zlim([0, 1])
plt.show()
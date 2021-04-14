###
# Comparison between the radiation beacons positions and the data collected in
# the DBM
###

import numpy as np
import json
import math

### Parameters
result_folder = "../results/"
radiation_sources_file = "../data/radiation_sources.json"
###

# Read radiation results.
result_X = np.array([])
result_Y = np.array([])
result_belief = np.array([])
result_W = np.array([])
result_total_data_transmitted = np.array([])
result_step = np.array([])
f = open(result_file, "r")
lines = f.readlines()
for line in lines:
    elems = line.split()
    result_X = np.append(result_X,int(elems[0]))
    result_Y = np.append(result_Y,int(elems[1]))
    result_belief = np.append(result_belief,float(elems[2]))
    result_W = np.append(result_W,float(elems[3]))
    result_step = np.append(result_step,float(elems[4]))

# Read the radiation sources
radiation_X = np.array([])
radiation_Y = np.array([])
radiation_intensity = np.array([])
with open(radiation_sources_file) as json_file:
    data = json.load(json_file)
    for r in data:
        radiation_X = np.append(radiation_X,float(r['x']))
        radiation_Y = np.append(radiation_Y,float(r['y']))
        radiation_intensity = np.append(radiation_intensity,float(r['intensity']))

### Compute metrics

# Number of steps
number_of_steps = int(result_step[0])
print("Number of steps = " + str(number_of_steps))
# Number of cases explored
number_of_cases_explored = len(lines)
print("Number of cases explored = " + str(number_of_cases_explored))

# Belief error and amount of radiation
belief_error = 0.0
amount_of_radiation = 0.0
for i in range(0, len(result_X)):
    # data
    x = result_X[i]
    y = result_Y[i]
    belief = result_belief[i]
    # gt belief
    total_radiation = 0.0
    for j in range(0, len(radiation_X)):
        r_x = radiation_X[j]
        r_y = radiation_Y[j]
        r_intensity = radiation_intensity[j]
        distance = math.sqrt((r_y-y)**2 + (r_x-x)**2)
        radiation = r_intensity / (1 + distance**2)
        if (radiation < 0.0):
            radiation = 0.0
        elif (radiation > 1.0):
            radiation = 1.0
        total_radiation = total_radiation + radiation
    error = abs(total_radiation - belief)
    belief_error = belief_error + error
    amount_of_radiation = amount_of_radiation + total_radiation
average_belief_error = belief_error / len(result_X)
print("Average error = " + str(average_belief_error))
print("Amount of radiation absorbed = " + str(amount_of_radiation))


## Amount transmitted
result_total_data_transmitted = np.array([])
result_step = np.array([])
f = open(data_transmitted_file, "r")
lines = f.readlines()
for line in lines:
    elems = line.split()
    result_total_data_transmitted = np.append(result_total_data_transmitted,float(elems[0]))
    result_step = np.append(result_step,float(elems[1]))

amount_transmitted = np.sum(result_total_data_transmitted)
print("Amount transmitted = " + str(amount_transmitted))

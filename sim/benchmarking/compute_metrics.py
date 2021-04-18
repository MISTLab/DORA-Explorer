###
# Comparison between the radiation beacons positions and the data collected in
# the DBM
###

import numpy as np
import json
import math
from os import listdir
from os.path import isfile, join
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

### Parameters
result_folder = "../results/"
radiation_sources_folder = "../data/"
result_random_final_folder = "../results/random-walk-final/"
figures_folder = "figures/"
number_of_steps_max = 100
folders = [result_random_final_folder, result_folder]
###

onlyfiles0 = [f for f in listdir(result_folder) if isfile(join(result_folder, f))]
onlyfiles1 = [f for f in listdir(result_folder) if isfile(join(result_folder, f))]
number_of_runs = min(len(onlyfiles0)/2, len(onlyfiles1)/2) 
number_of_folders = len(folders)

number_of_cases_explored = np.zeros((number_of_folders,number_of_runs, number_of_steps_max))
amount_of_radiation = np.zeros((number_of_folders,number_of_runs, number_of_steps_max))
average_belief_error = np.zeros((number_of_folders,number_of_runs, number_of_steps_max))
amount_transmitted = np.zeros((number_of_folders,number_of_runs, number_of_steps_max))

for folder in range(0, number_of_folders):
    print("---Processing folder " + folders[folder] + "---")
    for run in range(0, number_of_runs):
        # Set file names
        random_result_file = folders[folder] + "result" + str(run) + ".csv"
        random_data_transmitted_file = folders[folder] + "data_transmitted" + str(run) + ".csv"
        radiation_sources_file = radiation_sources_folder + "radiation_sources" + str(run) + ".json"
        print("------- RUN " + str(run) + " -------")

        # Read radiation results.
        result_X = np.array([])
        result_Y = np.array([])
        result_belief = np.array([])
        result_W = np.array([])
        result_total_data_transmitted = np.array([])
        result_step = np.array([])
        f = open(random_result_file, "r")
        lines = f.readlines()
        for line in lines:
            elems = line.split(',')
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

        # Number of cases explored
        for step in result_step:
            number_of_cases_explored[folder, run,int(step)] = number_of_cases_explored[folder, run,int(step)] + 1
        
        # Belief error and amount of radiation
        belief_error = np.zeros(number_of_steps_max)
        for i in range(0, len(result_X)):
            # data
            x = result_X[i]
            y = result_Y[i]
            belief = result_belief[i]
            step = int(result_step[i])
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
            belief_error[step] = belief_error[step] + error
            amount_of_radiation[folder, run, step] = amount_of_radiation[folder, run, step] + total_radiation
        
        for i in range(0,len(number_of_cases_explored[folder, run,:])):
            if (number_of_cases_explored[folder, run,i] != 0):
                average_belief_error[folder, run, i] = belief_error[i] / number_of_cases_explored[folder, run,i]

        ## Amount transmitted
        result_total_data_transmitted = np.array([])
        result_step = np.array([])
        f = open(random_data_transmitted_file, "r")
        lines = f.readlines()
        for line in lines:
            elems = line.split(',')
            result_total_data_transmitted = np.append(result_total_data_transmitted,float(elems[0]))
            result_step = np.append(result_step,float(elems[1]))

        total_transmission = 0.0
        for i in range(0,len(result_total_data_transmitted)):
            step = int(result_step[i])
            total_transmission = total_transmission + result_total_data_transmitted[i]
            amount_transmitted[folder, run, step] = total_transmission
    

x_axis = np.arange(number_of_steps_max)

fig = plt.figure()
ax = fig.gca()
for f in range(0,number_of_folders):
    ax.scatter(x_axis, number_of_cases_explored[f,:,:].mean(0))
ax.set_xlabel("Step")
ax.set_ylabel("Number of cells explored")
ax.legend(['Random Walk', 'Gradient'])
plt.savefig(figures_folder + "explored.png")

fig = plt.figure()
ax = fig.gca()
for f in range(0,number_of_folders):
    ax.scatter(x_axis, amount_of_radiation[f,:,:].mean(0))
ax.set_xlabel("Step")
ax.set_ylabel("Amount of radiation")
ax.legend(['Random Walk', 'Gradient'])
plt.savefig(figures_folder + "radiation.png")

fig = plt.figure()
ax = fig.gca()
for f in range(0,number_of_folders):
    ax.scatter(x_axis, average_belief_error[f,:,:].mean(0))
ax.set_xlabel("Step")
ax.set_ylabel("Averasge Belief Error")
ax.legend(['Random Walk', 'Gradient'])
plt.savefig(figures_folder + "error.png")

fig = plt.figure()
ax = fig.gca()
for f in range(0,number_of_folders):
    ax.scatter(x_axis, amount_transmitted[f,:,:].mean(0))
ax.set_xlabel("Step")
ax.set_ylabel("Total amount of data transmitted (B)")
ax.legend(['Random Walk', 'Gradient'])
plt.savefig(figures_folder + "transmitted.png")
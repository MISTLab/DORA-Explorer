import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


figures_folder = "figures/"
folders = ["../results/randomwalk/", "../results/frontier/", "../results/dora/"]
MAX_NB_STEPS = 200
NB_RUNS = 5


def parse_results() -> None:
    nb_explored_cells = np.zeros((len(folders), NB_RUNS, MAX_NB_STEPS))
    nb_active_robots = np.zeros((len(folders), NB_RUNS, MAX_NB_STEPS))

    for folder_id, folder_name in enumerate(folders):
        for run in range(NB_RUNS):
            print(f"---Processing {folder_name} run #{run}---")

            with open(f"{folder_name}result{run}.csv", "r") as res:
                explored_cells = set()
                step = 0
                for line in csv.reader(res):
                    step = int(line[4])
                    explored_cells.add(f"{line[0]}_{line[1]}")
                    nb_explored_cells[folder_id, run, step] = len(explored_cells)
                    nb_active_robots[folder_id, run, step] += 1

                nb_explored_cells[folder_id, run, step:MAX_NB_STEPS] = nb_explored_cells[folder_id, run, step]
                nb_active_robots[folder_id, run, step:MAX_NB_STEPS] = 0

    return nb_explored_cells, nb_active_robots

def plot_single_metric(metric_data: np.ndarray, dependant_variable: str, file_name: str) -> None:
    x_axis = np.arange(MAX_NB_STEPS)
    colors = ["lightcoral","orchid", "cornflowerblue"]

    fig = plt.figure()
    ax = fig.gca()

    for f in range(len(folders)):
        std = np.array([0.5 * np.nanstd(metric_data[f, :, i]) for i in range(MAX_NB_STEPS)])
        mean = metric_data[f, :, :].mean(0)
        ax.scatter(x_axis, mean, c=colors[f])
        ax.fill_between(x_axis, mean-std, mean+std, alpha=0.25, color=colors[f], label='_nolegend_')
    
    ax.set_xlabel("Step")
    ax.set_ylabel(dependant_variable)
    ax.legend(['Random Walk', 'Frontier', 'DORA'])
    plt.savefig(figures_folder + file_name)


def plot_metrics(nb_explored_cells: np.ndarray, nb_active_robots: np.ndarray) -> None:       
    plot_single_metric(nb_explored_cells, "Number of cells explored", "explored.png")
    plot_single_metric(nb_active_robots, "Number of active robots", "activerobots.png")


def main() -> None:
    plot_metrics(*parse_results())


if __name__ == "__main__":
    main()

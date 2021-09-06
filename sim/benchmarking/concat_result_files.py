import csv


FOLDER_RESULTS_DORA = "../results/dora"
FOLDER_RESULTS_FRONTIER = "../results/frontier"
FOLDER_RESULTS_RANDOM = "../results/randomwalk"
NB_RUNS = 5
ROBOT_IDS = [1, 7, 9]


def aggregate_results(folder, experiment) -> dict:
    stepwise_results = {}
    
    for robot_id in ROBOT_IDS:
        with open(f"{folder}/results_{experiment}_{robot_id}.csv", "r") as result_file:
            store_stepwise_results(csv.reader(result_file), stepwise_results)

    return stepwise_results


def store_stepwise_results(file_reader, stepwise_results: dict) -> None:
    next(file_reader)  # Skip header

    for line in file_reader:
        step = line[-2]
        
        if step in stepwise_results:
            stepwise_results[step].append(line)
        else:
            stepwise_results[step] = [line]


def main():
    for folder in [FOLDER_RESULTS_FRONTIER, FOLDER_RESULTS_RANDOM]:
        for experiment in range(NB_RUNS):
            stepwise_results = aggregate_results(folder, experiment)

            with open(f"{folder}/result{experiment}.csv", "w") as aggregated_file:
                writer = csv.writer(aggregated_file)
                for step in stepwise_results.values():
                    for result_line in step:
                        writer.writerow(result_line)
    
                    

if __name__ == "__main__":
    main()

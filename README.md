# DORA-Explorer

To run the experiment:
- Build a Docker image from docker/Dockerfile : `docker build IMAGE-NAME .`
- Create a docker container from the image while sharing your X11 server see [here](https://github.com/lajoiepy/argos3_docker_example/blob/master/README.md).
- Go into `/home/docker/DBM-SMS/sim/`
- Compile the Buzz scripts: `bzzc dbm-gradient.bzz` and `bzzc dbm-random-walk.bzz`.
- Launch `argos3 -c dbm-gradient.argos` for the DORA algorithm and `argos3 -c dbm-random-walk.argos` for the random walk algorithm.

To evaluate the results:
- Put the resulting `.csv` files generated in `/home/docker/DBM-SMS/sim/results` from the runs you want to evaluate into their respective subfolders.
- Go into `/home/docker/DBM-SMS/sim/benchmarking/` and run `python compute_metrics.py`
- The resulting figures will appear in `/home/docker/DBM-SMS/sim/benchmarking/figures`

If you already have argos3 and buzz installed on your computer you can simply clone the repository and build the C++ controller in `/home/docker/DBM-SMS/sim/controller/`.
If you want communication benchmarking you also need to install this buzz version: https://github.com/lajoiepy/Buzz.git on branch `bandwidth-log`

"""This program generates ground truth data for DBM-SMS.
The data is in JSON formats and represents radiation sources on a 2D grid.

The format is the following:
{"sources": [
    {"x": 0.5, "y": 2.1, "intensity": 0.75},
    {"x": 1.5, "y": 0.0, "intensity": 0.05}
]}
"""


import json
from random import uniform


NB_RADIATION_SOURCES = 2
MIN_MAP_X = -10
MAX_MAP_X = 10
MIN_MAP_Y = -10
MAX_MAP_Y = 10

def generate_source() -> dict:
    return {"x": uniform(MIN_MAP_X, MAX_MAP_X), "y": uniform(MIN_MAP_Y, MAX_MAP_Y), "intensity": uniform(0.0, 1.0)}


def main():
    with open("radiation_sources.json", "w") as f:
        json.dump([generate_source() for _ in range(NB_RADIATION_SOURCES)], f, indent=2)


if __name__ == "__main__":
    main()
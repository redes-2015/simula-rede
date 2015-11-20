#!/usr/bin/env python3

"""Main module. Checks command line arguments."""

import sys
from simulator import Simulator

# -------------------------------------------------------------

try:
    simulator = Simulator(sys.argv[1])
    simulator.start()
except IndexError:
    print("Simulation file not specified!")
except FileNotFoundError:
    print("Simulation file '%s' not found!" % sys.argv[1])
except KeyboardInterrupt:
    print("Simulation canceled!")

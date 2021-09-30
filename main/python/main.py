import sys

import logging
import logging_config
import dijkstra

logging_config.load_config()

# logging.basicConfig(filename=None, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s", level=logging.DEBUG)

LOGGER = logging.getLogger("main")

if __name__ == "__main__":
    matrix = sys.argv[1]
    start = sys.argv[2]
    destination = sys.argv[3]

    dijkstra.calculate(matrix, start, destination)

import sys

import logging
import logging_config
import dijkstra

logging_config.load_config()

# logging.basicConfig(filename=None, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s", level=logging.DEBUG)

LOGGER = logging.getLogger("main")

if __name__ == "__main__":
    # matrix = sys.argv[1]
    # start = sys.argv[2]
    # destination = sys.argv[3]
    from loader import read_csv_adjacent, read_json_eve
    from graph import Graph
    matrix = read_csv_adjacent("test/resources/test_matrix_1.csv")
    start = "A"
    destination = "H"
    graph = read_json_eve("test/resources/universe-pretty.json")
    start = "Tanoo"
    destination = "Zaid"

    dijkstra.calculate(graph, start, destination)

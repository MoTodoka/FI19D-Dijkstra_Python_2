import logging
import sys

from logging import config

import dijkstra

logging.config.fileConfig("log/log.conf")

LOGGER = logging.getLogger("main")

if __name__ == "__main__":
    graph = sys.argv[1]
    start = sys.argv[2]
    destination = sys.argv[3]

    dijkstra.print_path(graph, start, destination)

import logging
import argparse
import os
import typing
from enum import Enum, auto

from logging import config

import dijkstra
import loader

logging.config.fileConfig("log/log.conf")

LOGGER = logging.getLogger("main")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file")
    argparser.add_argument("start")
    argparser.add_argument("destination")
    argparser.add_argument("--type",
                           help="Determines the type of the file",
                           choices=["csv", "eve", "json", "fileaware"],
                           default="fileaware")
    node_table_group = argparser.add_mutually_exclusive_group()
    node_table_group.add_argument("-n", "--print-visited-nodes", action="store_true")
    node_table_group.add_argument("--print-nodes-with-parents", action="store_true")
    node_table_group.add_argument("-N", "--print-all-nodes", action="store_true")

    args = argparser.parse_args()

    if args.type == "fileaware":
        file_parts = os.path.splitext(args.file)
        if len(file_parts) == 2:
            if file_parts[1] == ".csv":
                selected_loader = loader.read_csv_adjacent
                known_type = True
            else:
                selected_loader = loader.read_json_node
                known_type = file_parts[1] == ".json"
        else:
            selected_loader = loader.read_json_node
            known_type = False

        if not known_type:
            LOGGER.warning("Unknown file type, defaulting to JSON")
    elif args.type == "csv":
        selected_loader = loader.read_csv_adjacent
    elif args.type == "eve":
        selected_loader = loader.read_json_eve
    elif args.type == "json":
        selected_loader = loader.read_json_node
    else:
        raise Exception("Unknown type")

    graph = selected_loader(args.file)
    start = args.start
    destination = args.destination

    show_visited: dijkstra.PrintNodesMode
    if args.print_visited_nodes:
        show_visited = dijkstra.PrintNodesMode.VISITED
    elif args.print_nodes_with_parents:
        show_visited = dijkstra.PrintNodesMode.HAS_PARENT
    elif args.print_all_nodes:
        show_visited = dijkstra.PrintNodesMode.ALL
    else:
        show_visited = dijkstra.PrintNodesMode.NONE

    dijkstra.print_path(graph, start, destination, show_visited)

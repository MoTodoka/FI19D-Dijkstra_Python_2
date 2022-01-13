from __future__ import annotations

import logging
import typing
from enum import auto, Enum

from MalformedGraphException import MalformedGraphException
from graph import Graph
from weighted_node import Node
from solver import Solver

LOGGER = logging.getLogger("dijkstra")


class PrintNodesMode(Enum):
    NONE = auto()
    VISITED = auto()
    HAS_PARENT = auto()
    ALL = auto()

    def check_node(self, node: Node) -> bool:
        if self == PrintNodesMode.VISITED:
            return node.visited
        elif self == PrintNodesMode.HAS_PARENT:
            return node.has_parent
        else:
            return self == PrintNodesMode.ALL


def get_path_string(path: [Node]) -> str:
    result: str = ""
    for step, node in enumerate(path):
        result += f"\n Step: {step} | Node: {node.graph_node.name}, weight: {node.weight}"
    return result


def get_path(graph: Graph, start: str, destination: str) -> [Node]:
    solver: Solver = Solver(graph, start, destination)
    solver.run()
    return solver.path


def print_path(graph: typing.Union[list[list[int]], Graph],
               start: str,
               destination: str,
               show_visited: PrintNodesMode = PrintNodesMode.NONE,
               astar_mode: bool = False):
    if not isinstance(graph, Graph):
        try:
            graph = Graph.from_adjacent_matrix(graph)
        except MalformedGraphException as e:
            LOGGER.error(str(e))
            return
    solver: Solver = Solver(graph, start, destination)
    solver.astar_mode = astar_mode
    solver.run()
    path_string: str = get_path_string(solver.path)
    print(path_string)

    if show_visited != PrintNodesMode.NONE:
        print()
        visited_nodes: int = 0
        nodes_with_parent: int = 0
        for node in solver.nodes:
            if node.visited:
                visited_nodes += 1
            if node.has_parent:
                nodes_with_parent += 1
        node_count = len(solver.nodes)
        summary: str = f"{node_count} Nodes"
        if node_count > 0:
            summary += f": {visited_nodes} visited ({visited_nodes/node_count:.1%}), {nodes_with_parent} have a parent ({nodes_with_parent/node_count:.1%})"
        print(summary)
        print()

        info = Node.print_nodes(node for node in solver.nodes if show_visited.check_node(node))
        print(info)

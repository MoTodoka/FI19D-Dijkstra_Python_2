from __future__ import annotations

import logging
import math
import typing
from dataclasses import dataclass
from typing import Optional

from MalformedGraphException import MalformedGraphException
from graph import GraphNode, Graph

LOGGER = logging.getLogger("root")


@dataclass
class Edge:
    node_start: Node
    node_target: Node
    weight: int

    def try_update_target(self) -> None:
        if not self.node_target.has_parent or self.node_start.weight + self.weight < self.node_target.weight:
            self.node_target._parent = self.node_start
            total_weight: int = self.weight
            if self.node_start != self.node_target:
                total_weight += self.node_start.weight
            self.node_target._weight = total_weight


class Node:
    _parent: Optional[Node] = None
    _weight: int = math.inf
    _visited: bool = False
    _graph_node: GraphNode

    def __init__(self, graph_node: GraphNode):
        self._graph_node = graph_node

    @property
    def index(self) -> int:
        return self._graph_node.index

    @property
    def label(self) -> str:
        return self._graph_node.label

    @property
    def parent(self) -> Optional[Node]:
        return self._parent

    @property
    def weight(self) -> int:
        return self._weight

    @property
    def visited(self) -> bool:
        return self._visited

    @property
    def has_parent(self) -> bool:
        return self._parent is not None

    @property
    def graph_node(self) -> GraphNode:
        return self._graph_node

    def set_as_visited(self) -> None:
        self._visited = True

    def __str__(self) -> str:
        return f"Node[{self.graph_node.name}, " \
               f"w={self.weight}, " \
               f"p={self.parent.index if self.has_parent else 'None'}]"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def get_index_from_label(label: chr):
        return ord(label) - ord('A')


class UnnamedNode(Node):
    pass


def get_next_node(nodes: list[Node]) -> Optional[Node]:
    filtered_node_generator = (node for node in nodes if node.has_parent and not node.visited)
    try:
        return min(filtered_node_generator, key=lambda n: n.weight)
    except ValueError:
        # Returned, when the generator is empty
        return None


def print_nodes(nodes: [Node], info: str = "") -> str:
    if info:
        info = f" ({info})"
    info = f"Current nodes{info}:"
    longest_line = len(info)
    for node in nodes:
        line = f"  {node.graph_node.name} -> " \
               f"w={node.weight!r} " \
               f"p={node.parent!r} " \
               f"hp={node.has_parent!r} " \
               f"iv={node.visited!r}"
        longest_line = max(len(line), longest_line)
        info += "\n" + line
    info += "\n" + "=" * longest_line
    return info


def get_path_string(path: [Node]) -> str:
    result: str = ""
    for step, node in enumerate(path):
        result += f"\n Step: {step} | Node: {node.graph_node.name}, weight: {node.weight}"
    return result


def path_iterator(node: Node) -> typing.Iterator[Node]:
    while node is not None:
        yield node
        if node == node.parent:
            break
        node = node.parent


def get_path(graph: Graph, start: str, destination: str) -> [Node]:
    # nodes array
    nodes: [Node] = [Node(graph_node) for graph_node in graph.nodes]
    node_map: {GraphNode, Node} = {node.graph_node: node for node in nodes}
    start_node: GraphNode = graph.node_from_label(start)
    destination_node: GraphNode = graph.node_from_label(destination)
    LOGGER.info(f"Try to find path from {start} ({start_node.index}) to {destination} ({destination_node.index})")

    start_node: Node = node_map[start_node]
    destination_node: Node = node_map[destination_node]
    Edge(start_node, start_node, 0).try_update_target()

    current_node: Node = start_node
    while current_node is not None:
        current_node.set_as_visited()
        if current_node == destination_node:
            break
        for graph_edge in graph.get_adjacent_edges(current_node.graph_node):
            node_start: Node = node_map[graph_edge.start_node]
            node_end: Node = node_map[graph_edge.end_node]
            Edge(node_start, node_end, graph_edge.weight).try_update_target()

        LOGGER.debug(print_nodes(nodes))

        # niedriges Gewicht, nicht besucht, hat Eltern
        current_node = get_next_node(nodes)

        LOGGER.info(f"next_node: {current_node}")

    path: [Node] = list(path_iterator(destination_node))
    path.reverse()

    return path


def print_path(graph: typing.Union[list[list[int]], Graph], start: str, destination: str):
    if not isinstance(graph, Graph):
        try:
            graph = Graph.from_adjacent_matrix(graph)
        except MalformedGraphException as e:
            LOGGER.error(str(e))
            return
    path: [Node] = get_path(graph, start, destination)
    path_string: str = get_path_string(path)
    print(path_string)

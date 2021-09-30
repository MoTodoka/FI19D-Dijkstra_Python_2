from __future__ import annotations

import typing
from typing import Optional
from dataclasses import dataclass
import math
import logging

from main.python.MalformedGraphException import MalformedGraphException

LOGGER = logging.getLogger("dijkstra")


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
    _index: int
    _parent: Optional[Node] = None
    _weight: int = math.inf
    _visited: bool = False

    def __init__(self, index):
        self._index = index

    @property
    def index(self) -> int:
        return self._index

    @property
    def label(self) -> str:
        return Node.get_label_from_index(self.index)

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

    def set_as_visited(self) -> None:
        self._visited = True

    def __str__(self) -> str:
        return f"Node[{self.index} ({self.label}), " \
               f"w={self.weight}, " \
               f"p={self.parent.index if self.has_parent else 'None'}]"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def get_label_from_index(index: int):
        return chr(index + ord('A'))

    @staticmethod
    def get_index_from_label(label: chr):
        return ord(label) - ord('A')


class UnnamedNode(Node):
    pass


def verify_matrix(matrix):
    node_count: int = len(matrix)
    if any(len(row) != node_count for row in matrix):
        raise MalformedGraphException("adjacent matrix is not a square")
    if any(matrix[i][i] for i in range(node_count)):
        raise MalformedGraphException("not all self referencing node are zero")


def get_next_node(nodes: list[Node]) -> Optional[Node]:
    filtered_node_generator = (node for node in nodes if node.has_parent and not node.visited)
    try:
        return min(filtered_node_generator, key=lambda n: n.weight)
    except ValueError:
        # Returned, when the generator is empty
        return None


def get_adjacent_edges(adjacency_matrix: [[int]], nodes: [Node], node: Node) -> list[Edge]:
    result: list[Edge] = list()
    for idx, edge_weight in enumerate(adjacency_matrix[node.index]):
        if edge_weight > 0:
            result.append(Edge(node, nodes[idx], edge_weight))
    return result


def print_nodes(nodes: list[Node], info: str = "") -> str:
    if info:
        info = f" ({info})"
    info = f"Current nodes{info}:"
    for node in nodes:
        info += f"\n  {node.index} ({node.label}) -> " \
                f"w={node.weight!r} " \
                f"p={node.parent!r} " \
                f"hp={node.has_parent!r} " \
                f"iv={node.visited!r}"
    info += "\n" + "=" * len(info)
    return info


def get_path_string(path: [Node]) -> str:
    result: str = ""
    for step, node in enumerate(path):
        result += f"\n Step: {step} | Node: #{node.index} ({node.label})"
    return result


def path_iterator(node: Node) -> typing.Iterator[Node]:
    while node is not None:
        yield node
        if node == node.parent:
            break
        node = node.parent


def get_path(matrix: [[int]], start: chr, destination: chr) -> [Node]:
    idx_start: int = Node.get_index_from_label(start)
    idx_end: int = Node.get_index_from_label(destination)
    LOGGER.info(f"Try to find path from {start} ({idx_start}) to {destination} ({idx_end})")

    node_count: int = len(matrix)

    # nodes array
    nodes: [Node] = [Node(i) for i in range(node_count)]
    # Node-list as a map for the index, so that sorting won't kill the relationship between index and Node
    # node_map: {int, Node} = {node.index: node for node in nodes}
    Edge(nodes[idx_start], nodes[idx_start], 0).try_update_target()

    current_node: Node = nodes[idx_start]
    while current_node is not None:
        current_node.set_as_visited()
        if current_node.index == idx_end:
            break
        for edge in get_adjacent_edges(matrix, nodes, current_node):
            edge.try_update_target()

        LOGGER.debug(print_nodes(nodes))

        # niedriges Gewicht, nicht besucht, hat Eltern
        current_node = get_next_node(nodes)

        LOGGER.info(f"next_node: {current_node}")

    # nur zum testen wie sich Edge verhält
    # GH: Müsste eine Edge nicht 2 Nodes enthalten? Start -> Ziel
    edge: Edge = Edge(nodes[idx_start], nodes[idx_start], 42)
    LOGGER.info(edge)

    path: [Node] = list(path_iterator(nodes[idx_end]))
    path.reverse()

    return path


def calculate(matrix: [[int]], start: chr, destination: chr):
    try:
        verify_matrix(matrix)
    except MalformedGraphException as e:
        print(str(e))
    else:
        path: [Node] = get_path(matrix, start, destination)
        path_string: str = get_path_string(path)
        print(path_string)

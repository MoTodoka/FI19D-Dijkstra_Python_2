from __future__ import annotations
from typing import Optional
from collections import namedtuple
from dataclasses import dataclass
import math

#            A, B, C, D, E, F, G, H, I
adjacent = ((0, 3, 0, 9, 2, 0, 0, 0, 0),  # A
            (3, 0, 2, 5, 6, 5, 0, 0, 0),  # B
            (0, 2, 0, 0, 3, 2, 0, 0, 0),  # C
            (9, 5, 0, 0, 8, 0, 1, 3, 0),  # D
            (2, 6, 3, 8, 0, 3, 7, 6, 2),  # E
            (0, 5, 2, 0, 3, 0, 0, 2, 3),  # F
            (0, 0, 0, 1, 7, 0, 0, 2, 0),  # G
            (0, 0, 0, 0, 6, 2, 4, 0, 6),  # H
            (0, 0, 0, 0, 2, 3, 0, 6, 0))  # I
start = "A"
ziel = "H"


class MalformedGraphException(Exception):
    pass


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
        return f"Node[{self.index} ({get_label_from_index(self.index)}), w={self.weight}, p={self.parent.index if self.has_parent else 'None'}]"

    def __repr__(self) -> str:
        return str(self)


def verify_matrix(matrix):
    node_count: int = len(adjacent)
    if any(len(row) != node_count for row in adjacent):
        raise MalformedGraphException("adjacent matrix is not a square")
    if any(adjacent[i][i] for i in range(node_count)):
        raise MalformedGraphException("not all self referencing node are zero")


def get_label_from_index(index: int):
    return chr(index + ord('A'))


def get_index_from_label(label: chr):
    return ord(label) - ord('A')


def get_next_node(nodes: list[Node]) -> Optional[None]:
    return None

    # du brauchst ein Node und ein Gewicht
    # deshalb habe ich das namedtuple Edge erstellt (siehe über Node)
    # also e = Edge(node, weight); e.weight/e.node :-)


def get_adjacent_edges(adjacency_matrix: [[int]], nodes: [Node], node: Node) -> list[Edge]:
    result: list[Edge] = list()
    for idx, edge_weight in enumerate(adjacency_matrix[node.index]):
        if edge_weight > 0:
            result.append(Edge(node, nodes[idx], edge_weight))
    return result


def print_nodes(nodes: list[Node], info: str = "") -> None:
    if info:
        info = f" ({info})"
    info = f"Current nodes{info}:"
    print(info)
    for idx, node in enumerate(nodes):
        print(
            f"  {idx} ({get_label_from_index(idx)}) -> w={node.weight!r} p={node.parent!r} hp={node.has_parent!r} iv={node.visited!r}")
    print("=" * len(info))


def print_path(end_node: Node) -> None:
    n: Node = end_node
    step: int = 0
    print(f"Path to #{end_node.index}")
    while n is not None:
        print(f"\t{step}: #{n.index}")
        n = n.parent
        step += 1
        if n is not None and n == n.parent:
            break
    print()


def get_path(matrix: [[int]], start: str, ziel: str):
    idx_start: int = get_index_from_label(start)
    idx_end: int = get_index_from_label(ziel)
    print(f"Try to find path from {start} ({idx_start}) to {ziel} ({idx_end})")

    verify_matrix(matrix)
    # if not verify_matrix(matrix):
    #    raise Exception("")

    node_count: int = len(matrix)

    # nodes array
    nodes: [Node] = [Node(i) for i in range(node_count)]
    # Node-list as a map for the index, so that sorting won't kill the relationship between index and Node
    # node_map: {int, Node} = {node.index: node for node in nodes}
    Edge(nodes[idx_start], nodes[idx_start], 0).try_update_target()

    current_node: Node = nodes[idx_start]
    for edge in get_adjacent_edges(matrix, nodes, current_node):
        edge.try_update_target()
    current_node.set_as_visited()

    # niedriges Gewicht, nicht besucht, hat eltern

    print_nodes(nodes)

    node = min((node for node in nodes if node.has_parent and not node.visited), key=lambda n: n.weight)

    print(f"Min: {node}")

    # nur zum testen wie sich Edge verhält
    # GH: Müsste eine Edge nicht 2 Nodes enthalten? Start -> Ziel
    e: Edge = Edge(nodes[idx_start], nodes[idx_start], 42)
    print(e)

    print_path(nodes[idx_start])
    print_path(nodes[idx_end])

    return True


if __name__ == "__main__":
    print(get_path(adjacent, start, ziel))

    print('here ya go')

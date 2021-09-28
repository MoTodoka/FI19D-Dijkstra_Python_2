from __future__ import annotations
from typing import Optional

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


class Node:
    _index: int
    _parent: Optional[Node] = None
    _weight: int = 0
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
    def has_path(self) -> bool:
        return self._parent is not None

    def try_update_parent(self, new_parent: Node, edge_weight: int) -> None:
        if not self.has_path or new_parent.weight + edge_weight < self.weight:
            self._parent = new_parent
            self._weight = new_parent.weight + edge_weight

    def __str__(self) -> str:
        return f"Node[{self.index}, w={self.weight if self.has_path else 'inf'}, p={self.parent.index if self.has_path else 'None'}]"

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
    
def get_adjacent_nodes(adjacency_matrix: [[int]], node: Node):
    nodes: list[Node] = list()
    node_idx = Node.index
    #for idx in range 
    

def get_path(matrix: [[int]], start: str, ziel: str):
    idx_start: int = get_index_from_label(start)
    idx_end: int = get_index_from_label(ziel)
    print(f"Try to find path from {start} ({idx_start}) to {ziel} ({idx_end})")

    verify_matrix(matrix)
    #if not verify_matrix(matrix):
    #    raise Exception("")

    node_count: int = len(matrix)

    # nodes array
    # "parent", "weight", "visited"
    nodes = [Node(i) for i in range(node_count)]
    nodes[idx_start].try_update_parent(nodes[idx_start], 0)

    for idx, node in enumerate(nodes):
        print(f"{idx} -> {node.weight!r} {node.parent!r} {node.has_path!r} {node.visited!r}")

    nodes.sort(key=lambda x: x.weight, reverse=False)

    return True

if __name__ == "__main__":
    print(get_path(adjacent, start, ziel))
    
    print("here ya' go")
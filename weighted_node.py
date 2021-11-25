from __future__ import annotations

import math
from typing import Optional

from graph import GraphNode


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

    def try_update_target(self, node_start: Node, weight: int) -> None:
        if not self.has_parent or node_start.weight + weight < self.weight:
            self._parent = node_start
            total_weight: int = weight
            if node_start != self:
                total_weight += node_start.weight
            self._weight = total_weight

    @staticmethod
    def get_index_from_label(label: chr):
        return ord(label) - ord('A')

    @staticmethod
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


class UnnamedNode(Node):
    pass

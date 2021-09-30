from __future__ import annotations
from dataclasses import dataclass, field


class Graph:
    _nodes: [GraphNode]
    _edges: [GraphEdge]

    def __init__(self, nodes: [GraphNode], edges: [GraphEdge]):
        self._nodes = nodes
        self._edges = edges

    @property
    def node_count(self):
        return len(self._nodes)

    def __len__(self):
        return self.node_count

    def get_adjacent_edges(self, node: GraphNode) -> [GraphEdge]:
        return (edge for edge in self._edges if edge.node_start == node)


@dataclass
class GraphNode:
    label: str
    index: int


@dataclass
class GraphEdge:
    start: GraphNode
    end: GraphNode
    weight: int = field(default=0)

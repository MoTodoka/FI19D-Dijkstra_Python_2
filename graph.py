from __future__ import annotations
from dataclasses import dataclass, field


class Graph:
    _nodes: tuple[GraphNode]
    _edges: tuple[GraphEdge]

    def __init__(self, nodes: [GraphNode], edges: [GraphEdge]):
        self._nodes = tuple(nodes)
        self._edges = tuple(edges)

    @staticmethod
    def from_adjacent_matrix(adjacent_matrix: [[int]]) -> Graph:
        nodes: tuple[GraphNode] = tuple(GraphNode.create(idx) for idx in range(len(adjacent_matrix)))
        edges: [GraphEdge] = []
        for start_idx, edges_row in enumerate(adjacent_matrix):
            start_node: GraphNode = nodes[start_idx]
            for end_idx, weight in enumerate(edges_row):
                if weight != 0 and start_idx != end_idx:
                    end_node: GraphNode = nodes[end_idx]
                    edges.append(GraphEdge(start_node, end_node, weight))
        return Graph(nodes, edges)

    def node_from_label(self, label: str) -> GraphNode:
        for node in self._nodes:
            if node.label == label:
                return node
        raise KeyError()

    @property
    def nodes(self) -> tuple[GraphNode]:
        return self._nodes

    @property
    def node_count(self):
        return len(self._nodes)

    def __len__(self):
        return self.node_count

    def get_adjacent_edges(self, node: GraphNode) -> [GraphEdge]:
        return (edge for edge in self._edges if edge.start_node == node)


@dataclass(frozen=True)
class GraphNode:
    index: int
    label: str

    @staticmethod
    def create(index: int) -> GraphNode:
        return GraphNode(index, GraphNode.get_label_from_index(index))

    @staticmethod
    def get_label_from_index(index: int):
        return chr(index + ord('A'))

    @property
    def name(self) -> str:
        return f"{self.label} ({self.index})"


@dataclass(frozen=True)
class GraphEdge:
    start_node: GraphNode
    end_node: GraphNode
    weight: int = field(default=0)

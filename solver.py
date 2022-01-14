import logging
from typing import Optional, Union, Callable

from weighted_node import Node
from graph import Graph, GraphNode


LOGGER = logging.getLogger("solver")


class Solver:

    _graph: Graph
    _nodes: Optional[tuple[Node]]
    _start_graph_node: GraphNode
    _destination_graph_node: GraphNode
    _astar_mode: bool = False

    def __init__(self, graph: Graph, start: str, destination: str):
        self._graph = graph
        self._nodes = None
        self._start_graph_node = graph.node_from_label(start)
        self._destination_graph_node = graph.node_from_label(destination)

    @property
    def astar_mode(self) -> bool:
        return self._astar_mode

    @astar_mode.setter
    def astar_mode(self, value: bool) -> None:
        self._astar_mode = value

    def run(self) -> bool:
        if self._nodes is not None:
            return self._destination_node.has_parent
        self._nodes = tuple(Node(graph_node, self._destination_graph_node) for graph_node in self._graph.nodes)
        node_map: {GraphNode, Node} = {node.graph_node: node for node in self._nodes}
        LOGGER.info(f"Try to find path from {self._start_graph_node.name} to {self._destination_graph_node.name}")

        start_node: Node = node_map[self._start_graph_node]
        destination_node: Node = node_map[self._destination_graph_node]
        start_node.try_update_target(start_node, 0)

        current_node: Node = start_node
        while current_node is not None:
            current_node.set_as_visited()
            if current_node == destination_node:
                break
            for graph_edge in self._graph.get_adjacent_edges(current_node.graph_node):
                node_start: Node = node_map[graph_edge.start_node]
                node_end: Node = node_map[graph_edge.end_node]
                node_end.try_update_target(node_start, graph_edge.weight)

            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug(Node.print_nodes(self._nodes))

            # niedriges Gewicht, nicht besucht, hat Eltern
            current_node = self._get_next_node()

            LOGGER.info(f"next_node: {current_node}")

        return destination_node.has_parent

    @property
    def nodes(self) -> [Node]:
        return self._nodes

    @property
    def path(self) -> list[Node]:
        return self.sub_path(self._destination_node)

    def sub_path(self, destination_node: Union[Node, GraphNode, str]) -> list[Node]:
        if isinstance(destination_node, GraphNode):
            destination_node = self._get_node(lambda node: node.graph_node == destination_node)
        elif isinstance(destination_node, str):
            destination_node = self._get_node(lambda node: node.label == destination_node)
        nodes: list[Node] = [self._destination_node]
        while nodes[0].has_parent:
            if nodes[0].parent == nodes[0]:
                break
            nodes.insert(0, nodes[0].parent)
        return nodes

    @property
    def _destination_node(self) -> Optional[Node]:
        return self._get_node(lambda node: node.graph_node == self._destination_graph_node)

    def _get_node(self, test: Callable[[Node], bool]) -> Optional[Node]:
        if self._nodes is None:
            return None
        for node in self._nodes:
            if test(node):
                return node
        return None

    @staticmethod
    def _astar_weight(node: Node) -> float:
        return node.weight + node.distance

    @staticmethod
    def _dijkstra_weight(node: Node) -> float:
        return node.weight

    def _get_next_node(self) -> Optional[Node]:
        filtered_node_generator = (node for node in self._nodes if node.has_parent and not node.visited)
        try:
            return min(filtered_node_generator, key=Solver._astar_weight if self.astar_mode else Solver._dijkstra_weight)
        except ValueError:
            # Returned, when the generator is empty
            return None

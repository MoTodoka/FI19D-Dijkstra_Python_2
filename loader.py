import json
import graph
from MalformedGraphException import MalformedGraphException


def read_json_node(filename: str) -> [[int]]:
    with open(filename, "r") as f:
        mapping = json.load(f)

    node_count = len(mapping)
    matrix: [[int]] = []
    for maps in mapping:
        edges_from_node: [int] = [0] * node_count
        for edge_node, edge_weight in maps:
            if edges_from_node[edge_node] != 0:
                raise MalformedGraphException(f"multiple edges from node ({len(matrix)}) to node ({edge_node}) defined")
            edges_from_node[edge_node] = edge_weight
        matrix.append(edges_from_node)

    return matrix


def read_json_eve(filename: str, euclidean_distance: bool) -> graph.Graph:
    with open(filename, "r") as f:
        node_vertices = json.load(f)

    nodes = [graph.GraphNode(node["id"], node["name"], (node["x"], node["y"], node["z"]))
             for node in node_vertices["solarSystems"]]
    node_map = {node.index: node for node in nodes}
    edges: [graph.GraphEdge] = []
    for jump in node_vertices["jumps"]:
        start_node: graph.GraphNode = node_map[jump["from"]]
        end_node: graph.GraphNode = node_map[jump["to"]]
        distance: float = start_node.distance(end_node) if euclidean_distance else 1
        edges.append(graph.GraphEdge(start_node, end_node, distance))

    return graph.Graph(nodes, edges)


def read_csv_adjacent(filename: str) -> [[int]]:
    matrix: [[int]] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            matrix.append([int(entry.strip()) for entry in line.split(",")])
    return matrix

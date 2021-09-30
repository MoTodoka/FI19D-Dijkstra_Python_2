import json
from collections import defaultdict

from main.python.MalformedGraphException import MalformedGraphException


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


def read_json_eve(filename: str) -> [[int]]:
    with open(filename, "r") as f:
        node_vertices = json.load(f)

    node_count = len(node_vertices["solarSystems"])
    matrix: [[int]] = []
    node_ids = [node["id"] for node in node_vertices["solarSystems"]]
    node_id_map = {node_id: idx for idx, node_id in enumerate(node_ids)}
    edges = defaultdict(list)
    for jump in node_vertices["jumps"]:
        edges[jump["from"]].append(jump["to"])


def read_csv_adjacent(filename: str) -> [[int]]:
    matrix: [[int]] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            matrix.append([int(entry.strip()) for entry in line.split(",")])
    return matrix

import unittest

import loader


class MyTestCase(unittest.TestCase):
    resources_path = "../resources/"

    def test_parse_json(self):
        # given
        file_name: str = "test_matrix_2.json"
        expected_matrix: [[int]] = [[0, 3, 3], [1, 0, 0], [2, 0, 0]]

        # when
        actual_matrix = loader.read_json_node(self.resources_path + file_name)

        # then
        self.assertEqual(expected_matrix, actual_matrix, "JSON lesen")

    def test_parse_json_eve(self):
        # given
        file_name: str = "universe-pretty.json"
        expected_matrix: [[int]] = [[]]

        # when
        graph = loader.read_json_eve(self.resources_path + file_name)

        self.assertEqual(graph.node_count, 5431, "Eve-JSON node_count")
        self.assertEqual(graph.nodes[0].label, "Tanoo", "Eve-JSON node_count")
        self.assertEqual(graph.nodes[141].label, "Jita", "Eve-JSON node_count")

    def test_parse_csv(self):
        # given
        file_name: str = "test_matrix_1.csv"
        expected_matrix: [[int]] = [[0, 3, 0, 9, 2, 0, 0, 0, 0],
                                    [3, 0, 2, 5, 6, 5, 0, 0, 0],
                                    [0, 2, 0, 0, 3, 2, 0, 0, 0],
                                    [9, 5, 0, 0, 8, 0, 1, 3, 0],
                                    [2, 6, 3, 8, 0, 3, 7, 6, 2],
                                    [0, 5, 2, 0, 3, 0, 0, 2, 3],
                                    [0, 0, 0, 1, 7, 0, 0, 2, 0],
                                    [0, 0, 0, 0, 6, 2, 4, 0, 6],
                                    [0, 0, 0, 0, 2, 3, 0, 6, 0]]

        # when
        actual_matrix = loader.read_csv_adjacent(self.resources_path + file_name)

        self.assertEqual(expected_matrix, actual_matrix, "CSV lesen")


if __name__ == '__main__':
    unittest.main()

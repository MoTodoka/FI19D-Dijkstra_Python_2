import unittest

from main.python import dijkstra, logging_config


class MyTestCase(unittest.TestCase):
    def test_process_matrix(self):
        logging_config.load_config()
        # given
        # A, B, C, D, E, F, G, H, I
        matrix: [[int]] = ((0, 3, 0, 9, 2, 0, 0, 0, 0),  # A
                           (3, 0, 2, 5, 6, 5, 0, 0, 0),  # B
                           (0, 2, 0, 0, 3, 2, 0, 0, 0),  # C
                           (9, 5, 0, 0, 8, 0, 1, 3, 0),  # D
                           (2, 6, 3, 8, 0, 3, 7, 6, 2),  # E
                           (0, 5, 2, 0, 3, 0, 0, 2, 3),  # F
                           (0, 0, 0, 1, 7, 0, 0, 2, 0),  # G
                           (0, 0, 0, 0, 6, 2, 4, 0, 6),  # H
                           (0, 0, 0, 0, 2, 3, 0, 6, 0))  # I
        start: chr = "A"
        destination: chr = "H"

        expected_path: [chr] = ['A', 'E', 'F', 'H']

        # when
        node_path: [dijkstra.Node] = dijkstra.get_path(matrix, start, destination)

        actual_path: [chr] = [node.label for node in node_path]

        # then
        self.assertEqual(actual_path, expected_path, "Process Adjacent-Matrix")


if __name__ == '__main__':
    unittest.main()

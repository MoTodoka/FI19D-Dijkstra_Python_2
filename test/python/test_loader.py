import unittest

from main.python import loader


class MyTestCase(unittest.TestCase):
    def test_parse_json(self):
        # given
        file_path: str = "../resources/test_matrix_2.json"
        expected_matrix: [[int]] = [[0, 3, 3], [1, 0, 0], [2, 0, 0]]

        # when
        actual_matrix = loader.read_json_node(file_path)

        # then
        self.assertEqual(expected_matrix, actual_matrix, "JSON lesen")


if __name__ == '__main__':
    unittest.main()

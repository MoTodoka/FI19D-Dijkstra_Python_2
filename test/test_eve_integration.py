import unittest

import dijkstra
import loader


class MyTestCase(unittest.TestCase):
    resources_path = "../resources/"

    # given
    file_name: str = "universe-pretty.json"
    start: str = "Jita"
    destination: str = "Amarr"
    expected_path: [str] = ['Jita',
                            'Perimeter',
                            'Urlen',
                            'Sirppala',
                            'Inaro',
                            'Kaaputenen',
                            'Niarja',
                            'Madirmilire',
                            'Ashab',
                            'Amarr']

    def test_route_jita_amarr(self):

        # when
        graph = loader.read_json_eve(self.resources_path + self.file_name, False)
        node_path = dijkstra.get_path(graph, self.start, self.destination)

        actual_path: [str] = [node.label for node in node_path]

        self.assertEqual(self.expected_path, actual_path, "Route: Jita -> Amarr")

    def test_route_jita_amarr_euclidean(self):

        # when
        graph = loader.read_json_eve(self.resources_path + self.file_name, True)
        node_path = dijkstra.get_path(graph, self.start, self.destination)

        actual_path: [str] = [node.label for node in node_path]

        self.assertEqual(self.expected_path, actual_path, "Route: Jita -> Amarr")


if __name__ == '__main__':
    unittest.main()

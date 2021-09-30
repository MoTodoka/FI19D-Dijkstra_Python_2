import unittest

import dijkstra
import loader


class MyTestCase(unittest.TestCase):
    resources_path = "../resources/"

    def test_route_jita_amarr(self):
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

        # when
        graph = loader.read_json_eve(self.resources_path + file_name)
        node_path = dijkstra.get_path(graph, start, destination)

        actual_path: [str] = [node.label for node in node_path]

        self.assertEqual(expected_path, actual_path, "Route: Jita -> Amarr")


if __name__ == '__main__':
    unittest.main()

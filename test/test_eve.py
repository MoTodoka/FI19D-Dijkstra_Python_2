import time
import unittest
from typing import Union

import dijkstra
import loader


def compare_dijkstra_astar_time(start, destination) -> {}:
    # given
    graph = loader.read_json_eve("../resources/universe-pretty.json", True)
    show_visited = dijkstra.PrintNodesMode.SUM

    # when
    print(f"Starting Dijkstra - {start} to {destination}")
    pre_dijkstra = time.process_time()
    dijkstra.print_path(graph, start, destination, show_visited, astar_mode=False)
    post_dijkstra = time.process_time()
    duration_dijkstra = post_dijkstra - pre_dijkstra
    print(f"dijkstra: start={pre_dijkstra}s end={post_dijkstra}s duration={duration_dijkstra}s\n---")

    print(f"Starting A*       - {start} to {destination}")
    pre_astar = time.process_time()
    dijkstra.print_path(graph, start, destination, show_visited, astar_mode=True)
    post_astar = time.process_time()
    duration_astar = post_astar - pre_astar
    print(f"astar   : start={pre_astar}s end={post_astar}s duration={duration_astar}s\n---")

    difference_seconds = duration_dijkstra - duration_astar
    difference_percent = abs(difference_seconds) / duration_dijkstra
    print(f"A* was {abs(difference_seconds)}s ({difference_percent:.1%}) "
          f"{'faster' if difference_seconds > 0 else 'slower'} than Dijkstra\n---")

    # then
    return {"duration_dijkstra": duration_dijkstra, "duration_astar": duration_astar}


class MyTestCase(unittest.TestCase):

    def test_generator(self):
        testcases: list[dict[str, str]] = [
            {"start": "Jita", "destination": "Amarr"},
            {"start": "Saminer", "destination": "F7-ICZ"}
        ]
        result_set: list[dict[str, Union[str, float]]] = []
        for testcase in testcases:
            result: dict[str, Union[str, float]] = testcase
            result.update(compare_dijkstra_astar_time(testcase['start'], testcase['destination']))
            result_set.append(result)

        for result in result_set:
            self.assertGreater(result['duration_dijkstra'],
                               result['duration_astar'],
                               f"Dijkstra was quicker than A* from {result['start']} to {result['destination']}")

    if __name__ == '__main__':
        unittest.main()

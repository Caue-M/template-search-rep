import unittest

from algorithms.a_star import AStar
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from puzzle.result import SearchResult
from puzzle.state import GOAL_STATE, State


def zero_heuristic(state):
    return 0


class TestState(unittest.TestCase):
    def test_neighbors_respect_board_boundaries(self):
        expected_counts = [2, 3, 2, 3, 4, 3, 2, 3, 2]

        for blank in range(9):
            tiles = list(GOAL_STATE)
            tiles[8] = tiles[blank]
            tiles[blank] = 0
            initial = State(tuple(tiles), cost=5)
            children = initial.neighbors()
            boards = set()

            self.assertEqual(len(children), expected_counts[blank])

            for child in children:
                new_blank = child.blank_index
                distance = abs(blank // 3 - new_blank // 3)
                distance += abs(blank % 3 - new_blank % 3)
                self.assertEqual(distance, 1)
                self.assertEqual(set(child.tiles), set(range(9)))
                self.assertEqual(child.tiles[blank], initial.tiles[new_blank])
                self.assertEqual(child.cost, 6)
                self.assertIs(child.parent, initial)
                boards.add(child.tiles)

            self.assertEqual(len(boards), len(children))
            self.assertEqual(initial.tiles, tuple(tiles))

    def test_path_and_actions(self):
        initial = State((1, 2, 3, 4, 0, 6, 7, 5, 8))
        middle = State((1, 2, 3, 4, 5, 6, 7, 0, 8), initial, "DOWN", 1)
        goal = State(GOAL_STATE, middle, "RIGHT", 2)

        self.assertEqual(goal.path(), [initial, middle, goal])
        self.assertEqual(goal.actions(), ["DOWN", "RIGHT"])
        self.assertEqual(initial.path(), [initial])
        self.assertEqual(initial.actions(), [])

    def test_path_handles_long_chains(self):
        current = State(GOAL_STATE)

        for cost in range(1, 1501):
            current = State(GOAL_STATE, current, "UP", cost)

        self.assertEqual(len(current.path()), 1501)
        self.assertEqual(len(current.actions()), 1500)


class TestSearch(unittest.TestCase):
    def check_solution(self, initial, result):
        self.assertIsInstance(result, SearchResult)
        self.assertTrue(result.found)
        self.assertTrue(result.solution.is_goal)
        path = result.solution.path()
        self.assertIs(path[0], initial)
        self.assertEqual(len(path) - 1, result.depth)
        self.assertEqual(len(result.actions), result.depth)
        self.assertEqual(result.path_cost, initial.cost + result.depth)
        self.assertGreaterEqual(result.nodes_generated, len(path))
        self.assertGreaterEqual(result.max_frontier_size, 1)
        moves = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

        for index in range(1, len(path)):
            previous = path[index - 1]
            current = path[index]
            row_change, column_change = moves[current.action]
            blank = previous.blank_index
            new_blank = current.blank_index
            self.assertEqual(new_blank // 3, blank // 3 + row_change)
            self.assertEqual(new_blank % 3, blank % 3 + column_change)
            expected = list(previous.tiles)
            expected[blank] = expected[new_blank]
            expected[new_blank] = 0
            self.assertEqual(current.tiles, tuple(expected))
            self.assertIs(current.parent, previous)
            self.assertEqual(current.cost, previous.cost + 1)

    def test_already_solved(self):
        for algorithm in [BFS(), DFS(), AStar()]:
            with self.subTest(algorithm=type(algorithm).__name__):
                initial = State(GOAL_STATE)
                result = algorithm.search(initial)
                self.check_solution(initial, result)
                self.assertEqual(result.depth, 0)
                self.assertEqual(result.nodes_expanded, 0)
                self.assertEqual(result.nodes_generated, 1)
                self.assertEqual(result.max_frontier_size, 1)

    def test_bfs_and_astar_find_shortest_paths(self):
        cases = [
            ((1, 2, 3, 4, 5, 6, 7, 0, 8), 1),
            ((1, 2, 3, 4, 0, 6, 7, 5, 8), 2),
            ((1, 2, 3, 5, 0, 6, 4, 7, 8), 4),
            ((1, 3, 6, 5, 0, 2, 4, 7, 8), 8),
            ((7, 2, 4, 5, 0, 6, 8, 3, 1), 20),
        ]

        for algorithm in [BFS(), AStar()]:
            for tiles, depth in cases:
                with self.subTest(algorithm=type(algorithm).__name__, tiles=tiles):
                    initial = State(tiles)
                    result = algorithm.search(initial)
                    self.check_solution(initial, result)
                    self.assertEqual(result.depth, depth)

    def test_astar_solves_a_31_move_board(self):
        initial = State((8, 6, 7, 2, 5, 4, 3, 0, 1))
        result = AStar().search(initial)
        self.check_solution(initial, result)
        self.assertEqual(result.depth, 31)

    def test_dfs_respects_depth_limit(self):
        initial = State((1, 3, 6, 5, 0, 2, 4, 7, 8))
        self.assertFalse(DFS(7).search(initial).found)
        result = DFS(8).search(initial)
        self.check_solution(initial, result)
        self.assertEqual(result.depth, 8)

    def test_dfs_revisits_states_reached_at_a_smaller_depth(self):
        initial = State((2, 4, 3, 0, 1, 5, 7, 8, 6))
        result = DFS(7).search(initial)
        self.check_solution(initial, result)
        self.assertEqual(result.depth, 7)

    def test_dfs_with_zero_depth_limit(self):
        result = DFS(0).search(State((1, 2, 3, 4, 5, 6, 7, 0, 8)))
        self.assertFalse(result.found)
        self.assertEqual(result.nodes_expanded, 0)
        self.assertEqual(result.nodes_generated, 1)
        self.assertEqual(result.max_frontier_size, 1)
        self.assertTrue(DFS(0).search(State(GOAL_STATE)).found)

    def test_dfs_default_limit(self):
        initial = State((1, 2, 3, 5, 0, 6, 4, 7, 8))
        result = DFS().search(initial)
        self.check_solution(initial, result)
        self.assertLessEqual(result.depth, 50)

    def test_unsolvable_board(self):
        for algorithm in [BFS(), DFS(), AStar()]:
            with self.subTest(algorithm=type(algorithm).__name__):
                result = algorithm.search(State((1, 2, 3, 4, 5, 6, 8, 7, 0)))
                self.assertFalse(result.found)
                self.assertEqual(result.actions, [])
                self.assertEqual(result.path_cost, -1)
                self.assertEqual(result.depth, 0)

    def test_initial_cost_is_preserved(self):
        for algorithm in [BFS(), DFS(1), AStar()]:
            with self.subTest(algorithm=type(algorithm).__name__):
                initial = State((1, 2, 3, 4, 5, 6, 7, 0, 8), cost=10)
                result = algorithm.search(initial)
                self.check_solution(initial, result)
                self.assertEqual(result.depth, 1)
                self.assertEqual(result.path_cost, 11)

    def test_search_object_can_be_reused(self):
        for algorithm in [BFS(), DFS(2), AStar()]:
            algorithm.search(State(GOAL_STATE))
            initial = State((1, 2, 3, 4, 5, 6, 7, 0, 8))
            result = algorithm.search(initial)
            self.check_solution(initial, result)
            self.assertEqual(result.depth, 1)

    def test_astar_accepts_a_custom_heuristic(self):
        initial = State((1, 3, 6, 5, 0, 2, 4, 7, 8))
        result = AStar(zero_heuristic).search(initial)
        self.check_solution(initial, result)
        self.assertEqual(result.depth, 8)

    def test_astar_metrics_on_a_one_move_board(self):
        result = AStar().search(State((1, 2, 3, 4, 5, 6, 7, 0, 8)))
        self.assertEqual(result.nodes_expanded, 1)
        self.assertEqual(result.nodes_generated, 4)
        self.assertEqual(result.max_frontier_size, 3)


class TestHeuristic(unittest.TestCase):
    def test_manhattan_distance(self):
        algorithm = AStar()
        self.assertEqual(algorithm.heuristic(State(GOAL_STATE)), 0)
        self.assertEqual(algorithm.heuristic(State((1, 2, 3, 4, 5, 6, 7, 0, 8))), 1)
        self.assertEqual(algorithm.heuristic(State((1, 2, 3, 5, 0, 6, 4, 7, 8))), 4)

    def test_heuristic_is_admissible_and_consistent(self):
        algorithm = AStar()
        queue = [State(GOAL_STATE)]
        visited = {GOAL_STATE}
        index = 0

        while index < len(queue):
            current = queue[index]
            index += 1
            estimate = algorithm.heuristic(current)
            self.assertLessEqual(estimate, current.cost)

            if current.cost < 8:
                for neighbor in current.neighbors():
                    self.assertLessEqual(estimate, 1 + algorithm.heuristic(neighbor))

                    if neighbor.tiles not in visited:
                        visited.add(neighbor.tiles)
                        queue.append(neighbor)


if __name__ == "__main__":
    unittest.main()

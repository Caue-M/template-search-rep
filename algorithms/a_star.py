import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def __init__(self, heuristic=None):
        self.heuristic_function = heuristic

    def heuristic(self, state: State) -> int:
        distance = 0

        for index in range(9):
            tile = state.tiles[index]

            if tile != 0:
                row = index // 3
                column = index % 3
                goal_row = (tile - 1) // 3
                goal_column = (tile - 1) % 3
                distance += abs(row - goal_row) + abs(column - goal_column)

        return distance

    def search(self, initial: State) -> SearchResult:
        heuristic = self.heuristic

        if self.heuristic_function is not None:
            heuristic = self.heuristic_function

        priority = initial.cost + heuristic(initial)
        frontier = [(priority, initial)]
        costs = {initial.tiles: initial.cost}
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            priority, current = heapq.heappop(frontier)

            if current.cost > costs[current.tiles]:
                continue

            if current.is_goal:
                result.solution = current
                result.depth = current.cost - initial.cost
                return result

            result.nodes_expanded += 1

            for neighbor in current.neighbors():
                result.nodes_generated += 1

                if neighbor.tiles not in costs or neighbor.cost < costs[neighbor.tiles]:
                    costs[neighbor.tiles] = neighbor.cost
                    priority = neighbor.cost + heuristic(neighbor)
                    heapq.heappush(frontier, (priority, neighbor))

            if len(frontier) > result.max_frontier_size:
                result.max_frontier_size = len(frontier)

        return result

from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        frontier = deque([initial])
        visited = {initial.tiles}
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            current = frontier.popleft()

            if current.is_goal:
                result.solution = current
                result.depth = current.cost - initial.cost
                return result

            result.nodes_expanded += 1

            for neighbor in current.neighbors():
                result.nodes_generated += 1

                if neighbor.tiles not in visited:
                    visited.add(neighbor.tiles)
                    frontier.append(neighbor)

            if len(frontier) > result.max_frontier_size:
                result.max_frontier_size = len(frontier)

        return result

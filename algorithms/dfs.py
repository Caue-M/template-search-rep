from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [(initial, 0)]
        depths = {initial.tiles: 0}
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            current, depth = frontier.pop()

            if depth > depths[current.tiles]:
                continue

            if current.is_goal:
                result.solution = current
                result.depth = depth
                return result

            if depth >= self.depth_limit:
                continue

            result.nodes_expanded += 1

            for neighbor in reversed(current.neighbors()):
                result.nodes_generated += 1
                new_depth = depth + 1

                if neighbor.tiles not in depths or new_depth < depths[neighbor.tiles]:
                    depths[neighbor.tiles] = new_depth
                    frontier.append((neighbor, new_depth))

            if len(frontier) > result.max_frontier_size:
                result.max_frontier_size = len(frontier)

        return result

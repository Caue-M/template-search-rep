from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        children = []
        blank = self.blank_index
        row = blank // 3
        column = blank % 3
        moves = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]

        for row_change, column_change, action in moves:
            new_row = row + row_change
            new_column = column + column_change

            if 0 <= new_row < 3 and 0 <= new_column < 3:
                new_blank = new_row * 3 + new_column
                tiles = list(self.tiles)
                tiles[blank] = tiles[new_blank]
                tiles[new_blank] = 0
                child = State(tuple(tiles), self, action, self.cost + 1)
                children.append(child)

        return children

    def path(self) -> List["State"]:
        states = []
        current = self

        while current is not None:
            states.append(current)
            current = current.parent

        states.reverse()
        return states

    def actions(self) -> List[str]:
        actions = []

        for state in self.path():
            if state.parent is not None and state.action is not None:
                actions.append(state.action)

        return actions

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")

# leetcode 37: https://leetcode.cn/problems/sudoku-solver/

from typing import Tuple, Set, List


class Solution:
    def to_matrix(self, x: int) -> Tuple[int, int]:  # noqa
        return x // 9, x % 9

    def get_constraints(self, matrix: List[List[int]], x: int, y: int) -> Set[int]:  # noqa
        """
        获取同一 3x3 格子，同一行，同一列的所有数字
        """

        # 获取 3x3 格子的中间
        def get_center(a: int) -> int:
            if a in {0, 1, 2}:
                return 1
            elif a in {3, 4, 5}:
                return 4
            else:
                return 7

        center_x: int = get_center(x)
        center_y: int = get_center(y)
        s: Set[int] = set()
        # 获取同一 3x3 格子中的数字
        for coord in [
            (center_x - 1, center_y - 1), (center_x - 1, center_y), (center_x - 1, center_y + 1),
            (center_x, center_y - 1), (center_x, center_y), (center_x, center_y + 1),
            (center_x + 1, center_y - 1), (center_x + 1, center_y), (center_x + 1, center_y + 1)
        ]:
            if coord == (x, y):
                continue
            element: int = matrix[coord[0]][coord[1]]
            if element:
                s.add(element)

        # 获取同一行的数字
        for ind in range(0, 9):  # type: int
            if ind != y:
                element: int = matrix[x][ind]
                if element:
                    s.add(element)

        # 获取同一列的数字
        for ind in range(0, 9):  # type: int
            if ind != x:
                element: int = matrix[ind][y]
                if element:
                    s.add(element)

        return s

    def solveSudoku(self, board: List[List[str]]) -> None:  # noqa
        # 初始状态
        status: List[List[int]] = []
        for row in board:  # type: List[str]
            status.append([])
            for column in row:  # type: str
                if column == ".":
                    status[-1].append(0)
                else:
                    status[-1].append(int(column))

        top: int = 0
        while top < 81:
            x, y = self.to_matrix(top)  # type: int, int
            # 已给定数字直接填入
            if board[x][y] != ".":
                top += 1
                continue
            constraints: Set[int] = self.get_constraints(status, x, y)
            for new_value in range(status[x][y] + 1, 10):  # type: int
                if new_value in constraints:
                    continue
                status[x][y] = new_value
                top += 1
                break
            else:
                # 回溯到最近的 “.”
                top -= 1
                while top >= 0:
                    temp_x, temp_y = self.to_matrix(top)  # type: int, int
                    if board[temp_x][temp_y] != ".":
                        top -= 1
                        continue
                    break
                if top < 0:
                    break
                # 重置状态
                status[x][y] = 0
        else:
            for i in range(len(board)):  # type: int
                for j in range(len(board[i])):  # type: int
                    if board[i][j] == ".":
                        board[i][j] = str(status[i][j])
            return
        raise RuntimeError("no answer")


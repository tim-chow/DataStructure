import copy
from typing import List, Tuple


def search(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> List[List[Tuple[int, int]]]:
    result: List[List[Tuple[int, int]]] = []

    # 1 代表上面的格子待搜索；
    # 2 代表右面的格子待搜索
    # 3 代表下面的格子待搜索
    # 4 代表左面的格子待搜索
    # 5 代表上下左右都已搜索
    status: List[List[int]] = []
    for row in range(len(maze)):  # type: int
        status.append([1] * len(maze[row]))

    stack: List[Tuple[int, int]] = [start]
    while stack:
        current_expand_node: Tuple[int, int] = stack[-1]
        x, y = current_expand_node  # type: int, int
        match status[x][y]:
            case 1:
                status[x][y] = 2
                if x == 0:
                    continue
                next_node: Tuple[int, int] = (x - 1, y)
            case 2:
                status[x][y] = 3
                if y == len(maze[x]) - 1:
                    continue
                next_node: Tuple[int, int] = (x, y + 1)
            case 3:
                status[x][y] = 4
                if x == len(maze) - 1:
                    continue
                next_node: Tuple[int, int] = (x + 1, y)
            case 4:
                status[x][y] = 5
                if y == 0:
                    continue
                next_node: Tuple[int, int] = (x, y - 1)
            case _:
                # 无法继续向纵深方向前进
                # 恢复状态
                status[x][y] = 1
                # 将死节点从栈中弹出
                stack.pop(-1)
                continue
        x, y = next_node  # type: int, int
        # 新节点是墙
        if maze[x][y] == 0:
            continue
        # 已经在栈中
        if next_node in stack:
            continue
        # 到达终点
        if next_node == end:
            path: List[Tuple[int, int]] = copy.copy(stack)
            path.append(next_node)
            result.append(path)
            continue
        # 使其成为活结点
        stack.append(next_node)

    return result


def main() -> None:
    # 0 代表墙；1 代表路
    maze = [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
    ]
    for path in search(maze, (1, 0), (3, 0)):
        print(path)


if __name__ == "__main__":
    main()


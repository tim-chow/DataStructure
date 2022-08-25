from queue import PriorityQueue
from typing import List, Dict, Tuple

GraphType = Tuple[List[str], List[List[int]]]


def generate_direct_graph_example() -> GraphType:
    vertexes: List[str] = ['s', 'a', 'b', 'c', 'd', 'e',
                           'f', 'g', 'h', 'i', 't']
    arches: List[List[int]] = [
        [0, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 7, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    return vertexes, arches


def shortest_path(graph: GraphType, start: int) -> Dict[int, int]:
    queue: PriorityQueue = PriorityQueue()
    queue.put((0, start))
    result: Dict[int, int] = {}
    while not queue.empty():
        # 第一个活节点是当前扩展节点
        current_weight, index = queue.get()  # type: int, int
        # 列出当前扩展节点的所有孩子节点
        for index, weight in enumerate(graph[1][index]):  # type: int, int
            if not weight:
                continue
            # 剪去无法到达最优解的孩子节点
            if index in result and result[index] <= weight + current_weight:
                continue
            # 将其余孩子节点添加到活结点列表，并使用限界函数进行排序
            result[index] = weight + current_weight
            queue.put((result[index], index))
    return result


if __name__ == "__main__":
    graph: GraphType = generate_direct_graph_example()
    result: Dict[int, int] = shortest_path(graph, 0)
    for idx, weight in result.items():
        print(f"s -> {graph[0][idx]}: {weight}")

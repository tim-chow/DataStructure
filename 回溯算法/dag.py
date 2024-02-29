from typing import List, MutableMapping, Mapping


class Task:
    def __init__(self, name: str) -> None:
        # 任务名称
        self._name: str = name
        # 任务依赖的任务
        self._dependencies: List[Task] = []

    @property
    def name(self) -> str:
        """
        获取任务名称
        """
        return self._name

    def add_dependency(self, dependency: "Task") -> None:
        """
        添加依赖的任务
        :param dependency: 被依赖的任务
        """
        self._dependencies.append(dependency)

    @property
    def dependency_count(self) -> int:
        """
        获取依赖的任务的数量
        """
        return len(self._dependencies)

    def get_dependency(self, idx: int) -> "Task":
        """
        获取依赖的任务
        """
        return self._dependencies[idx]


def backtrace(dag: Mapping[str, List[str]]) -> None:
    # 定义问题的解空间；确定解空间的组织结构
    root: Task = Task("")
    cache: MutableMapping[str, Task] = {}
    for task, dependencies in dag.items():
        if task not in cache:
            cache[task] = Task(task)
        root.add_dependency(cache[task])
        for dependency in dependencies:
            if dependency not in cache:
                cache[dependency] = Task(dependency)
            cache[task].add_dependency(cache[dependency])

    stack: List[Task] = [root]
    status: MutableMapping[str, int] = {}
    visited: MutableMapping[str, bool] = {}
    while stack:
        current_node: Task = stack[-1]
        which_dependency: int = status.get(current_node.name, 0)
        # 无法继续向前搜索
        if which_dependency == current_node.dependency_count:
            if current_node is root:
                break
            print(f"execute {current_node.name}")
            visited[current_node.name] = True
            stack.pop(-1)
            continue
        # 到达新节点
        new_node: Task = current_node.get_dependency(which_dependency)
        status[current_node.name] = which_dependency + 1
        # 如果已经访问过，那么什么也不做
        if new_node.name in visited:
            continue
        # 如果未访问过，那么将其添加到活节点列表
        stack.append(new_node)


if __name__ == "__main__":
    backtrace({"a": ["b", "c"], "b": ["c", "d"], "c": ["e"], "d": ["f"], "e": ["f"]})


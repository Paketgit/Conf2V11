from cargo_fetcher import CargoDependencyFetcher
from typing import Set, Dict, List


class DependencyGraph:
    def __init__(self, fetcher: CargoDependencyFetcher):
        self.fetcher = fetcher
        self.graph: Dict[str, List[str]] = {}
        self.visited: Set[str] = set()
        self.cycles: List[List[str]] = []

    def build_graph_dfs(self, package: str, max_depth: int, filter_substring: str = None,
                        current_depth: int = 0, path: List[str] = None) -> None:
        if path is None:
            path = []

        if current_depth >= max_depth:
            return

        if package in path:
            cycle = path[path.index(package):] + [package]
            self.cycles.append(cycle)
            return

        if filter_substring and filter_substring in package:
            return

        if package in self.visited:
            return

        self.visited.add(package)
        current_path = path + [package]

        try:
            dependencies = self.fetcher.fetch_dependencies(package)
            self.graph[package] = dependencies

            for dep in dependencies:
                self.build_graph_dfs(dep, max_depth, filter_substring,
                                     current_depth + 1, current_path)

        except Exception as e:
            print(f"Ошибка при обработке пакета {package}: {e}")
            self.graph[package] = []

    def get_graph(self) -> Dict[str, List[str]]:
        return self.graph

    def get_cycles(self) -> List[List[str]]:
        return self.cycles

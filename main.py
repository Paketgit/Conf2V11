import argparse
import sys
from cargo_fetcher import CargoDependencyFetcher
from dependency_graph import DependencyGraph


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Инструмент визуализации графа зависимостей для Cargo'
    )

    parser.add_argument(
        '--package',
        required=True,
        help='Имя анализируемого пакета'
    )

    parser.add_argument(
        '--repository',
        required=True,
        help='URL-адрес репозитория или путь к файлу тестового репозитория'
    )

    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Режим работы с тестовым репозиторием'
    )

    parser.add_argument(
        '--version',
        help='Версия пакета'
    )

    parser.add_argument(
        '--max-depth',
        type=int,
        default=10,
        help='Максимальная глубина анализа зависимостей'
    )

    parser.add_argument(
        '--filter-substring',
        help='Подстрока для фильтрации пакетов'
    )

    return parser.parse_args()


def main():
    try:
        args = parse_arguments()

        fetcher = CargoDependencyFetcher(test_mode=args.test_mode)

        graph_builder = DependencyGraph(fetcher)
        graph_builder.build_graph_dfs(
            args.package,
            args.max_depth,
            args.filter_substring
        )

        graph = graph_builder.get_graph()
        cycles = graph_builder.get_cycles()

        print(f"\n=== Граф зависимостей для {args.package} (глубина: {args.max_depth}) ===")
        for package, deps in graph.items():
            filtered_deps = [d for d in deps if not args.filter_substring or args.filter_substring not in d]
            print(f"{package} -> {filtered_deps}")

        if cycles:
            print(f"\nОбнаружены циклические зависимости:")
            for cycle in cycles:
                print(f"  Цикл: {' -> '.join(cycle)}")
        else:
            print(f"\nЦиклические зависимости не обнаружены")

        print(f"Обработано пакетов -  {len(graph)}")

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

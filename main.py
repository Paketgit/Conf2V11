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

    parser.add_argument(
        '--reverse-deps',
        action='store_true',
        help='Показать обратные зависимости (пакеты, зависящие от указанного)'
    )

    parser.add_argument(
        '--installation-order',
        action='store_true',
        help='Показать порядок загрузки зависимостей'
    )

    return parser.parse_args()


def main():
    try:
        args = parse_arguments()

        fetcher = CargoDependencyFetcher(test_mode=args.test_mode)
        graph_builder = DependencyGraph(fetcher)

        if args.reverse_deps:
            print("Построение полного графа для поиска обратных зависимостей...")
            if args.test_mode:
                test_root_packages = ['A', 'B', 'C', 'serde', 'tokio']
                for root_pkg in test_root_packages:
                    try:
                        graph_builder.build_graph_dfs(
                            root_pkg,
                            args.max_depth,
                            args.filter_substring
                        )
                    except:
                        pass
            else:
                graph_builder.build_graph_dfs(
                    args.package,
                    args.max_depth,
                    args.filter_substring
                )
        else:
            graph_builder.build_graph_dfs(
                args.package,
                args.max_depth,
                args.filter_substring
            )

        graph = graph_builder.get_graph()
        cycles = graph_builder.get_cycles()

        # 3
        print(f"\n=== Граф зависимостей (глубина: {args.max_depth}) ===")
        if graph:
            for package, deps in graph.items():
                filtered_deps = [d for d in deps if not args.filter_substring or args.filter_substring not in d]
                print(f"{package} -> {filtered_deps}")
        else:
            print("Граф пуст")

        if cycles:
            print(f"\nОбнаружены циклические зависимости:")
            for cycle in cycles:
                print(f"Цикл: {' -> '.join(cycle)}")
        else:
            print(f"\nЦиклические зависимости не обнаружены")

        print(f"Обработано пакетов - {len(graph)}")

        # 4
        if args.reverse_deps:
            print(f"\n=== Обратные зависимости для {args.package} ===")
            reverse_deps = graph_builder.get_reverse_dependencies(args.package)
            if reverse_deps:
                print(f"Пакеты, зависящие от {args.package}:")
                for dep in reverse_deps:
                    print(f"  - {dep}")
                print(f"Всего обратных зависимостей: {len(reverse_deps)}")
            else:
                print(f"Обратные зависимости не найдены")
                if args.test_mode:
                    print("В тестовых данных проверьте зависимости пакетов A, B, C, E")

        if args.installation_order:
            print(f"\n=== Порядок загрузки зависимостей для {args.package} ===")
            order = graph_builder.get_installation_order(args.package)
            if order:
                for i, pkg in enumerate(order, 1):
                    print(f"{i:2d}. {pkg}")
            else:
                print("Не удалось определить порядок загрузки")

            print(f"\nСравнение с Cargo:")
            if args.test_mode:
                print("В тестовом режиме:")
                print("  - Порядок основан на топологической сортировке")
                print("  - Cargo использует более сложный алгоритм разрешения зависимостей")
                print("  - Учитываются feature flags и версионные ограничения")
            else:
                print("Возможные причины расхождений:")
                print("  1. Cargo учитывает семантическое версионирование")
                print("  2. Наличие опциональных зависимостей (features)")
                print("  3. Разные алгоритмы разрешения конфликтов версий")
                print("  4. Локальный кеш и уже установленные пакеты")
                print("\nДля точного сравнения:")
                print(f"  cargo tree --package {args.package} --invert")

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
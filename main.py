import argparse
import sys
from cargo_fetcher import CargoDependencyFetcher  # исправленное имя файла


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

        fetcher = CargoDependencyFetcher(test_mode=args.test_mode, crates_base_url=args.repository)

        dependencies = fetcher.fetch_dependencies(args.package, args.version)

        print(f"=== Прямые зависимости пакета {args.package} ===")
        if dependencies:
            for dep in dependencies:
                print(f"  - {dep}")
        else:
            print("зависимости отсутствуют")

        print(f"Найдено зависимостей - {len(dependencies)}")

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

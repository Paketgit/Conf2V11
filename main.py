import argparse
import sys
from typing import Dict, Any


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

        print("=== Параметры конфигурации ===")
        config_params = {
            'package': args.package,
            'repository': args.repository,
            'test_mode': args.test_mode,
            'version': args.version,
            'max_depth': args.max_depth,
            'filter_substring': args.filter_substring
        }

        for key, value in config_params.items():
            print(f"{key}: {value}")

        if not args.package:
            raise ValueError("Имя пакета не может быть пустым")

        if not args.repository:
            raise ValueError("Репозиторий empty()")

        if args.max_depth <= 0:
            raise ValueError("бро, давай глубину больше 0")

        print("Конфигурация успешно загружена")

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
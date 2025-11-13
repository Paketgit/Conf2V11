import requests
import json
import os
from typing import List, Dict


class CargoDependencyFetcher:
    def __init__(self, test_mode: bool = False, crates_base_url="https://crates.io/api/v1/crates"):
        self.test_mode = test_mode
        self.crates_base_url = crates_base_url

    def fetch_dependencies(self, package_name: str, version: str = None) -> List[str]:
        if self.test_mode:
            return self._fetch_test_dependencies(package_name)
        else:
            return self._fetch_real_dependencies(package_name, version)

    def _fetch_real_dependencies(self, package_name: str, version: str = None) -> List[str]:
        try:
            print(f"Запрос данных для пакета {package_name}...")

            if version:
                url = f"{self.crates_base_url}/{package_name}/{version}/dependencies"
            else:
                crate_info = requests.get(f"{self.crates_base_url}/{package_name}")
                crate_info.raise_for_status()
                crate_data = crate_info.json()
                version = crate_data["crate"]["newest_version"]
                url = f"{self.crates_base_url}/{package_name}/{version}/dependencies"

            print(f"Используется версия: {version}")

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            dependencies = [
                dep["crate_id"]
                for dep in data.get("dependencies", [])
                if dep.get("kind") == "normal"  # исключаем dev и build
            ]

            return dependencies

        except requests.RequestException as e:
            raise Exception(f"Ошибка при получении данных из crates.io: {e}")

    def _fetch_test_dependencies(self, package_name: str) -> List[str]:
        print(f"Тестовый режим для пакета {package_name}")

        test_file = f"test_{package_name}.json"

        if not os.path.exists(test_file):
            test_data = self._create_test_data(package_name)
            with open(test_file, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, indent=2, ensure_ascii=False)
            print(f"Создан тестовый файл: {test_file}")

        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)

        return test_data.get('dependencies', [])

    def _create_test_data(self, package_name: str) -> Dict:
        test_graphs = {
            'serde': ['serde_derive', 'serde_json', 'serde_yaml'],
            'serde_derive': ['proc-macro2', 'quote', 'syn'],
            'serde_json': ['itoa', 'ryu', 'serde'],
            'tokio': ['tokio-macros', 'mio', 'num_cpus'],
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': [],
            'E': ['F'],
            'F': []
        }

        deps = test_graphs.get(package_name, [])
        return {'package': package_name, 'dependencies': deps}

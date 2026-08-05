#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверка конфигурации проекта lessonNS04
Этот скрипт проверяет все настройки и зависимости
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from loguru import logger

# Настройка логирования
logger.remove()
logger.add(sys.stderr, level="INFO", format="{message}")


class ConfigValidator:
    """Класс для проверки конфигурации проекта"""
    
    def __init__(self, project_root: str):
        """
        Инициализация валидатора конфигурации
        
        Args:
            project_root: Корневая папка проекта
        """
        self.project_root = Path(project_root)
        self.required_files = [
            "README.md",
            "requirements.txt",
            ".gitignore",
            "homework-webhook.json"
        ]
        self.required_dirs = [
            "scripts",
            "docs"
        ]
        
    def check_file_exists(self, file_path: Path) -> bool:
        """
        Проверка существования файла
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            True если файл существует, иначе False
        """
        exists = file_path.exists()
        if exists:
            logger.success(f"Файл найден: {file_path.name}")
        else:
            logger.error(f"Файл не найден: {file_path.name}")
        return exists
    
    def check_directory_exists(self, dir_path: Path) -> bool:
        """
        Проверка существования директории
        
        Args:
            dir_path: Путь к директории
            
        Returns:
            True если директория существует, иначе False
        """
        exists = dir_path.exists() and dir_path.is_dir()
        if exists:
            logger.success(f"Директория найдена: {dir_path.name}")
        else:
            logger.error(f"Директория не найдена: {dir_path.name}")
        return exists
    
    def check_python_version(self) -> Tuple[bool, str]:
        """
        Проверка версии Python
        
        Returns:
            Кортеж (успех, версия Python)
        """
        try:
            version = sys.version.split()[0]
            major, minor = map(int, version.split('.')[:2])
            
            if major >= 3 and minor >= 8:
                logger.success(f"Python {version} (совместимо)")
                return True, version
            else:
                logger.warning(f"Python {version} (рекомендуется 3.8+)")
                return True, version
        except Exception as e:
            logger.error(f"Не удалось определить версию Python: {e}")
            return False, "unknown"
    
    def check_pip_packages(self) -> Dict[str, bool]:
        """
        Проверка установленных пакетов Python
        
        Returns:
            Словарь с результатами проверки
        """
        required_packages = [
            "requests",
            "python-dotenv",
            "loguru",
            "pydantic"
        ]
        
        results = {}
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_").split("[")[0])
                results[package] = True
                logger.success(f"Пакет установлен: {package}")
            except ImportError:
                results[package] = False
                logger.warning(f"Пакет не установлен: {package}")
        
        return results
    
    def check_env_file(self) -> Dict[str, bool]:
        """
        Проверка файла .env
        
        Returns:
            Словарь с результатами проверки переменных окружения
        """
        env_file = self.project_root / ".env"
        env_example = self.project_root / ".env.example"
        
        results = {
            "env_exists": env_file.exists(),
            "env_example_exists": env_example.exists()
        }
        
        if results["env_exists"]:
            logger.success("Файл .env найден")
            
            # Читаем переменные из .env
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            key = line.split("=")[0]
                            if "TOKEN" in key or "SECRET" in key or "PASSWORD" in key:
                                logger.info(f"  Найдена переменная: {key}=***")
                            else:
                                logger.info(f"  Найдена переменная: {key}")
        else:
            logger.warning("Файл .env не найден")
        
        if results["env_example_exists"]:
            logger.success("Файл .env.example найден")
        else:
            logger.info("Файл .env.example не найден (не обязательно)")
        
        return results
    
    def check_gitignore(self) -> bool:
        """
        Проверка файла .gitignore
        
        Returns:
            True если файл корректен
        """
        gitignore_path = self.project_root / ".gitignore"
        
        if not gitignore_path.exists():
            logger.error("Файл .gitignore не найден")
            return False
        
        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        required_entries = [
            "venv",
            "__pycache__",
            "*.pyc",
            ".env"
        ]
        
        missing_entries = []
        for entry in required_entries:
            if entry not in content:
                missing_entries.append(entry)
        
        if missing_entries:
            logger.warning(f"В .gitignore отсутствуют записи: {missing_entries}")
            return False
        else:
            logger.success("Файл .gitignore корректен")
            return True
    
    def check_workflow_json(self) -> bool:
        """
        Проверка JSON файла workflow
        
        Returns:
            True если файл корректен
        """
        workflow_path = self.project_root / "homework-webhook.json"
        
        if not workflow_path.exists():
            logger.error("Файл workflow не найден")
            return False
        
        try:
            with open(workflow_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Проверяем наличие основных полей
            if "nodes" in data:
                node_count = len(data["nodes"])
                logger.success(f"Workflow содержит {node_count} нод")
                
                # Проверяем наличие основных нод
                node_names = [node.get("name", "") for node in data.get("nodes", [])]
                required_nodes = ["Webhook", "Telegram"]
                
                for required in required_nodes:
                    if any(required.lower() in name.lower() for name in node_names):
                        logger.success(f"Найдена нода: {required}")
                    else:
                        logger.warning(f"Нода не найдена: {required}")
                
                return True
            else:
                logger.error("В JSON отсутствует поле 'nodes'")
                return False
                
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка чтения файла workflow: {e}")
            return False
    
    def run_full_validation(self) -> Dict[str, bool]:
        """
        Запуск полной проверки конфигурации
        
        Returns:
            Словарь с результатами проверки
        """
        logger.info("="*50)
        logger.info("ПРОВЕРКА КОНФИГУРАЦИИ ПРОЕКТА")
        logger.info("="*50)
        
        results = {}
        
        # Проверка версии Python
        python_ok, python_version = self.check_python_version()
        results["python_version"] = python_ok
        
        # Проверка необходимых файлов
        logger.info("\n--- Проверка файлов ---")
        for file_name in self.required_files:
            file_path = self.project_root / file_name
            results[f"file_{file_name}"] = self.check_file_exists(file_path)
        
        # Проверка необходимых директорий
        logger.info("\n--- Проверка директорий ---")
        for dir_name in self.required_dirs:
            dir_path = self.project_root / dir_name
            results[f"dir_{dir_name}"] = self.check_directory_exists(dir_path)
        
        # Проверка пакетов Python
        logger.info("\n--- Проверка пакетов Python ---")
        packages = self.check_pip_packages()
        results["packages"] = all(packages.values())
        
        # Проверка .env файла
        logger.info("\n--- Проверка переменных окружения ---")
        env_results = self.check_env_file()
        results["env"] = env_results.get("env_exists", False)
        
        # Проверка .gitignore
        logger.info("\n--- Проверка .gitignore ---")
        results["gitignore"] = self.check_gitignore()
        
        # Проверка workflow JSON
        logger.info("\n--- Проверка workflow ---")
        results["workflow"] = self.check_workflow_json()
        
        # Итоговый отчет
        logger.info("\n" + "="*50)
        logger.info("ИТОГОВЫЙ ОТЧЕТ")
        logger.info("="*50)
        
        all_ok = True
        for key, value in results.items():
            if isinstance(value, bool):
                status = "✓" if value else "✗"
                logger.info(f"{status} {key}: {'OK' if value else 'ОШИБКА'}")
                if not value:
                    all_ok = False
        
        if all_ok:
            logger.success("\nВсе проверки пройдены успешно!")
        else:
            logger.warning("\nОбнаружены проблемы. Проверьте логи выше.")
        
        return results


def main():
    """Основная функция скрипта"""
    # Определяем корневую папку проекта
    project_root = Path(__file__).parent.parent
    
    # Создаем валидатор
    validator = ConfigValidator(project_root)
    
    # Запускаем проверку
    results = validator.run_full_validation()
    
    # Возвращаем код завершения
    return 0 if all(v for v in results.values() if isinstance(v, bool)) else 1


if __name__ == "__main__":
    sys.exit(main())

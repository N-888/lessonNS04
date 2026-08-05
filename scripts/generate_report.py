#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерация отчета по выполнению домашнего задания NS04
Этот скрипт проверяет все компоненты и генерирует отчет
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from loguru import logger

# Настройка логирования
logger.remove()
logger.add(sys.stderr, level="INFO", format="{message}")


class HomeworkReporter:
    """Класс для генерации отчета по домашнему заданию"""
    
    def __init__(self, project_root: str):
        """
        Инициализация генератора отчета
        
        Args:
            project_root: Корневая папка проекта
        """
        self.project_root = Path(project_root)
        self.report_data = {
            "project_name": "NS04 - Автоматизация обработки заявок",
            "generated_at": datetime.now().isoformat(),
            "checks": [],
            "screenshots_needed": [],
            "tasks_completed": [],
            "tasks_pending": []
        }
    
    def check_project_structure(self) -> bool:
        """
        Проверка структуры проекта
        
        Returns:
            True если структура корректна
        """
        logger.info("Проверка структуры проекта...")
        
        required_items = {
            "files": ["README.md", "requirements.txt", ".gitignore", "homework-webhook.json"],
            "dirs": ["scripts", "docs"]
        }
        
        all_ok = True
        
        # Проверка файлов
        for file_name in required_items["files"]:
            file_path = self.project_root / file_name
            if file_path.exists():
                self.report_data["checks"].append({
                    "item": file_name,
                    "status": "OK",
                    "message": f"Файл {file_name} найден"
                })
                logger.success(f"✓ {file_name}")
            else:
                self.report_data["checks"].append({
                    "item": file_name,
                    "status": "ERROR",
                    "message": f"Файл {file_name} не найден"
                })
                logger.error(f"✗ {file_name}")
                all_ok = False
        
        # Проверка директорий
        for dir_name in required_items["dirs"]:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.report_data["checks"].append({
                    "item": dir_name,
                    "status": "OK",
                    "message": f"Директория {dir_name} найдена"
                })
                logger.success(f"✓ {dir_name}/")
            else:
                self.report_data["checks"].append({
                    "item": dir_name,
                    "status": "ERROR",
                    "message": f"Директория {dir_name} не найдена"
                })
                logger.error(f"✗ {dir_name}/")
                all_ok = False
        
        return all_ok
    
    def check_workflow_json(self) -> bool:
        """
        Проверка файла workflow
        
        Returns:
            True если файл корректен
        """
        logger.info("Проверка workflow JSON...")
        
        workflow_path = self.project_root / "homework-webhook.json"
        
        if not workflow_path.exists():
            self.report_data["checks"].append({
                "item": "workflow",
                "status": "ERROR",
                "message": "Файл workflow не найден"
            })
            return False
        
        try:
            with open(workflow_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Проверяем наличие основных нод
            nodes = data.get("nodes", [])
            node_names = [node.get("name", "") for node in nodes]
            
            required_nodes = ["Webhook", "Telegram"]
            found_nodes = []
            
            for required in required_nodes:
                if any(required.lower() in name.lower() for name in node_names):
                    found_nodes.append(required)
                    self.report_data["checks"].append({
                        "item": f"node_{required}",
                        "status": "OK",
                        "message": f"Нода {required} найдена в workflow"
                    })
                    logger.success(f"✓ Нода {required}")
                else:
                    self.report_data["checks"].append({
                        "item": f"node_{required}",
                        "status": "WARNING",
                        "message": f"Нода {required} не найдена в workflow"
                    })
                    logger.warning(f"⚠ Нода {required} не найдена")
            
            # Проверяем наличие Бипиум
            if any("бипиум" in name.lower() or "bpium" in name.lower() for name in node_names):
                self.report_data["checks"].append({
                    "item": "node_Бипиум",
                    "status": "OK",
                    "message": "Нода Бипиум найдена в workflow"
                })
                logger.success("✓ Нода Бипиум")
            else:
                self.report_data["checks"].append({
                    "item": "node_Бипиум",
                    "status": "INFO",
                    "message": "Нода Бипиум не найдена (дополнительное задание)"
                })
                logger.info("ℹ Нода Бипиум не найдена (дополнительное задание)")
            
            return True
            
        except json.JSONDecodeError as e:
            self.report_data["checks"].append({
                "item": "workflow",
                "status": "ERROR",
                "message": f"Ошибка парсинга JSON: {e}"
            })
            logger.error(f"Ошибка парсинга JSON: {e}")
            return False
    
    def generate_screenshots_checklist(self):
        """
        Генерация списка необходимых скриншотов
        """
        logger.info("Генерация списка скриншотов...")
        
        self.report_data["screenshots_needed"] = [
            {
                "id": 1,
                "name": "Workflow в n8n",
                "description": "Скриншот workflow с тремя нодами (Webhook → Telegram → Airtable/Бипиум)",
                "required": True
            },
            {
                "id": 2,
                "name": "Сообщение в Telegram",
                "description": "Скриншот сообщения от бота с данными заявки",
                "required": True
            },
            {
                "id": 3,
                "name": "Таблица Airtable",
                "description": "Скриншот таблицы Airtable с новой строкой заявки",
                "required": True
            },
            {
                "id": 4,
                "name": "Нода HTTP Request",
                "description": "Скриншот ноды HTTP Request с зелёным Output (для Бипиум)",
                "required": False
            },
            {
                "id": 5,
                "name": "Таблица Бипиум",
                "description": "Скриншот таблицы Бипиум с новой заявкой",
                "required": False
            }
        ]
    
    def generate_task_checklist(self):
        """
        Генерация чек-листа задач
        """
        logger.info("Генерация чек-листа задач...")
        
        self.report_data["tasks_completed"] = [
            "Создание структуры папки проекта",
            "Создание файла .gitignore",
            "Создание файла requirements.txt",
            "Создание файла README.md",
            "Создание workflow JSON для импорта",
            "Создание скриптов для тестирования",
            "Создание документации"
        ]
        
        self.report_data["tasks_pending"] = [
            "Регистрация в n8n Cloud",
            "Создание Telegram бота",
            "Получение Chat ID",
            "Настройка webhook в n8n",
            "Настройка ноды Telegram",
            "Тестирование отправки в Telegram",
            "Создание таблицы в Airtable",
            "Получение Access Token Airtable",
            "Настройка ноды Airtable",
            "Создание каталога в Бипиум",
            "Настройка ноды HTTP Request",
            "Финальное тестирование всего workflow",
            "Активация workflow",
            "Создание скриншотов",
            "Обновление README.md"
        ]
    
    def generate_report(self) -> str:
        """
        Генерация итогового отчета
        
        Returns:
            Текст отчета
        """
        report_lines = []
        
        report_lines.append("="*60)
        report_lines.append("ОТЧЕТ ПО ВЫПОЛНЕНИЮ ДОМАШНЕГО ЗАДАНИЯ NS04")
        report_lines.append("="*60)
        report_lines.append(f"Проект: {self.report_data['project_name']}")
        report_lines.append(f"Дата генерации: {self.report_data['generated_at']}")
        report_lines.append("")
        
        # Проверки
        report_lines.append("РЕЗУЛЬТАТЫ ПРОВЕРОК:")
        report_lines.append("-"*40)
        
        ok_count = sum(1 for check in self.report_data["checks"] if check["status"] == "OK")
        warning_count = sum(1 for check in self.report_data["checks"] if check["status"] == "WARNING")
        error_count = sum(1 for check in self.report_data["checks"] if check["status"] == "ERROR")
        
        for check in self.report_data["checks"]:
            status_icon = {
                "OK": "✓",
                "WARNING": "⚠",
                "ERROR": "✗",
                "INFO": "ℹ"
            }.get(check["status"], "?")
            
            report_lines.append(f"{status_icon} {check['item']}: {check['message']}")
        
        report_lines.append("")
        report_lines.append(f"ИТОГО: OK - {ok_count}, Предупреждения - {warning_count}, Ошибки - {error_count}")
        report_lines.append("")
        
        # Скриншоты
        report_lines.append("НЕОБХОДИМЫЕ СКРИНШОТЫ:")
        report_lines.append("-"*40)
        
        for screenshot in self.report_data["screenshots_needed"]:
            required_text = "(ОБЯЗАТЕЛЬНО)" if screenshot["required"] else "(опционально)"
            report_lines.append(f"{screenshot['id']}. {screenshot['name']} {required_text}")
            report_lines.append(f"   {screenshot['description']}")
        
        report_lines.append("")
        
        # Задачи
        report_lines.append("ВЫПОЛНЕННЫЕ ЗАДАЧИ:")
        report_lines.append("-"*40)
        
        for task in self.report_data["tasks_completed"]:
            report_lines.append(f"✓ {task}")
        
        report_lines.append("")
        
        report_lines.append("ОЖИДАЮТ ВЫПОЛНЕНИЯ:")
        report_lines.append("-"*40)
        
        for task in self.report_data["tasks_pending"]:
            report_lines.append(f"☐ {task}")
        
        report_lines.append("")
        report_lines.append("="*60)
        report_lines.append("КОНТАКТЫ ДЛЯ ПОДДЕРЖКИ:")
        report_lines.append("Telegram: @Tpomoschnik")
        report_lines.append("Телефон: +7-925-104-10-73")
        report_lines.append("Email: mamambell@gmail.com")
        report_lines.append("GitHub: N-888")
        report_lines.append("="*60)
        
        return "\n".join(report_lines)
    
    def save_report(self, report_text: str):
        """
        Сохранение отчета в файл
        
        Args:
            report_text: Текст отчета
        """
        report_path = self.project_root / "homework_report.txt"
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        
        logger.success(f"Отчет сохранен: {report_path}")
    
    def run(self):
        """
        Запуск генерации отчета
        """
        logger.info("Запуск генерации отчета по домашнему заданию NS04")
        
        # Выполняем проверки
        self.check_project_structure()
        self.check_workflow_json()
        
        # Генерируем списки
        self.generate_screenshots_checklist()
        self.generate_task_checklist()
        
        # Генерируем отчет
        report_text = self.generate_report()
        
        # Сохраняем отчет
        self.save_report(report_text)
        
        # Выводим отчет
        print("\n" + report_text)
        
        logger.success("Генерация отчета завершена")


def main():
    """Основная функция скрипта"""
    # Определяем корневую папку проекта
    project_root = Path(__file__).parent.parent
    
    # Создаем генератор отчета
    reporter = HomeworkReporter(project_root)
    
    # Запускаем генерацию
    reporter.run()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

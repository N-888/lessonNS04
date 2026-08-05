#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Помощник для работы с Git в проекте lessonNS04
Этот скрипт помогает с основными операциями Git
"""

import os
import sys
import subprocess
from pathlib import Path
from loguru import logger

# Настройка логирования
logger.remove()
logger.add(sys.stderr, level="INFO", format="{message}")


class GitHelper:
    """Класс для помощи с Git операциями"""
    
    def __init__(self, project_root: str):
        """
        Инициализация помощника Git
        
        Args:
            project_root: Корневая папка проекта
        """
        self.project_root = Path(project_root)
    
    def run_git_command(self, command: list) -> tuple:
        """
        Выполнение команды Git
        
        Args:
            command: Список аргументов команды
            
        Returns:
            Кортеж (stdout, stderr, returncode)
        """
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            logger.error(f"Ошибка выполнения команды Git: {e}")
            return "", str(e), 1
    
    def init_repo(self):
        """Инициализация Git репозитория"""
        logger.info("Инициализация Git репозитория...")
        
        stdout, stderr, returncode = self.run_git_command(["init"])
        
        if returncode == 0:
            logger.success("Git репозиторий успешно инициализирован")
        else:
            logger.error(f"Ошибка инициализации: {stderr}")
        
        return returncode == 0
    
    def add_files(self, files: list = None):
        """
        Добавление файлов в индекс
        
        Args:
            files: Список файлов для добавления (None = все файлы)
        """
        if files is None:
            logger.info("Добавление всех файлов в индекс...")
            stdout, stderr, returncode = self.run_git_command(["add", "."])
        else:
            logger.info(f"Добавление файлов: {files}")
            stdout, stderr, returncode = self.run_git_command(["add"] + files)
        
        if returncode == 0:
            logger.success("Файлы успешно добавлены в индекс")
        else:
            logger.error(f"Ошибка добавления: {stderr}")
        
        return returncode == 0
    
    def commit(self, message: str):
        """
        Создание коммита
        
        Args:
            message: Сообщение коммита
        """
        logger.info(f"Создание коммита: {message}")
        
        stdout, stderr, returncode = self.run_git_command(["commit", "-m", message])
        
        if returncode == 0:
            logger.success("Коммит успешно создан")
        else:
            logger.error(f"Ошибка создания коммита: {stderr}")
        
        return returncode == 0
    
    def status(self):
        """Получение статуса репозитория"""
        logger.info("Получение статуса Git...")
        
        stdout, stderr, returncode = self.run_git_command(["status"])
        
        if returncode == 0:
            logger.info("Статус репозитория:")
            print(stdout)
        else:
            logger.error(f"Ошибка получения статуса: {stderr}")
        
        return returncode == 0
    
    def log(self, count: int = 10):
        """
        Получение истории коммитов
        
        Args:
            count: Количество последних коммитов
        """
        logger.info(f"Получение последних {count} коммитов...")
        
        stdout, stderr, returncode = self.run_git_command(["log", f"--oneline", f"-{count}"])
        
        if returncode == 0:
            logger.info("История коммитов:")
            print(stdout)
        else:
            logger.error(f"Ошибка получения лога: {stderr}")
        
        return returncode == 0
    
    def diff(self):
        """Показ изменений"""
        logger.info("Показ изменений...")
        
        stdout, stderr, returncode = self.run_git_command(["diff"])
        
        if returncode == 0:
            if stdout:
                logger.info("Изменения:")
                print(stdout)
            else:
                logger.info("Нет изменений")
        else:
            logger.error(f"Ошибка показа изменений: {stderr}")
        
        return returncode == 0
    
    def create_initial_commit(self):
        """Создание первоначального коммита"""
        logger.info("Создание первоначального коммита...")
        
        # Добавляем все файлы
        if not self.add_files():
            return False
        
        # Создаем коммит
        if not self.commit("Начальный коммит: структура проекта lessonNS04"):
            return False
        
        logger.success("Первоначальный коммит создан успешно")
        return True
    
    def setup_remote(self, remote_name: str, remote_url: str):
        """
        Настройка удаленного репозитория
        
        Args:
            remote_name: Имя удаленного репозитория
            remote_url: URL удаленного репозитория
        """
        logger.info(f"Настройка удаленного репозитория: {remote_name}")
        
        # Удаляем существующий remote если есть
        self.run_git_command(["remote", "remove", remote_name])
        
        # Добавляем новый remote
        stdout, stderr, returncode = self.run_git_command(["remote", "add", remote_name, remote_url])
        
        if returncode == 0:
            logger.success(f"Удаленный репозиторий {remote_name} добавлен")
        else:
            logger.error(f"Ошибка добавления remote: {stderr}")
        
        return returncode == 0
    
    def push(self, remote: str = "origin", branch: str = "main"):
        """
        Отправка изменений на удаленный репозиторий
        
        Args:
            remote: Имя удаленного репозитория
            branch: Имя ветки
        """
        logger.info(f"Отправка изменений на {remote}/{branch}...")
        
        stdout, stderr, returncode = self.run_git_command(["push", remote, branch])
        
        if returncode == 0:
            logger.success("Изменения успешно отправлены")
        else:
            logger.error(f"Ошибка отправки: {stderr}")
        
        return returncode == 0


def main():
    """Основная функция скрипта"""
    # Определяем корневую папку проекта
    project_root = Path(__file__).parent.parent
    
    # Создаем помощник Git
    helper = GitHelper(project_root)
    
    # Показываем меню
    print("\n" + "="*50)
    print("ПОМОЩНИК GIT ДЛЯ ПРОЕКТА lessonNS04")
    print("="*50)
    print("1. Инициализировать Git репозиторий")
    print("2. Показать статус")
    print("3. Добавить все файлы")
    print("4. Создать коммит")
    print("5. Показать историю коммитов")
    print("6. Показать изменения")
    print("7. Создать первоначальный коммит")
    print("0. Выход")
    print("="*50)
    
    while True:
        choice = input("\nВыберите действие (0-7): ").strip()
        
        if choice == "1":
            helper.init_repo()
        elif choice == "2":
            helper.status()
        elif choice == "3":
            helper.add_files()
        elif choice == "4":
            message = input("Введите сообщение коммита: ").strip()
            if message:
                helper.commit(message)
            else:
                logger.warning("Сообщение коммита не может быть пустым")
        elif choice == "5":
            helper.log()
        elif choice == "6":
            helper.diff()
        elif choice == "7":
            helper.create_initial_commit()
        elif choice == "0":
            logger.info("Выход из помощника Git")
            break
        else:
            logger.warning("Неверный выбор. Попробуйте снова.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

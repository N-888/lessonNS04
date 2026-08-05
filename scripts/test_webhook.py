#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование webhook для проекта lessonNS04
Этот скрипт отправляет тестовые данные на webhook n8n
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from loguru import logger

# Настройка логирования
logger.remove()  # Удаляем стандартный обработчик
logger.add(
    "logs/webhook_test_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(sys.stderr, level="INFO", format="{message}")


class WebhookTester:
    """Класс для тестирования webhook"""
    
    def __init__(self, webhook_url: str):
        """
        Инициализация тестировщика webhook
        
        Args:
            webhook_url: URL webhook для тестирования
        """
        self.webhook_url = webhook_url
        self.test_data = []
        
    def create_test_payload(self, name: str, email: str, phone: str) -> Dict[str, Any]:
        """
        Создание тестового payload для webhook
        
        Args:
            name: Имя тестового пользователя
            email: Email тестового пользователя
            phone: Телефон тестового пользователя
            
        Returns:
            Словарь с тестовыми данными
        """
        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.debug(f"Создан тестовый payload: {payload}")
        return payload
    
    def send_webhook_request(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Отправка запроса на webhook
        
        Args:
            payload: Данные для отправки
            
        Returns:
            Ответ сервера или None в случае ошибки
        """
        try:
            # Формируем URL с параметрами для GET запроса
            params = {
                "name": payload["name"],
                "email": payload["email"],
                "phone": payload["phone"]
            }
            
            logger.info(f"Отправка запроса на webhook: {self.webhook_url}")
            logger.debug(f"Параметры запроса: {params}")
            
            response = requests.get(
                self.webhook_url,
                params=params,
                timeout=10
            )
            
            logger.info(f"Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                logger.success("Webhook успешно обработал запрос")
                return response.json() if response.text else {"status": "success"}
            else:
                logger.error(f"Webhook вернул ошибку: {response.status_code}")
                logger.debug(f"Тело ответа: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при отправке запроса: {e}")
            return None
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")
            return None
    
    def run_tests(self, test_cases: list) -> Dict[str, Any]:
        """
        Запуск серии тестов
        
        Args:
            test_cases: Список тестовых случаев
            
        Returns:
            Результаты тестирования
        """
        results = {
            "total": len(test_cases),
            "success": 0,
            "failed": 0,
            "details": []
        }
        
        logger.info(f"Запуск {len(test_cases)} тестов")
        
        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"Тест {i}/{len(test_cases)}: {test_case['name']}")
            
            payload = self.create_test_payload(
                name=test_case["name"],
                email=test_case["email"],
                phone=test_case["phone"]
            )
            
            response = self.send_webhook_request(payload)
            
            test_result = {
                "test_case": test_case["name"],
                "payload": payload,
                "response": response,
                "success": response is not None
            }
            
            results["details"].append(test_result)
            
            if response is not None:
                results["success"] += 1
                logger.success(f"Тест '{test_case['name']}' пройден")
            else:
                results["failed"] += 1
                logger.error(f"Тест '{test_case['name']}' не пройден")
        
        logger.info(f"Итоги тестирования: {results['success']}/{results['total']} успешно")
        return results


def main():
    """Основная функция скрипта"""
    # Конфигурация
    WEBHOOK_URL = "https://your-n8n.com/webhook/new-lead"  # Замените на ваш URL
    
    # Тестовые случаи
    test_cases = [
        {
            "name": "Тест 1: Базовый тест",
            "name": "Иван Петров",
            "email": "ivan@example.com",
            "phone": "+79991234567"
        },
        {
            "name": "Тест 2: Кириллица",
            "name": "Мария Иванова",
            "email": "maria@example.com",
            "phone": "+79997654321"
        },
        {
            "name": "Тест 3: Специальные символы",
            "name": "Тест User",
            "email": "test@example.com",
            "phone": "+7(999)123-45-67"
        }
    ]
    
    # Создаем тестировщик
    tester = WebhookTester(WEBHOOK_URL)
    
    # Запускаем тесты
    results = tester.run_tests(test_cases)
    
    # Выводим результаты
    print("\n" + "="*50)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("="*50)
    print(f"Всего тестов: {results['total']}")
    print(f"Успешно: {results['success']}")
    print(f"Неудачно: {results['failed']}")
    print("="*50)
    
    # Детали по каждому тесту
    for detail in results["details"]:
        status = "✓" if detail["success"] else "✗"
        print(f"{status} {detail['test_case']}")
        if not detail["success"]:
            print(f"  Ошибка: {detail['response']}")
    
    return 0 if results["failed"] == 0 else 1


if __name__ == "__main__":
    # Создаем папку для логов если её нет
    import os
    os.makedirs("logs", exist_ok=True)
    
    sys.exit(main())

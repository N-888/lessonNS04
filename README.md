# Автоматизация обработки заявок: n8n + Telegram + Таблицы

Современная система автоматизации обработки заявок с интеграцией мессенджеров и баз данных. Проект демонстрирует построение полноценного workflow для бизнес-процессов с соблюдением требований 152-ФЗ.

## Возможности системы

### Основной функционал
- **Приём заявок через Webhook** - универсальный входной интерфейс для любых источников данных
- **Мгновенные уведомления в Telegram** - получайте заявки в реальном времени
- **Автоматическое сохранение в таблицы** - Airtable (международный) и Бипиум (российский, 152-ФЗ)
- **Полная отслеживаемость** - логирование каждого этапа обработки

### Технические особенности
- Модульная архитектура для легкого расширения
- Обработка ошибок на каждом этапе
- Детальное логирование всех действий
- Готовность к интеграции с внешними сервисами
- Соответствие требованиям безопасности

## Архитектура решения

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Источник      │    │    Webhook      │    │    Telegram     │    │    Таблицы      │
│   заявок        │───▶│   (Приём)      │───▶│  (Уведомление)  │───▶│  (Хранение)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                       │                       │
                              ▼                       ▼                       ▼
                        ┌─────────┐             ┌─────────┐             ┌─────────┐
                        │  JSON   │             │  Бот    │             │ Airtable│
                        │  данные │             │  n8n    │             │ Бипиум  │
                        └─────────┘             └─────────┘             └─────────┘
```

## Быстрый старт

### Предварительные требования
- Аккаунт n8n Cloud (или локальная установка)
- Telegram бот (создаётся через @BotFather)
- Аккаунт Airtable (для международного варианта)
- Аккаунт Бипиум (для российского варианта, 152-ФЗ)

### Установка и настройка

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/N-888/lessonNS04.git
   cd lessonNS04
   ```

2. **Установите зависимости** (опционально, для локальных скриптов)
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте переменные окружения** (если используете локальные скрипты)
   ```bash
   cp .env.example .env
   # Заполните значения в файле .env
   ```

4. **Импортируйте workflow в n8n**
   - Откройте n8n
   - Нажмите "Import from File"
   - Выберите файл `homework-webhook.json`

5. **Настройте.credentials**
   - Telegram Bot Token
   - Airtable Access Token (если используете)
   - Данные для Бипиум (если используете)

## Структура проекта

```
lessonNS04/
├── README.md                 # Этот файл с документацией
├── .gitignore               # Файлы, которые Git будет игнорировать
├── requirements.txt         # Зависимости Python (опционально)
├── homework-webhook.json    # Готовый workflow для импорта в n8n
├── docs/                    # Документация
│   ├── setup.md            # Инструкция по настройке
│   ├── api.md              # Документация по API
│   └── troubleshooting.md  # Решение проблем
├── scripts/                 # Вспомогательные скрипты
│   ├── test_webhook.py     # Тестирование webhook
│   ├── validate_config.py  # Проверка конфигурации
│   └── export_data.py      # Экспорт данных
└── examples/               # Примеры использования
    ├── basic_workflow.json
    └── advanced_workflow.json
```

## Настройка интеграций

### 1. Telegram Bot
```python
# Пример создания бота через API
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    return response.json()
```

### 2. Airtable Integration
```python
# Пример работы с Airtable API
import requests

AIRTABLE_TOKEN = "YOUR_AIRTABLE_TOKEN"
BASE_ID = "YOUR_BASE_ID"
TABLE_NAME = "Orders"

def create_airtable_record(name, email, phone):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "name": name,
            "email": email,
            "phone": phone
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
```

### 3. Бипиум Integration (152-ФЗ)
```python
# Пример работы с API Бипиум
import requests
import base64

BPium_DOMAIN = "your-domain"
CATALOG_ID = 16
EMAIL = "your-email"
PASSWORD = "your-password"

def create_bpium_record(name, email, phone):
    url = f"https://{BPium_DOMAIN}.bpium.ru/api/v1/catalogs/{CATALOG_ID}/records"
    
    # Авторизация
    auth_string = f"{EMAIL}:{PASSWORD}"
    auth_bytes = auth_string.encode("ascii")
    auth_b64 = base64.b64encode(auth_bytes).decode("ascii")
    
    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "values": {
            "2": name,    # Поле "Имя"
            "3": email,   # Поле "Почта"
            "4": phone    # Поле "Телефон"
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
```

## Примеры использования

### Базовый workflow
```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "GET",
        "path": "new-lead"
      }
    },
    {
      "name": "Telegram",
      "type": "n8n-nodes-base.telegram",
      "parameters": {
        "chatId": "YOUR_CHAT_ID",
        "text": "Новая заявка: {{ $json.query.name }}"
      }
    }
  ]
}
```

### Расширенный workflow с условиями
```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook"
    },
    {
      "name": "Check Email",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "string": [{
            "value1": "={{ $json.query.email }}",
            "operation": "contains",
            "value2": "@gmail.com"
          }]
        }
      }
    },
    {
      "name": "Process Gmail",
      "type": "n8n-nodes-base.set"
    }
  ]
}
```

## Тестирование

### Запуск тестов
```bash
# Тестирование webhook
python scripts/test_webhook.py

# Проверка конфигурации
python scripts/validate_config.py

# Экспорт данных
python scripts/export_data.py
```

### Ручное тестирование
1. Откройте n8n и активируйте workflow
2. Перейдите по URL webhook с параметрами:
   ```
   https://your-n8n.com/webhook/new-lead?email=test@example.com&name=Тест&phone=+79991234567
   ```
3. Проверьте:
   - Сообщение в Telegram
   - Запись в Airtable
   - Запись в Бипиум (если настроено)

## Решение проблем

### Частые ошибки

**Ошибка: "Cannot find module"**
```bash
pip install -r requirements.txt
```

**Ошибка: "Invalid credentials"**
- Проверьте токены в настройках n8n
- Убедитесь, что токены не истекли

**Ошибка: "Webhook not receiving data"**
- Проверьте, что workflow активен
- Убедитесь, что URL webhook корректен

### Логирование
Все действия логируются в файл `n8n.log`. Проверьте его при проблемах:
```bash
tail -f n8n.log
```

## Безопасность

### Рекомендации
- Никогда не коммитьте реальные токены и пароли
- Используйте переменные окружения
- Регулярно обновляйте зависимости
- Следите за уязвимостями в зависимостях

### Соответствие 152-ФЗ
- Используйте Бипиум для хранения персональных данных
- Не храните персональные данные в Airtable (это зарубежный сервис)
- Реализуйте механизм удаления данных по запросу

## Масштабирование

### Добавление новых источников
1. Создайте新的 Webhook endpoint
2. Добавьте ноду обработки
3. Подключите к существующим нодам уведомлений и хранения

### Интеграция с CRM
```python
# Пример интеграции с amoCRM
def create_amoCRM_contact(name, email, phone):
    # Реализация интеграции
    pass
```

### Мобильное приложение
- Используйте webhook как API для мобильного приложения
- Реализуйте аутентификацию через JWT
- Добавьте rate limiting

## Контакты

**Разработчик:** Telegram: @Tpomoschnik

**Техническая поддержка:**
- Telegram: @Tpomoschnik
- Телефон: +7-925-104-10-73
- Email: mamambell@gmail.com

**GitHub:** [N-888](https://github.com/N-888)

## Лицензия

MIT License - свободное использование и модификация

---

**Версия:** 1.0.0  
**Последнее обновление:** Август 2026  
**Совместимость:** n8n Cloud, n8n Self-hosted

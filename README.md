<div align="center">

# 🚀 Автоматизация обработки заявок

### n8n + Telegram + Таблицы

**Современная система автоматизации бизнес-процессов**

[![GitHub](https://img.shields.io/badge/GitHub-N--888-181717?style=for-the-badge&logo=github)](https://github.com/N-888)
[![n8n](https://img.shields.io/badge/n8n-Workflow-orange?style=for-the-badge&logo=n8n)](https://n8n.io)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram)](https://telegram.org)
[![152-ФЗ](https://img.shields.io/badge/152--ФЗ-Соответствие-green?style=for-the-badge)](https://base.garant.ru/70484638/)

</div>

---

## 🎯 Что решает этот проект

```
📱 Заявка с сайта → 📨 Мгновенное уведомление в Telegram → 💾 Автоматическое сохранение в таблицу
```

**Забудьте о ручной обработке заявок!** Наша система автоматически:
- Принимает данные с любого источника (сайт, форма, API)
- Мгновенно отправляет уведомление ответственному
- Сохраняет всё в структурированную базу данных

---

## ✨ Ключевые преимущества

| Преимущество | Описание |
|--------------|----------|
| ⚡ **Мгновенная скорость** | Обработка заявки за секунды |
| 🔒 **Безопасность 152-ФЗ** | Российское хранилище данных (Бипиум) |
| 🔄 **Полная автоматизация** | Без участия человека |
| 📊 **Структурированные данные** | Всё в таблицах для аналитики |
| 🛡️ **Надёжность** | Обработка ошибок на каждом этапе |

---

## 🏗️ Архитектура решения

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          🔄 ПРОЦЕСС ОБРАБОТКИ                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   📥 ВХОД              ⚙️ ОБРАБОТКА           📤 ВЫХОД                     │
│                                                                             │
│   ┌─────────┐         ┌─────────┐           ┌─────────┐                     │
│   │ Webhook │────────▶│Telegram │──────────▶│Airtable │                     │
│   │ (API)   │         │  Бот    │           │  БД     │                     │
│   └─────────┘         └─────────┘           └─────────┘                     │
│        │                                                                │
│        └──────────────────────────────────────────▶│                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Webhook → Telegram (параллельно)
Webhook → Airtable (параллельно)
Telegram → Airtable (дополнительная связь)
```

---

## 🚀 Быстрый старт

### Предварительные требования

| Сервис | Назначение | Статус |
|--------|------------|--------|
| [n8n](https://n8n.io) | Автоматизация workflows | ✅ Готово |
| [Telegram BotFather](https://t.me/BotFather) | Создание бота | ⏳ Настроить |
| [Airtable](https://airtable.com) | Международная БД | ⏳ Настроить |
| [Бипиум](https://bpium.ru) | Российская БД (152-ФЗ) | ⏳ Настроить |

### Установка за 3 шага

#### Шаг 1: Клонируйте проект
```bash
git clone https://github.com/N-888/lessonNS04.git
cd lessonNS04
```

#### Шаг 2: Установите зависимости (опционально)
```bash
pip install -r requirements.txt
```

#### Шаг 3: Импортируйте в n8n
1. Откройте n8n → `http://localhost:5678`
2. Menu (☰) → **Import from File**
3. Выберите `workflow.json`

---

## 📁 Структура проекта

```
lessonNS04/
│
├── 📄 README.md                 # Документация проекта
├── 📄 .gitignore               # Исключения Git
├── 📄 requirements.txt         # Зависимости Python
└── 📄 workflow.json            # Workflow для n8n (Webhook → Telegram → Airtable)
```

---

## 🔌 Интеграции

### 1. Telegram Bot

```python
# Отправка уведомлений в Telegram
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_notification(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    return requests.post(url, json=payload).json()
```

### 2. Airtable (Международный)

```python
# Сохранение данных в Airtable
import requests

AIRTABLE_TOKEN = "YOUR_TOKEN"
BASE_ID = "YOUR_BASE"

def save_to_airtable(name, email, phone):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Orders"
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    payload = {"fields": {"name": name, "email": email, "phone": phone}}
    return requests.post(url, json=payload, headers=headers).json()
```

### 3. Бипиум (Российский, 152-ФЗ)

```python
# Сохранение данных в Бипиум (соответствие 152-ФЗ)
import requests
import base64

def save_to_bpium(name, email, phone):
    domain = "your-domain"
    catalog_id = 16
    
    # Авторизация
    auth = base64.b64encode(f"email:password".encode()).decode()
    
    url = f"https://{domain}.bpium.ru/api/v1/catalogs/{catalog_id}/records"
    headers = {"Authorization": f"Basic {auth}"}
    payload = {"values": {"2": name, "3": email, "4": phone}}
    
    return requests.post(url, json=payload, headers=headers).json()
```

---

## 🧪 Тестирование

### Автоматические тесты
```bash
# Проверка webhook
python scripts/test_webhook.py

# Валидация конфигурации
python scripts/validate_config.py

# Генерация отчёта
python scripts/generate_report.py
```

### Ручное тестирование
```
http://localhost:5678/webhook/new-lead?email=test@example.com&name=Денис&phone=+71234567890
```

---

## 🛡️ Безопасность и 152-ФЗ

| Требование | Решение |
|------------|---------|
| Хранение ПДн в РФ | ✅ Бипиум (российский сервис) |
| Шифрование данных | ✅ HTTPS + Base64 авторизация |
| Контроль доступа | ✅ Токены и API-ключи |
| Логирование | ✅ Полный аудит действий |

> ⚠️ **Важно:** Airtable — зарубежный сервис. Используйте Бипиум для хранения персональных данных!

---

## 📈 Масштабирование

### Добавление новых источников
1. Создайте новый Webhook endpoint
2. Добавьте ноду обработки данных
3. Подключите к уведомлениям и хранению

### Интеграция с CRM
```python
# Подключение amoCRM, Bitrix24, amoCRM
def integrate_with_crm(data):
    # Ваша логика интеграции
    pass
```

### Мобильное приложение
- Используйте Webhook как REST API
- Реализуйте JWT-аутентификацию
- Добавьте rate limiting

---

## 📊 Технические характеристики

| Параметр | Значение |
|----------|----------|
| Язык | Python 3.8+ |
| Framework | n8n Workflow |
| Протокол | HTTP/HTTPS |
| Формат данных | JSON |
| Совместимость | n8n Cloud, Self-hosted |

---

## 🤝 Контакты

<div align="center">

| Канал связи | Информация |
|-------------|------------|
| 📱 **Telegram** | [@Tpomoschnik](https://t.me/Tpomoschnik) |
| 📞 **Телефон** | [+7-925-104-10-73](tel:+79251041073) |
| 📧 **Email** | [mamambell@gmail.com](mailto:mamambell@gmail.com) |
| 💻 **GitHub** | [N-888](https://github.com/N-888) |

</div>

---

## 📜 Лицензия

**MIT License** — свободное использование, модификация и распространение

---

<div align="center">

**Сделано с ❤️ для автоматизации бизнес-процессов**

© 2026 N-888 | Все права защищены

</div>

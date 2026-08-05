# Инструкция по настройке - lessonNS04

## Твоё окружение
- **n8n:** Локальный Docker → `http://localhost:5678`
- **Сервер:** Локальный компьютер

---

## Быстрый старт (5 минут)

### Шаг 1: Создай Telegram бота
```
1. Открой Telegram → найди @BotFather
2. Отправь: /newbot
3. Введи имя бота (например: "Мой бот заявок")
4. Введи username (должен заканчиваться на "bot")
5. Сохрани ТОКЕН - он понадобится!
6. Отправь боту любое сообщение
7. Получи Chat ID:
   Браузер → https://api.telegram.org/bot<ТОКЕН>/getUpdates
   Найди "chat":{"id": - это Chat ID
```

### Шаг 2: Импортируй workflow в n8n
```
1. Открой http://localhost:5678
2. Нажми "+" (Create Workflow)
3. Menu (☰) → Import from File
4. Выбери: C:\Users\User\Documents\BIZNES\N8N\lessonNS04\homework-webhook.json
```

### Шаг 3: Настрой Telegram
```
1. Кликни на ноду Telegram
2. Credential → Create New Credential
3. Вставь токен бота → Save
4. Chat ID → вставь свой Chat ID
5. Проверь Expression в поле Text (должно быть зелёное)
```

### Шаг 4: Протестируй
```
1. Нажми "Execute Workflow"
2. Открой браузер → перейди:
   http://localhost:5678/webhook/new-lead?email=test@gmail.com&name=Денис&phone=+71234567890
3. Проверь Telegram - должно прийти сообщение!
```

---

## Настройка Airtable

### Регистрация
```
1. Перейди на https://airtable.com
2. Sign up for Free (через Google или email)
```

### Создание базы
```
1. "+ Create" → "Build an app on your own"
2. Переименуй базу: "CRM"
3. Переименуй таблицу: "Orders"
4. Удали лишние поля (оставь Name)
5. Добавь поля:
   - email (тип: Email)
   - phone (тип: Phone number)
```

### Получение токена
```
1. Значок аккаунта (правый верхний угол)
2. Builder hub → Personal access tokens
3. Create Token
4. Добавь ВСЕ scope и ресурсы
5. Скопируй токен (СОХРАНИ СРАЗУ - потом не покажется!)
```

### Настройка в n8n
```
1. "+" → Airtable → Create a Record
2. Create New Credential → вставь Access Token
3. Base: CRM, Table: Orders
4. Перетащи поля из Webhook:
   - name ← ...query.name
   - email ← ...query.email
   - phone ← ...query.phone
```

---

## Настройка Бипиум (152-ФЗ)

### Регистрация
```
1. Перейди на https://bpium.ru
2. Создать систему
3. Подтверди email, заполни данные
```

### Создание каталога
```
1. "+ Создать каталог" → "Заказы"
2. Добавь поля: Имя, Почта, Телефон
3. Получи ID: шестерёнка → "Задать ID для API"
```

### Настройка HTTP Request в n8n
```
1. "+" → HTTP Request
2. Method: POST
3. URL: https://<поддомен>.bpium.ru/api/v1/catalogs/<ID>/records
4. Headers: Authorization: Basic base64Encode(email:password)
5. Body → JSON:
{
  "values": {
    "2": "{{ $json['query']['name'] }}",
    "3": "{{ $json['query']['email'] }}",
    "4": "{{ $json['query']['phone'] }}"
  }
}
```

---

## Решение проблем

### Webhook не отвечает
```
Проверь: workflow активен? (Active → ON)
Проверь: Docker запущен?
```

### Telegram не приходит
```
Проверь: токен бота правильный?
Проверь: Chat ID правильный?
Проверь: бот не заблокирован?
```

### Airtable не сохраняет
```
Проверь: Access Token правильный?
Проверь: Base и Table называются CRM и Orders?
```

### Бипиум не сохраняет
```
Проверь: email и пароль правильные?
Проверь: ID каталога правильный?
Проверь: JSON синтаксис корректен?
```

---

## Контакты

Если возникли проблемы:
- Telegram: @Tpomoschnik
- Телефон: +7-925-104-10-73
- Email: mamambell@gmail.com

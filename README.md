# AKFADesk

Проект состоит из трех основных компонентов:

1. **Бэкенд (Django)** - REST API для управления данными проекта
2. **Фронтенд (React)** - Веб-интерфейс для пользователей
3. **Телеграм бот** - Бот для доступа к системе через Telegram

## Структура проекта

```
akfadesk_project/
├── backend/           # Django REST API
│   ├── akfadesk/      # Основной проект Django
│   ├── api/           # Django приложение для API
│   ├── venv/          # Виртуальное окружение Python
│   └── requirements.txt
│
├── frontend/          # React приложение
│   ├── public/
│   ├── src/
│   └── package.json
│
└── telegram_bot/      # Telegram бот
    ├── bot.py         # Основной файл бота
    ├── venv/          # Виртуальное окружение Python
    └── requirements.txt
```

## Установка и запуск

### Бэкенд (Django)

1. Перейдите в директорию backend:
```
cd backend
```

2. Активируйте виртуальное окружение:
```
source venv/bin/activate
```

3. Установите зависимости:
```
pip install -r requirements.txt
```

4. Запустите миграции:
```
python manage.py migrate
```

5. Запустите сервер разработки:
```
python manage.py runserver
```

### Фронтенд (React)

1. Перейдите в директорию frontend:
```
cd frontend
```

2. Установите зависимости:
```
npm install
```

3. Запустите сервер разработки:
```
npm start
```

### Телеграм бот

1. Перейдите в директорию telegram_bot:
```
cd telegram_bot
```

2. Активируйте виртуальное окружение:
```
source venv/bin/activate
```

3. Установите зависимости:
```
pip install -r requirements.txt
```

4. Создайте файл .env на основе .env.example и добавьте токен бота:
```
cp .env.example .env
# Отредактируйте файл .env, добавив токен бота
```

5. Запустите бота:
```
python bot.py
``` 
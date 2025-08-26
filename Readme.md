# User Balance API

REST API для управления пользователями и переводами между ними.

## Запуск

```bash
git clone https://github.com/bulat-nitaliev/balance_task.git
cd balance_task
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## API Endpoints

##

- POST /users - Создание пользователя

- GET /users - Получение списка пользователей

- POST /transfer - Перевод между пользователями

- GET /health - Проверка здоровья приложения

## Примеры запросов

### Создание пользователя

```
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com", "balance": 1000.0}'
```

### Получение пользователей

```
curl "http://localhost:8000/users"
```

### Перевод

```
curl -X POST "http://localhost:8000/transfer" \
     -H "Content-Type: application/json" \
     -d '{"from_user_id": "uuid-here", "to_user_id": "uuid-here", "amount": 100.0}'
```

## Ключевые особенности решения:

1. **Чистая архитектура** - разделение на модели, сервисы, схемы и исключения
2. **Валидация данных** - использование Pydantic для валидации входных данных
3. **Обработка ошибок** - кастомные исключения с понятными сообщениями
4. **Типизация** - строгая типизация для предотвращения ошибок
5. **Документация** - автоматическая генерация OpenAPI документации
6. **Тестовые данные** - in-memory хранилище для демонстрации

Это решение демонстрирует понимание лучших практик FastAPI, работу с исключениями, валидацию данных и чистую архитектуру приложения.

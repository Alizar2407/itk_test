# ITK Academy - тестовое задание

По заданию нужно было реализовать REST API, которое принимает 2 запроса:

### 1. Получить баланс кошелька

`GET /wallets/{wallet_id}`

**Пример ответа:**
```json
{
  "wallet_id": "550e8400-e29b-41d4-a716-446655440000",
  "balance": 100
}
```

### 2. Выполнить операцию с кошельком

`POST /wallets/{wallet_id}/operate`
```json
{
  "operation_type": "DEPOSIT",   // или "WITHDRAW"
  "amount": 50
}
```

**Пример ответа:**
```json
{
  "wallet_id": "550e8400-e29b-41d4-a716-446655440000",
  "balance": 150
}
```

# Реализация

Был выбран следующий стек:
- **FastAPI** - REST API
- **PostgreSQL** - в качестве БД
- **Alembic** - для миграций
- **Docker-compose** - развертывание приложения

Для запуска достаточно склонировать репозиторий и выполнить команду `docker-compose up`:
```shell
git clone https://github.com/Alizar2407/itk_test
cd itk_test
docker-compose up --build
```

Приложение будет доступно по адресу *http://localhost:8000/docs*

Тесты можно выполнить с помощью следующей команды:
```shell
docker-compose up --build tests
```

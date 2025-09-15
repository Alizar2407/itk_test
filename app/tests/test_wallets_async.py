import pytest
import asyncio

import uuid
import httpx
import requests


BASE_URL = "http://app:8000/api/v1/wallets"


@pytest.mark.asyncio
async def test_async_deposits():
    wallet_id = uuid.uuid4()
    deposit_amount = 100
    num_requests = 10

    # Создаем кошелек с нулевым балансом
    resp = requests.post(
        f"{BASE_URL}/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 0},
    )
    assert resp.status_code == 200

    async def deposit():
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{BASE_URL}/{wallet_id}/operation",
                json={"operation_type": "DEPOSIT", "amount": deposit_amount},
            )
            assert r.status_code == 200

    # Параллельно выполняем несколько запросов типа DEPOSIT
    await asyncio.gather(*[deposit() for _ in range(num_requests)])
    resp = requests.get(f"{BASE_URL}/{wallet_id}")

    assert resp.status_code == 200
    assert resp.json()["balance"] == deposit_amount * num_requests

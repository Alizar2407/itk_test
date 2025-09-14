import uuid
import requests

BASE_URL = "http://app:8000/api/v1/wallets"


def test_deposit_and_get_wallet():
    wallet_id = uuid.uuid4()

    # Создаем кошелек с балансом 1000
    resp = requests.post(
        f"{BASE_URL}/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000},
    )
    assert resp.status_code == 200

    data = resp.json()
    assert data["wallet_id"] == str(wallet_id)
    assert data["balance"] == 1000

    # Получаем баланс кошелька
    resp = requests.get(f"{BASE_URL}/{wallet_id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["balance"] == 1000


def test_withdraw_and_insufficient_funds():
    wallet_id = uuid.uuid4()

    # Создаем кошелек с балансом 500
    resp = requests.post(
        f"{BASE_URL}/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 500},
    )
    assert resp.status_code == 200

    # Списываем 300 — должно остаться 200
    resp = requests.post(
        f"{BASE_URL}/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 300},
    )
    assert resp.status_code == 200
    assert resp.json()["balance"] == 200

    # Пытаемся списать еще 500
    resp = requests.post(
        f"{BASE_URL}/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 500},
    )
    assert resp.status_code == 400
    assert "Недостаточно средств" in resp.json()["detail"]

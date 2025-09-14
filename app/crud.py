from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Wallet
from app.schemas import OperationType


class InsufficientFunds(Exception):
    pass


async def get_wallet(session: AsyncSession, wallet_id: UUID) -> Wallet | None:
    statement = select(Wallet).where(Wallet.id == wallet_id)
    result = await session.execute(statement)

    return result.scalar_one_or_none()


async def create_wallet(session: AsyncSession, wallet_id: UUID) -> Wallet:
    new_wallet = Wallet(id=wallet_id, balance=0)
    session.add(new_wallet)

    await session.flush()
    return new_wallet


async def apply_operation(
    session: AsyncSession,
    wallet_id: UUID,
    op_type: OperationType,
    amount: int,
) -> int:

    # блокируем строку с помощью `select ... for update`
    statement = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
    result = await session.execute(statement)
    wallet = result.scalar_one_or_none()

    # если кошелька с указанным UUDI не существует, создаем новый
    if wallet is None:
        wallet = Wallet(id=wallet_id, balance=0)
        session.add(wallet)
        await session.flush()

    if op_type == OperationType.DEPOSIT:
        wallet.balance += amount

    elif op_type == OperationType.WITHDRAW:
        if wallet.balance < amount:
            raise InsufficientFunds(
                "Недостаточно средств для выполнения операции списания"
            )
        wallet.balance = wallet.balance - amount

    else:
        raise ValueError("Неизвестная операция")

    await session.flush()
    return wallet.balance

from uuid import UUID

from fastapi import FastAPI, Depends, status, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.db import get_session


app = FastAPI(title="Тестовое задание ITK Academy")


@app.post(
    "/api/v1/wallets/{wallet_id}/operation",
    response_model=schemas.WalletResponse,
    status_code=status.HTTP_200_OK,
)
async def wallet_operation(
    wallet_id: UUID = Path(..., description="Wallet UUID"),
    req: schemas.OperationRequest = None,
    session: AsyncSession = Depends(get_session),
):
    try:
        async with session.begin():
            new_balance = await crud.apply_operation(
                session, wallet_id, req.operation_type, req.amount
            )
    except crud.InsufficientFunds as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Неизвестная ошибка: {str(e)}")

    return schemas.WalletResponse(wallet_id=wallet_id, balance=new_balance)


@app.get(
    "/api/v1/wallets/{wallet_id}",
    response_model=schemas.WalletResponse,
    status_code=status.HTTP_200_OK,
)
async def get_wallet(
    wallet_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    wallet = await crud.get_wallet(session, wallet_id)
    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Кошелек с указанным UUID не найден",
        )
    return schemas.WalletResponse(wallet_id=wallet.id, balance=wallet.balance)

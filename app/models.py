import uuid
from sqlalchemy import BigInteger, MetaData, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData()


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    balance: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0,
    )

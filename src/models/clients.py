# SqlAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, Boolean

# Local
from .base import Base


class Clients(Base):
    """Model for clients and their agrees."""

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    wa_number: Mapped[str] = mapped_column(String, index=True)
    wa_id: Mapped[str] = mapped_column(String, index=True)
    confirm: Mapped[bool] = mapped_column(Boolean, default=False)

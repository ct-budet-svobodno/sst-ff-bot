from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .engine import Base


class Activist(Base):
    __tablename__ = 'activists'
    
    name: Mapped[str] = mapped_column(String)
    birthday: Mapped[str] = mapped_column(String)
    student_group: Mapped[str] = mapped_column(String)
    number: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    studak: Mapped[str] = mapped_column(String)
    basis_of_study: Mapped[str] = mapped_column(String)
    others: Mapped[str] = mapped_column(String)
    membership_period: Mapped[str] = mapped_column(String)
    station: Mapped[str | None] = mapped_column(String, default=None)
    telegram_id: Mapped[str] = mapped_column(String, primary_key=True)
    status: Mapped[str] = mapped_column(String)
    score: Mapped[int] = mapped_column(Integer)
    ach_kos: Mapped[str | None] = mapped_column(String, default=None)
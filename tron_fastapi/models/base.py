from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    """
    Base class for all models.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

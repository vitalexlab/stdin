from typing import List
from sqlalchemy import create_engine, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

db_name = 'orders.db'
connection = f'sqlite:///{db_name}'

engine = create_engine(connection, echo=True)

Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders_order'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    sign_at: Mapped[DateTime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(100), nullable=False, default='draft')
    project_id: Mapped[int] = mapped_column(ForeignKey('orders_project.id'))
    project: Mapped["Project"] = relationship(back_populates="order_links")

    def __repr__(self) -> str:
        return f"Order(id={self.id!r},name={self.name!r}),date={self.created_at!r}"


class Project(Base):

    __tablename__ = 'orders_project'
    """Описывает сущность Проект"""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    order_links: Mapped[List["Order"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Project(id={self.id!r},name={self.name!r}),date={self.created_at!r}"


Base.metadata.create_all(engine)

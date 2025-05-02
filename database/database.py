import asyncio

from sqlalchemy import False_, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import DB_URL


class Model(DeclarativeBase):
    pass


class DrawsOrm(Model):
    __tablename__ = 'draws'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    winners_count: Mapped[int]
    is_end: Mapped[bool] = mapped_column(server_default='false') #  Я использую postgres. Если у вас другая СУБД, то аргумент - default=False

class UsersDrawOrm(Model):
    __tablename__ = 'users_draw'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]
    draw_id: Mapped[int] = mapped_column(ForeignKey('draws.id'))
    is_winner: Mapped[bool] = mapped_column(server_default='false')


class UsersOrm(Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    chat_id: Mapped[int]


engine = create_async_engine(DB_URL)
session_factory = async_sessionmaker(engine, expire_on_commit=False)
new_session = session_factory()
# Создание таблиц. Убрать комментарий
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.create_all)
#
# asyncio.run(create_tables())

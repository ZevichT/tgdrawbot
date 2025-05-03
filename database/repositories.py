from sqlalchemy import select, update

from .database import DrawsOrm, new_session, UsersDrawOrm, UsersOrm


class DrawsRepository:
    @classmethod
    async def get_draws(cls) -> list:
        async with new_session as session:
            query = select(DrawsOrm.name).where(DrawsOrm.is_end == False)
            response = await session.execute(query)
            draws = response.scalars().all()
            return draws


    @classmethod
    async def add_draw(cls, name: str, winners: int) -> None | str:
        async with new_session as session:
            query = select(DrawsOrm.name).where(DrawsOrm.name == name)
            response = await session.execute(query)
            check_duplicate = response.scalar_one_or_none()
            if check_duplicate is None:
                draw_dict = {'name': name, 'winners_count': winners}
                draw = DrawsOrm(**draw_dict)
                session.add(draw)
                await session.commit()
                await session.close()
            else:
                return 'Error'


    @classmethod
    async def get_id(cls, name: str) -> int | str:
        async with new_session as session:
            query = select(DrawsOrm.id).where(DrawsOrm.name == name)
            response = await session.execute(query)
            draw_id = response.scalar_one_or_none()
            if draw_id is None:
                draw_id = 'Error'
            return draw_id


    @classmethod
    async def get_max_winners(cls, draw_id: int) -> int | str:
        async with new_session as session:
            query = select(DrawsOrm.winners_count).where(DrawsOrm.id == draw_id)
            response = await session.execute(query)
            winners_count = response.scalar_one_or_none()
            if winners_count is None:
                return 'Error'
            return winners_count


    @classmethod
    async def end_draw(cls, draw_id: int) -> None:
        async with new_session as session:
            query = update(DrawsOrm).where(DrawsOrm.id == draw_id).values(is_end=True)
            await session.execute(query)
            await session.commit()
            await session.close()

class UsersDrawRepository:
    @classmethod
    async def check_participation(cls, user_id: str, draw_id: int) -> bool:
        async with new_session as session:
            query = select(UsersDrawOrm).where((UsersDrawOrm.user_id == user_id) & (UsersDrawOrm.draw_id == draw_id))
            response = await session.execute(query)
            participation = response.scalar_one_or_none()
            if participation is None:
                return False
            return True

    @classmethod
    async def add_participant(cls, user_id: str, draw_id: int) -> None:
        async with new_session as session:
            participant_dict = {'user_id': f'@{user_id}', 'draw_id': draw_id}
            participant = UsersDrawOrm(**participant_dict)
            session.add(participant)
            await session.commit()
            await session.close()


    @classmethod
    async def get_users_id(cls, draw_id: int) -> list:
        async with new_session as session:
            query = select(UsersDrawOrm.user_id).where(UsersDrawOrm.draw_id == draw_id)
            response = await session.execute(query)
            users = response.scalars().all()
            return users


    @classmethod
    async def set_winner(cls, user_id, draw_id) -> None:
        async with (new_session as session):
            query = update(UsersDrawOrm).where((UsersDrawOrm.user_id == user_id) & (UsersDrawOrm.draw_id == draw_id)
                                               ).values(is_winner=True)
            await session.execute(query)
            await session.commit()
            await session.close()


class UsersRepository:
    @classmethod
    async def add_user(cls, user_id: int, chat_id: int) -> None:
        async with new_session as session:
            query = select(UsersOrm.user_id).where(UsersOrm.user_id == user_id)
            response = await session.execute(query)
            check_duplicate = response.scalar_one_or_none()
            if check_duplicate is None:
                user_dict = {'user_id': user_id, 'chat_id': chat_id}
                user = UsersOrm(**user_dict)
                session.add(user)
                await session.commit()
                await session.close()
            else:
                return None


    @classmethod
    async def get_users_chat_id(cls) -> list:
        async with new_session as session:
            query = select(UsersOrm.chat_id)
            response = await session.execute(query)
            chats_ids = response.scalars().all()
            return chats_ids

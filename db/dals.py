from typing import Optional

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class UserDAL:
    """Data Access Layer(DAL) for operating user info"""

    def __init__(self, db_session: AsyncSession) -> None:
        # Initializing database session
        self.db_session = db_session

    async def create_user(self, name: str, surname: str, email: str) -> User:
        """Method for creating new user"""
        # User parameters
        new_user = User(
            name=name,
            surname=surname,
            email=email,
        )
        # Adding user info to db
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Optional[UUID]:
        """Method for deleting existing user"""
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
        ).returning(User.user_id)
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id, **kwargs) -> Optional[UUID]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

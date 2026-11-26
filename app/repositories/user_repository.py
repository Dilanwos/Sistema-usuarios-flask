"""Repositorio de acceso a datos de usuarios."""

import uuid

from sqlalchemy import or_, select

from app.extensions import db
from app.models.user import User


class UserRepository:
    """Gestiona las operaciones de persistencia de usuarios."""

    @staticmethod
    def get_by_id(
        user_id: uuid.UUID,
        include_deleted: bool = False,
    ) -> User | None:
        """Obtiene un usuario mediante su identificador."""

        statement = select(User).where(User.id == user_id)

        if not include_deleted:
            statement = statement.where(User.deleted_at.is_(None))

        return db.session.scalar(statement)

    @staticmethod
    def get_by_username(
        username: str,
        include_deleted: bool = False,
    ) -> User | None:
        """Busca un usuario mediante su nombre de usuario."""

        statement = select(User).where(User.username == username)

        if not include_deleted:
            statement = statement.where(User.deleted_at.is_(None))

        return db.session.scalar(statement)

    @staticmethod
    def get_by_email(
        email: str,
        include_deleted: bool = False,
    ) -> User | None:
        """Busca un usuario mediante su correo electrónico."""

        statement = select(User).where(User.email == email)

        if not include_deleted:
            statement = statement.where(User.deleted_at.is_(None))

        return db.session.scalar(statement)

    @staticmethod
    def get_by_identifier(identifier: str) -> User | None:
        """Busca un usuario mediante username o correo electrónico."""

        statement = select(User).where(
            or_(
                User.username == identifier,
                User.email == identifier,
            ),
            User.deleted_at.is_(None),
        )

        return db.session.scalar(statement)

    @staticmethod
    def username_exists(username: str) -> bool:
        """Comprueba si un nombre de usuario ya está reservado."""

        statement = select(User.id).where(User.username == username)

        return db.session.scalar(statement) is not None

    @staticmethod
    def email_exists(email: str) -> bool:
        """Comprueba si un correo electrónico ya está reservado."""

        statement = select(User.id).where(User.email == email)

        return db.session.scalar(statement) is not None

    @staticmethod
    def add(user: User) -> User:
        """Agrega un usuario a la sesión actual."""

        db.session.add(user)

        return user

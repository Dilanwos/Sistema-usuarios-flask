"""Servicios de autenticación y registro de usuarios."""

from email_validator import EmailNotValidError, validate_email
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.enums import UserStatus
from app.models.user import User
from app.models.user_profile import UserProfile
from app.repositories.user_profile_repository import UserProfileRepository
from app.repositories.user_repository import UserRepository


class AuthenticationError(Exception):
    """Error base del módulo de autenticación."""


class DuplicateUserError(AuthenticationError):
    """El username o correo electrónico ya está registrado."""


class InvalidCredentialsError(AuthenticationError):
    """Las credenciales proporcionadas no son válidas."""


class AccountNotActiveError(AuthenticationError):
    """La cuenta no está habilitada para autenticarse."""


class UserRegistrationError(AuthenticationError):
    """No fue posible completar el registro del usuario."""


class RegistrationValidationError(AuthenticationError):
    """Los datos proporcionados para el registro no son válidos."""


def register_user(
    username: str,
    email: str,
    password: str,
) -> User:
    """Registra un usuario y crea su perfil en una transacción."""

    # ================================================
    # VALIDACIÓN DE TIPOS
    # ================================================

    if not all(
        isinstance(value, str)
        for value in (username, email, password)
    ):
        raise RegistrationValidationError(
            "Todos los campos deben contener texto válido."
        )

    # ================================================
    # NORMALIZACIÓN DE DATOS
    # ================================================

    normalized_username = username.strip().lower()
    normalized_email = email.strip().lower()

    # ================================================
    # VALIDACIÓN DE LONGITUDES
    # ================================================

    if not 3 <= len(normalized_username) <= 50:
        raise RegistrationValidationError(
            "El nombre de usuario debe tener entre 3 y 50 caracteres."
        )

    if not normalized_email or len(normalized_email) > 255:
        raise RegistrationValidationError(
            "El correo electrónico debe tener un máximo de 255 caracteres."
        )

    if not 12 <= len(password) <= 128:
        raise RegistrationValidationError(
            "La contraseña debe tener entre 12 y 128 caracteres."
        )

    # ================================================
    # VALIDACIÓN DEL CORREO ELECTRÓNICO
    # ================================================

    try:
        email_result = validate_email(
            normalized_email,
            check_deliverability=False,
        )

        normalized_email = email_result.normalized.lower()

    except EmailNotValidError as error:
        raise RegistrationValidationError(
            "El correo electrónico no tiene un formato válido."
        ) from error

    if len(normalized_email) > 255:
        raise RegistrationValidationError(
            "El correo electrónico supera la longitud permitida."
        )

    # ================================================
    # REGISTRO DEL USUARIO
    # ================================================

    try:
        if UserRepository.username_exists(normalized_username):
            raise DuplicateUserError(
                "El nombre de usuario ya está registrado."
            )

        if UserRepository.email_exists(normalized_email):
            raise DuplicateUserError(
                "El correo electrónico ya está registrado."
            )

        user = User(
            username=normalized_username,
            email=normalized_email,
            password_hash=generate_password_hash(password),
            status=UserStatus.PENDING_VERIFICATION.value,
            is_email_verified=False,
        )

        # Crear el perfil asociado al usuario.
        profile = UserProfile(user=user)

        UserRepository.add(user)
        UserProfileRepository.add(profile)

        # Confirmar ambas operaciones en una transacción.
        db.session.commit()

    # ================================================
    # MANEJO DE EXCEPCIONES
    # ================================================

    except DuplicateUserError:
        db.session.rollback()
        raise

    except IntegrityError as error:
        db.session.rollback()

        original_error = getattr(error, "orig", None)
        diagnostic = getattr(original_error, "diag", None)
        constraint_name = getattr(diagnostic, "constraint_name", None)

        if constraint_name in {
            "users_username_key",
            "users_email_key",
        }:
            raise DuplicateUserError(
                "El nombre de usuario o correo electrónico ya está registrado."
            ) from error

        raise UserRegistrationError(
            "Se produjo un conflicto al guardar el registro."
        ) from error

    except SQLAlchemyError as error:
        db.session.rollback()

        raise UserRegistrationError(
            "No fue posible guardar el registro."
        ) from error

    return user

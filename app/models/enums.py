from enum import Enum


class UserStatus(str, Enum):
    """Estados posibles de una cuenta de usuario."""

    PENDING_VERIFICATION = "pending_verification"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DISABLED = "disabled"


class NotificationType(str, Enum):
    """Tipos de notificaciones del sistema."""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    SECURITY = "security"


class SecurityEventType(str, Enum):
    """Eventos relevantes para la seguridad."""

    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    PASSWORD_CHANGED = "password_changed"
    PASSWORD_RESET = "password_reset"
    EMAIL_VERIFIED = "email_verified"
    ACCOUNT_SUSPENDED = "account_suspended"
    SESSION_REVOKED = "session_revoked"

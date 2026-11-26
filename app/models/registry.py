"""Registro centralizado de los modelos de la aplicación."""

# ─────────────────────────────────────────────
# MODELOS DE IDENTIDAD Y USUARIOS
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# MODELOS DE AUDITORÍA Y NOTIFICACIONES
# ─────────────────────────────────────────────
from app.models.audit_log import AuditLog

# ─────────────────────────────────────────────
# MODELOS DE AUTENTICACIÓN Y SEGURIDAD
# ─────────────────────────────────────────────
from app.models.email_verification_token import EmailVerificationToken
from app.models.notification import Notification
from app.models.password_reset_token import PasswordResetToken
from app.models.permission import Permission

# ─────────────────────────────────────────────
# MODELOS DE ROLES Y PERMISOS
# ─────────────────────────────────────────────
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.security_event import SecurityEvent
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.user_role import UserRole
from app.models.user_session import UserSession

# ─────────────────────────────────────────────
# EXPORTACIONES PÚBLICAS
# ─────────────────────────────────────────────

__all__ = [
    "AuditLog",
    "EmailVerificationToken",
    "Notification",
    "PasswordResetToken",
    "Permission",
    "Role",
    "RolePermission",
    "SecurityEvent",
    "User",
    "UserProfile",
    "UserRole",
    "UserSession",
]

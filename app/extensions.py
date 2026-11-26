from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from app.models.base import Base

# Base de datos con SQLAlchemy 2.x
db = SQLAlchemy(model_class=Base)

# Migraciones con Alembic
migrate = Migrate()

# Autenticación y sesiones
login_manager = LoginManager()

# Protección CSRF
csrf = CSRFProtect()

# Limitación de solicitudes
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri="memory://",
)

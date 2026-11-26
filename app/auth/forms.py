"""Formularios del módulo de autenticación."""

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)

# ================================================
# FORMULARIO DE INICIO DE SESIÓN
# ================================================

class LoginForm(FlaskForm):
    identifier = StringField(
        "Usuario o correo electrónico",
        validators=[
            DataRequired(message="Este campo es obligatorio."),
            Length(max=255),
        ],
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
        ],
    )

    remember = BooleanField("Recordarme")

    submit = SubmitField("Iniciar sesión")


# ================================================
# FORMULARIO DE REGISTRO
# ================================================

class RegistrationForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(message="El nombre de usuario es obligatorio."),
            Length(
                min=3,
                max=50,
                message="Debe contener entre 3 y 50 caracteres.",
            ),
        ],
    )

    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo electrónico es obligatorio."),
            Email(message="Introduce un correo electrónico válido."),
            Length(max=255),
        ],
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(
                min=12,
                max=128,
                message="La contraseña debe tener entre 12 y 128 caracteres.",
            ),
        ],
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Debes confirmar tu contraseña."),
            EqualTo(
                "password",
                message="Las contraseñas no coinciden.",
            ),
        ],
    )

    submit = SubmitField("Crear cuenta")

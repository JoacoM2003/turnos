from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar la app
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Importar la configuración de la app
from app.core.config import settings

# Importar Base y todos los modelos
from app.infrastructure.db.base import Base

# IMPORTANTE: Importar TODOS los modelos para que Alembic los detecte
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.models.cliente_model import ClienteModel
from app.infrastructure.db.models.proveedor_model import ProveedorModel
from app.infrastructure.db.models.servicio_model import ServicioModel
from app.infrastructure.db.models.recurso_model import RecursoModel
from app.infrastructure.db.models.horario_model import HorarioModel
from app.infrastructure.db.models.horario_disponible_model import HorarioDisponibleModel
from app.infrastructure.db.models.reserva_model import ReservaModel
from app.infrastructure.db.models.bloqueo_model import BloqueoModel
from app.infrastructure.db.models.bloqueo_recurso_model import BloqueoRecursoModel

# this is the Alembic Config object
config = context.config

# Configurar la URL de la base de datos desde settings
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Detectar cambios en tipos de columnas
        compare_server_default=True,  # Detectar cambios en valores default
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
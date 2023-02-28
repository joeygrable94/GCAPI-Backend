from logging.config import fileConfig
from os import environ, path
import sys

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# Load the current location into the env path
alembic_env_file = __file__.split('/')
alem_last_i = alembic_env_file.index('alembic')
alembic_base_dir = '/'.join(alembic_env_file[0:alem_last_i])
sys.path.append(alembic_base_dir)

# Load the dotenv to use in alembic
try:
    load_dotenv(path.join(alembic_base_dir, ".env"))
except Exception as err:
    print('Alembic Error:', err)

# database uri
def get_url() -> str:
    dburi: str = environ.get("DATABASE_URI", "sqlite:///./app.db")
    return dburi

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
from app.db.base import Base  # noqa: E402
target_metadata = Base.metadata

# set DB URI
config.set_main_option("sqlalchemy.url", get_url())


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = get_url()
    configuration = config.get_section(config.config_ini_section)
    configuration["url"] = url  # type: ignore
    connectable = context.config.attributes.get("connection", None)
    
    if connectable is None:
        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

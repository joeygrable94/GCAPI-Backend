# Security

## Generate Secrets

`openssl rand -hex 32`

## Alembic for DB Migrations

`alembic init app/db/migrations`

    <!-- alembic.ini -->
    [alembic]
    script_location = app/db/migrations

`docker-compose run backend alembic revision --autogenerate`

`docker-compose run backend alembic upgrade head`

## SQLAlchemy ORM

- [SQLAlchemy Relationship Loading Techniques](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html)

## Testing

- [PyTest Raising Exceptions](https://docs.pytest.org/en/6.2.x/assert.html)

# Security

## Generate Secrets

`openssl rand -hex 32`

---

## Alembic for DB Migrations

### Alembic Configuration

First, run the alembic init command and specify where the migrations are to be stored.

    alembic init app/db/migrations

Next edit the `alembic.ini` file to the location of the initialized alembic directory

    [alembic]
    script_location = app/db/migrations

Last, edit the `env.py` file in the migrations directory to include your config and db base to migrate.

### Alembic Commands

Check current db version.

`docker-compose run backend alembic current`

After changing db models/tables, run revision, and autogenerate.
Always add a message about what changed in the db models/tables.

`docker-compose run backend alembic revision --autogenerate -m "added table ____"`

Upgrading db to the latest revision version.

`docker-compose run backend alembic upgrade head`

Upgrade db up 1 version.

`docker-compose run backend alembic upgrade +1`

Downgrade db up 1 version.

`docker-compose run backend alembic downgrade -1`

Downgrade db to the earliest version.

`docker-compose run backend alembic downgrade base`


## Alembic Resources

- [FastAPI, SQL, and Alembic](https://ahmed-nafies.medium.com/fastapi-with-sqlalchemy-postgresql-and-alembic-and-of-course-docker-f2b7411ee396)

---

## SQLAlchemy ORM

- [SQLAlchemy Relationship Loading Techniques](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html)

## Testing

- [PyTest Raising Exceptions](https://docs.pytest.org/en/6.2.x/assert.html)

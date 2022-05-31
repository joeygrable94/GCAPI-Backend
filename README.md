
openssl rand -hex 32


# Alembic
Alembic init app/db/migrations

<!-- alembic.ini -->
[alembic]
script_location = app/db/migrations


docker-compose run backend alembic revision --autogenerate
docker-compose run backend alembic upgrade head


See SQLAlchemy Relationship Loading Techniques:
- https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html

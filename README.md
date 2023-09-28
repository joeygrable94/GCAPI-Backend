# GCAPI Backend

[![CodeQL](https://github.com/joeygrable94/GCAPI-Backend/actions/workflows/codeql.yml/badge.svg)](https://github.com/joeygrable94/GCAPI-Backend/actions/workflows/codeql.yml) [![GitHub CI](https://github.com/joeygrable94/GCAPI-Backend/actions/workflows/ci.yml/badge.svg)](https://github.com/joeygrable94/GCAPI-Backend/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/joeygrable94/GCAPI-Backend/branch/main/graph/badge.svg?token=8FCB50574D)](https://codecov.io/gh/joeygrable94/GCAPI-Backend)

- [GCAPI Backend](#gcapi-backend)
  - [Getting Started](#getting-started)
  - [FastAPI](#fastapi)
    - [FastAPI Resources](#fastapi-resources)
  - [Alembic](#alembic)
    - [Configuration](#configuration)
    - [Commands](#commands)
  - [Hashing and Encrypting Data](#hashing-and-encrypting-data)
    - [Resources](#resources)
  - [SQLAlchemy ORM](#sqlalchemy-orm)
    - [SQLAlchemy Resources](#sqlalchemy-resources)
  - [PyTest](#pytest)
    - [PyTest Commands](#pytest-commands)
    - [PyTest Resources](#pytest-resources)

---

## Getting Started

First check to ensure Python 3.11 is installed and is the current version in use.

    python3 --version
    > python3.11

Create a virtual environment, activate it, then install the backend python pip `requirements.dev.txt` file.

    python3.11 -m venv venv
    source venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install poetry
    poetry install
    uvicorn app.main:app --host 0.0.0.0 --port 8888 --log-level info --reload
    > ... App Running at 0.0.0.0:8888
    > :q
    source venv/bin/deactivate

## FastAPI

### FastAPI Resources

- [FastAPI Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)

## Alembic

### Configuration

First, run the alembic init command and specify where the migrations are to be stored.

    alembic init alembic

Next edit the `alembic.ini` file to the location of the initialized alembic directory

    [alembic]
    script_location = alembic

Last, edit the `env.py` file in the migrations directory to include your config and db base to migrate.

### Commands

Check current db version.

    alembic current

After changing db models/tables, run revision, and autogenerate.
Always add a message about what changed in the db models/tables.

    alembic revision --autogenerate -m "added table ____"
    alembic upgrade head
    alembic upgrade +1
    alembic downgrade -1
    alembic downgrade base

## Hashing and Encrypting Data

- [Password Encryption in Python: Securing Your Data](https://pagorun.medium.com/password-encryption-in-python-securing-your-data-9e0045e039e1)
- [Asymmetric Encryption and Decryption in Python](https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/)
- [Asymmetric Cryptography with Python](https://medium.com/@ashiqgiga07/asymmetric-cryptography-with-python-5eed86772731)
- [Exploring approaches to field-level encryption in Python for Django applications](https://www.piiano.com/blog/field-level-encryption-in-python-for-django-applications)
- [Example RSA_example.py](https://gist.github.com/syedrakib/241b68f5aeaefd7ef8e2)
- [Example rsa.py](https://gist.github.com/edmhs/6afc542af8a20a619946c2c3b36df8f4)

### Resources

- [FastAPI, SQL, and Alembic](https://ahmed-nafies.medium.com/fastapi-with-sqlalchemy-postgresql-and-alembic-and-of-course-docker-f2b7411ee396)

---

## SQLAlchemy ORM

### SQLAlchemy Resources

- [SQLAlchemy Relationship Loading Techniques](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html)

---

## PyTest

### PyTest Commands

    pytest
    pytest tests/crud
    pytest tests/api/api_v1/test_websites.py

### PyTest Resources

- [FastAPI PyTest Coverage WalkThrough](https://www.azepug.az/posts/fastapi/ecommerce-fastapi-nuxtjs/ecommerce-pytest-user-auth-part1.html)
- [PyTest Raising Exceptions](https://docs.pytest.org/en/6.2.x/assert.html)

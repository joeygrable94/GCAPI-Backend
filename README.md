# GCAPI Backend

[![CodeQL](https://github.com/joeygrable94/GCAPI-Backend/actions/workflows/codeql.yml/badge.svg)](https://github.com/joeygrable94/GCAPI-Backend/actions/workflows/codeql.yml) [![GitHub CI](https://github.com/joeygrable94/GCAPI-Backend/actions/workflows/ci.yml/badge.svg)](https://github.com/joeygrable94/GCAPI-Backend/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/joeygrable94/GCAPI-Backend/branch/main/graph/badge.svg?token=8FCB50574D)](https://codecov.io/gh/joeygrable94/GCAPI-Backend)

- [GCAPI Backend](#gcapi-backend)
  - [Getting Started](#getting-started)
  - [Application Structure](#application-structure)
  - [Security Resources](#security-resources)
    - [Hashing and Encrypting Data](#hashing-and-encrypting-data)
    - [Session Management](#session-management)
  - [FastAPI Resources](#fastapi-resources)
  - [Alembic](#alembic)
    - [Configuration](#configuration)
    - [Commands](#commands)
  - [SQLAlchemy ORM](#sqlalchemy-orm)
    - [Pagination](#pagination)
  - [PyTest](#pytest)
    - [PyTest Commands](#pytest-commands)
    - [PyTest Resources](#pytest-resources)
  - [External Resources](#external-resources)
  - [Useful Commands](#useful-commands)

---

## Getting Started

First check to ensure Python 3.12 is installed and is the current version in use.

```bash
python3 --version
> python3.12
```

Create a virtual environment, activate it, then install the backend python pip `requirements.dev.txt` file.

```bash
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install poetry
poetry install
uvicorn app.main:app --host 0.0.0.0 --port 8888 --log-level info --reload
> ... App Running at 0.0.0.0:8888
> :q
source venv/bin/deactivate
```

---

## Application Structure

- [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file#project-structure)

---

## Security Resources

### Hashing and Encrypting Data

Examples:

- [Password Encryption in Python: Securing Your Data](https://pagorun.medium.com/password-encryption-in-python-securing-your-data-9e0045e039e1)
- [Asymmetric Encryption and Decryption in Python](https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/)
- [Asymmetric Cryptography with Python](https://medium.com/@ashiqgiga07/asymmetric-cryptography-with-python-5eed86772731)
- [Exploring approaches to field-level encryption in Python for Django applications](https://www.piiano.com/blog/field-level-encryption-in-python-for-django-applications)
- [Example RSA_example.py](https://gist.github.com/syedrakib/241b68f5aeaefd7ef8e2)
- [Example rsa.py](https://gist.github.com/edmhs/6afc542af8a20a619946c2c3b36df8f4)
- [Advanced Encryption Standard (AES) Methods](https://onboardbase.com/blog/aes-encryption-decryption/)
- [A Guide to Advanced Encryption Standard (AES)](https://medium.com/quick-code/understanding-the-advanced-encryption-standard-7d7884277e7)

### Session Management

- [Starlette Session Middleware](https://www.appsloveworld.com//python/1357/fastapi-starlettes-sessionmiddleware-creates-new-session-for-every-request)

---

## FastAPI Resources

- [FastAPI, SQL, and Alembic](https://ahmed-nafies.medium.com/fastapi-with-sqlalchemy-postgresql-and-alembic-and-of-course-docker-f2b7411ee396)
- [FastAPI Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)

---

## Alembic

### Configuration

First, run the alembic init command and specify where the migrations are to be stored.

```bash
alembic init alembic
```

Next edit the `alembic.ini` file to the location of the initialized alembic directory

```ini
[alembic]
script_location = alembic
```

Last, edit the `env.py` file in the migrations directory to include your config and db base to migrate.

### Commands

Check current db version.

```bash
alembic current
```

After changing db models/tables, run revision, and autogenerate.
Always add a message about what changed in the db models/tables.

```bash
alembic revision --autogenerate -m "added table ____"
alembic upgrade head
alembic upgrade +1
alembic downgrade -1
alembic downgrade base
```

---

## SQLAlchemy ORM

- [SQLAlchemy Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)
- [Asynchronous I/O (asyncio)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

### Pagination

- [Basic FastAPI-SQLAlchemy Pagination](https://github.com/jayhawk24/pagination-fastapi/tree/main)
- [Asyncio Support Pagination Example](https://github.com/dialoguemd/fastapi-sqla/blob/master/fastapi_sqla/asyncio_support.py)

---

## PyTest

### PyTest Commands

```bash
pytest
pytest tests/crud
pytest tests/api/api_v1/test_websites.py
```

### PyTest Resources

- [FastAPI PyTest Coverage WalkThrough](https://www.azepug.az/posts/fastapi/ecommerce-fastapi-nuxtjs/ecommerce-pytest-user-auth-part1.html)
- [PyTest Raising Exceptions](https://docs.pytest.org/en/6.2.x/assert.html)

---

## External Resources

- [IPInfo.io](https://ipinfo.io/)

---

## Useful Commands

Delete DS_Store files

```bash
find . -name '.DS_Store' -type f -delete
```

Delete all python cache files

```bash
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
```

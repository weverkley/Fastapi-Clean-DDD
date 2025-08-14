## Run fastapi
```bash
fastapi run main.py
```

```bash
uvicorn main:app --reload --no-server-header
```

## Clean local and cached files
```bash
py3clean .
```

## Generate CRUD Code
```bash
cookiecutter crud-generator
```

## Alembic migrations

- Generating migrations
```bash
alembic revision --autogenerate -m "create account table"
```

- Applying migrations
```bash
alembic upgrade head
```
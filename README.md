# FastAPI: Clean Architecture & DDD API

This repository is a FastAPI REST API template using Clean Architecture and Domain-Driven Design (DDD), with async SQLAlchemy and Alembic.

## Key Features

- Clean Architecture with explicit layer boundaries.
- Async-first API and persistence flow.
- Dependency injection via FastAPI.
- Mapping between DTOs and entities using `py-automapper`.
- Cookiecutter CRUD generator to scaffold new modules.
- JWT-based authentication flow.
- SQLAlchemy + Alembic integration for persistence and migrations.
- RabbitMQ-based messaging with transactional outbox publishing.

## Architecture

- `src/domain`
  - Entities, repository interfaces, domain exceptions.
- `src/application`
  - Use-case services and application DTOs.
  - Request DTOs: `src/application/dto/request`
  - Model DTOs: `src/application/dto/model`
- `src/infrastructure`
  - Repository implementations, DB/session setup, IoC wiring.
- `src/presentation`
  - FastAPI routes and API schemas.
  - Routes: `src/presentation/api/v1`
  - Request/response schemas: `src/presentation/api/schemas`

## DTO and Schema Flow

- Presentation layer receives/returns Pydantic schemas.
- Routes convert request schemas into application request/model DTOs.
- Services work with application DTOs and domain entities.
- Responses are validated back into presentation response schemas.

## CRUD Generator

The generator templates are in `crud-generator`.

Generated files are moved to:
- Repositories: `src/infrastructure/data/repository`
- Repository interfaces: `src/domain/interface/repository`
- Services: `src/application/service`
- Service interfaces: `src/application/interface/service`
- Entities: `src/domain/entity`
- Presentation schemas: `src/presentation/api/schemas`
- Routes: `src/presentation/api/v1`
- DB configurations: `src/infrastructure/data/configuration`

After generation, the schema is also copied to:
- `src/application/dto/model`

The hook updates route registration in the selected app module (`APP_MODULE` when provided, otherwise `main:app`).

## Setup

1. Prerequisites
- Python 3.9+
- PostgreSQL
- RabbitMQ

2. Clone
```bash
git clone https://github.com/weverkley/Fastapi-Clean-DDD.git
cd Fastapi-Clean-DDD
```

3. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` (especially `DATABASE_URL`).

Default RabbitMQ vars in `.env.example`:
- `RABBITMQ_URL=amqp://guest:guest@localhost:5672/`
- `RABBITMQ_HOST=localhost`
- `RABBITMQ_PORT=5672`
- `RABBITMQ_USER=guest`
- `RABBITMQ_PASSWORD=guest`

If using Docker services:
```bash
docker compose build
docker compose run --rm api alembic -c alembic.ini.example upgrade head
docker compose up -d
```

## Run

```bash
uvicorn main:app --reload
```

## Messaging Layer (Producer/Consumer)

Implemented pattern:
- Producer writes domain data and outbox event in the same DB transaction.
- Outbox publisher worker reads pending outbox rows and publishes using the configured bus provider.
- Consumer worker subscribes to `user.created.v1` with idempotency tracking.
- Dead-letter routing is enabled for consumer queue failures.

Files:
- Outbox table/entity: `src/domain/entity/outbox_message_entity.py`
- Outbox repository: `src/infrastructure/data/repository/outbox_repository.py`
- RabbitMQ publisher adapter: `src/infrastructure/messaging/adapters/outbound/rabbitmq_outgoing_event_publisher.py`
- GCP Pub/Sub publisher adapter: `src/infrastructure/messaging/adapters/outbound/pubsub_outgoing_event_publisher.py`
- Outgoing publisher port: `src/application/interface/messaging/outgoing_event_publisher.py`
- Outbox publish use case handler: `src/application/handlers/publish_outbox_batch_handler.py`
- Outgoing publisher factory: `src/infrastructure/messaging/factories/outgoing_event_publisher_factory.py`
- Publisher worker: `src/infrastructure/entrypoints/worker_outbox_publisher.py`
- Consumer worker: `src/infrastructure/entrypoints/worker_user_created_consumer.py`
- Consumer orchestration: `src/infrastructure/messaging/consumers/user_created_consumer.py`
- Inbound adapter port: `src/application/interface/messaging/incoming_event_adapter.py`
- Inbound adapters:
  - `src/infrastructure/messaging/adapters/inbound/rabbitmq_incoming_event_adapter.py`
  - `src/infrastructure/messaging/adapters/inbound/pubsub_incoming_event_adapter.py`
- Consumer use case handler: `src/application/handlers/user_created_event_handler.py`

Bus provider selection:
- `MESSAGE_BUS_PROVIDER=rabbitmq` (default)
- `MESSAGE_BUS_PROVIDER=gcp_pubsub`

For GCP Pub/Sub set:
- `GCP_PROJECT_ID=<your-project-id>`
- `GCP_PUBSUB_USER_CREATED_SUBSCRIPTION=<subscription-id>`
- `GOOGLE_APPLICATION_CREDENTIALS=<path to service account json>`

Run migrations:
```bash
alembic -c alembic.ini.example upgrade head
```

Run workers:
```bash
python src/infrastructure/entrypoints/worker_outbox_publisher.py
python src/infrastructure/entrypoints/worker_user_created_consumer.py
```

Docker entrypoints:
```bash
docker compose up -d api worker_outbox_publisher worker_user_created_consumer
```

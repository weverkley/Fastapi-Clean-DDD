# FastAPI: Clean Architecture & DDD API

This repository provides a complete REST API implementation in **FastAPI**, demonstrating the principles of **Clean Architecture** and **Domain-Driven Design (DDD)**. The project uses `py-automapper` for object mapping between layers, `SQLAlchemy` for asynchronous ORM, and `Alembic` for database migrations.

The main goal is to offer a robust and practical template for building scalable and maintainable Python applications, especially for projects with complex business logic.

## ✨ Key Features

* **Modern Architecture**: Clear implementation of Clean Architecture and DDD tactical patterns.
* **Async by Default**: Uses `async/await` across all layers, from API routes to database queries with `asyncpg`.
* **Dependency Injection**: Leverages FastAPI's dependency injection system to decouple layers.
* **Automatic Mapping**: Uses `py-automapper` to reduce boilerplate when converting DTOs (Schemas) into domain Entities.
* **Code Generation**: Includes a Cookiecutter-based CRUD generator to automate the creation of new entities, speeding up development.
* **JWT Authentication**: Authentication and authorization logic based on JSON Web Tokens.
* **ORM and Migrations**: Integration with SQLAlchemy for object-relational mapping and Alembic for managing database schema migrations.

## 🏛️ Design Philosophy

### 1. Clean Architecture

The core of the project is the **separation of concerns**, achieved by dividing the software into layers. The most important principle is the **Dependency Rule**: *source code dependencies can only point inwards*.

* **`src/domain`**: Contains business Entities, Repository interfaces, and custom exceptions. It is the heart of the application, with no external dependencies.
* **`src/application`**: Orchestrates the data flow and contains the application-specific business logic (Use Cases), implemented as Services. It defines the DTOs (Pydantic Schemas) for data transfer.
* **`src/infrastructure`**: Implements the interfaces from the domain layer. It contains details of frameworks and technologies, such as database configuration, repository implementations, and the Inversion of Control (IoC) container.
* **`src/presentation`**: The outermost layer, responsible for interaction with the user. In this case, the FastAPI API and its routes.

### 2. Domain-Driven Design (DDD)

DDD is an approach that focuses on a deep understanding of the business domain. This project uses the following tactical patterns:

* **Entity**: An object with a distinct identity that persists over time (e.g., `UserEntity`).
* **Repository**: An interface that abstracts the persistence mechanism, allowing access to domain objects as if they were in a collection.

### 3. Automatic Mapping with `py-automapper`

To reduce repetitive code and simplify data conversion between layers, this project uses the `py-automapper` library. The mapping between the Pydantic Schemas of the Application layer and the Entities of the Domain layer is configured centrally.

* **Why?** Automatic mapping speeds up development and reduces the chance of manual errors in object conversions. The logic for creating an entity from a schema is simplified, as seen in the `BaseService`.
* **Where is it configured?** Mappings are registered at application startup through the `configure_mappings` function, which in turn calls the specific configurations for each entity, such as `map_user`.

## 🚀 Setup and Installation

Follow these steps to run the project locally.

1.  **Prerequisites**
    * Python 3.9+
    * An active PostgreSQL server

2.  **Clone the Repository**
    ```bash
    git clone [https://github.com/weverkley/Fastapi-Clean-DDD.git](https://github.com/weverkley/Fastapi-Clean-DDD.git)
    cd Fastapi-Clean-DDD
    ```

3.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables**
    Create a `.env` file from the example:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file with your configurations, especially the `DATABASE_URL`.

## ⚙️ Usage

### Running the Application

To start the API server, run the following command:

```bash
uvicorn main:app --reload

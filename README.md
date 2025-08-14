# FastAPI: Clean Architecture & DDD API

This repository provides a sample implementation of a REST API in **FastAPI** that demonstrates the principles of **Clean Architecture** and **Domain-Driven Design (DDD)**. It uses an **imperative (manual) approach for mapping** data between layers and secures endpoints using **JWT-based authentication middleware**.

The primary goal is to offer a clear, practical template for building scalable, maintainable, Python applications, especially for projects with complex business logic.

## Core Concepts & Design Philosophy

This project is built on a specific set of architectural choices. Before diving in, it's crucial to understand the philosophy and the trade-offs involved.

### 1. Clean Architecture

The core idea of Clean Architecture is the **separation of concerns**, achieved by dividing the software into layers. The most important rule is the **Dependency Rule**: *source code dependencies can only point inwards*. Nothing in an inner layer can know anything at all about an outer layer.

* **Entities (Domain Layer)**: Contains the core business objects and rules. This is the heart of your application.
* **Use Cases (Application Layer)**: Orchestrates the flow of data to and from the entities to achieve business objectives.
* **Interface Adapters (Infrastructure/Presentation Layers)**: Convert data between the format most convenient for the use cases and entities, and the format most convenient for an external agency such as the Database or the Web.
* **Frameworks & Drivers (Outer Layer)**: Contains the implementation details like the web framework (FastAPI), database (PostgreSQL), etc.

### 2. Domain-Driven Design (DDD)

DDD is a software development approach that emphasizes a deep understanding of the business domain. This project uses several DDD tactical patterns:

* **Entity**: An object with a distinct identity that persists over time (e.g., a `User` with a unique ID).
* **Repository**: A collection-like interface for accessing domain objects, abstracting away the persistence mechanism.

### 3. Imperative Mapping

This project **intentionally avoids automatic mapping libraries** (like `pydantic-automapper`). Instead, data is mapped manually between layers (e.g., from a Pydantic schema in the Presentation layer to a domain Entity).

* **Why?** This approach makes the mapping process explicit and transparent. There is no "magic." It's easier to debug, gives you full control over the transformation logic, and avoids introducing another third-party dependency solely for mapping.
* **The Trade-off**: Manual mapping is more verbose and requires writing more boilerplate code. For simple applications, this can feel like unnecessary overhead.

## Setup and Installation

Follow these steps to get the project running locally.

1.  **Prerequisites**
    * Python 3.9+
    * An active PostgreSQL server

2.  **Clone the Repository**

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
    Create a `.env` file by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file with your specific configurations:
    ```dotenv
    APP_ENV=development
    SECRET_KEY=123123
    DATABASE_URL=postgresql+asyncpg://postgres:123456@localhost:5432/database
    ```

## Running the Application

To start the API server, run the following command from the root directory:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

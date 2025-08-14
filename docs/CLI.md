# CLI for Code Generation

This command-line interface (CLI) tool is built with Cookiecutter to automate the creation of the necessary files for a new entity in your project. It generates the entity, schema, repository, service, configuration, and route files based on a template.

## 1. Installation

Before using the generator, you need to have Cookiecutter and Jinja2-strcase installed. You can install it via pip:

```bash
pip install cookiecutter jinja2-strcase
```

## 2. Usage

To generate the code for a new entity, run the `cookiecutter` command and point it to the `crud-generator` directory.

The CLI will prompt you to enter the `entity_name`. The name should be in `PascalCase` (e.g., `UserProfile`, `ProductItem`).

```bash
cookiecutter crud-generator
```

## 3. Example: Generating a "User" Entity

Let's walk through an example of generating the files for a "User" entity.

### Running the Command

1.  Open your terminal.
2.  Run the generator:

    ```bash
    cookiecutter crud-generator
    ```

3.  When prompted, enter `User` for the `entity_name`:

    ```
    entity_name [User]: User
    ```

### Expected Output

After you enter the entity name, the `post_gen_project.py` hook will run, moving and renaming the files. You will see an output similar to this:

```
Moved user_configuration.py to src/infrastructure/data/configuration/user_configuration.py
Moved user_entity.py to src/domain/entity/user_entity.py
Moved user_repository.py to src/infrastructure/data/repository/user_repository.py
Moved user_routes.py to src/presentation/api/v1/user_routes.py
Moved user_schema.py to src/application/schemas/user_schema.py
Moved user_service.py to src/application/service/user_service.py
Moved i_user_repository.py to src/domain/interface/repository/user_repository.py
Moved i_user_service.py to src/application/interface/service/user_service.py
Cleaned up /path/to/your/project/user
```

### Generated Files and Locations

The following files will be automatically created and moved to their correct locations:

* `src/application/interface/service/user_service.py`
* `src/application/schemas/user_schema.py`
* `src/application/service/user_service.py`
* `src/domain/entity/user_entity.py`
* `src/domain/interface/repository/user_repository.py`
* `src/infrastructure/data/configuration/user_configuration.py`
* `src/infrastructure/data/repository/user_repository.py`
* `src/presentation/api/v1/user_routes.py`
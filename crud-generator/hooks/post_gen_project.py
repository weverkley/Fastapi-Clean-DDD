import os
import shutil
import subprocess
import textwrap

def _add_imports_if_missing(file_path: str, required_imports: list[str]):
    """
    Reads a file and adds the required imports if they are not already present.
    """
    try:
        with open(file_path, "r") as f:
            existing_lines = [line.rstrip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Warning: Could not find file at {file_path} to add imports.")
        return

    stripped_existing_lines = [line.strip() for line in existing_lines]
    new_imports = [
        imp for imp in required_imports if imp.strip() not in stripped_existing_lines
    ]

    if not new_imports:
        return

    last_import_index = -1
    for i, line in enumerate(existing_lines):
        if line.strip().startswith("from") or line.strip().startswith("import"):
            last_import_index = i
    
    for new_import in reversed(new_imports):
        existing_lines.insert(last_import_index + 1, new_import)

    with open(file_path, "w") as f:
        f.write("\n".join(existing_lines))
        f.write("\n")


def update_project_files(entity_name, entity_name_snake_case, project_root):
    """
    Updates all necessary project files (IOC, main.py) with the new entity's configuration.
    """
    entity_title = entity_name.title()

    # --- Update main.py ---
    main_py_file = os.path.join(project_root, "main.py")
    router_import_str = f"from src.presentation.api.v1 import {entity_name_snake_case}_routes as {entity_name_snake_case}_router"
    router_include_str = f"internal_router.include_router({entity_name_snake_case}_router.router, prefix=\"/{entity_name_snake_case}s\", tags=[\"{entity_name}s\"])"

    try:
        with open(main_py_file, "r+") as f:
            lines = [line.rstrip() for line in f.readlines()]
            stripped_lines = [line.strip() for line in lines]

            if router_import_str not in stripped_lines:
                last_import_index = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith("from") or line.strip().startswith("import"):
                        last_import_index = i
                lines.insert(last_import_index + 1, router_import_str)

            if router_include_str not in stripped_lines:
                insert_index = -1
                for i, line in enumerate(lines):
                    if "configure_mappings()" in line:
                        insert_index = i
                        break
                
                if insert_index != -1:
                    # Insert the new router line AFTER the configure_mappings() line
                    lines.insert(insert_index + 1, router_include_str)
            
            f.seek(0)
            f.write("\n".join(lines) + "\n")
            f.truncate()
        print(f"Updated {main_py_file}")
    except FileNotFoundError:
        print(f"Warning: main.py not found at {main_py_file}. Could not update routes.")


    # --- Update ioc/mappings.py ---
    mappings_file = os.path.join(project_root, "src/infrastructure/ioc/mappings.py")
    map_import_str = f"from src.infrastructure.data.configuration.{entity_name_snake_case}_configuration import map_{entity_name_snake_case}"
    map_call_str = f"    map_{entity_name_snake_case}()"
    with open(mappings_file, "r+") as f:
        lines = [line.rstrip() for line in f.readlines()]
        stripped_lines = [line.strip() for line in lines]
        
        if map_import_str.strip() not in stripped_lines:
            last_import_index = -1
            for i, line in enumerate(lines):
                if line.strip().startswith("from"):
                    last_import_index = i
            lines.insert(last_import_index + 1, map_import_str)
            
        if map_call_str.strip() not in stripped_lines:
            map_user_index = -1
            for i, line in enumerate(lines):
                if "map_user()" in line:
                    map_user_index = i
                    break
            if map_user_index != -1:
                lines.insert(map_user_index + 1, map_call_str)
        
        f.seek(0)
        f.write("\n".join(lines) + "\n")
        f.truncate()
    print(f"Updated {mappings_file}")


    # --- Update ioc/repository.py ---
    repository_file = os.path.join(project_root, "src/infrastructure/ioc/repository.py")
    repo_imports = [
        "from fastapi import Depends",
        "from sqlalchemy.ext.asyncio import AsyncSession",
        "from src.infrastructure.data.session.base import get_session",
        f"from src.domain.interface.repository.{entity_name_snake_case}_repository import I{entity_name}Repository",
        f"from src.infrastructure.data.repository.{entity_name_snake_case}_repository import {entity_name}Repository",
    ]
    _add_imports_if_missing(repository_file, repo_imports)
    repo_function = (
        "\n\n"
        f"def get_{entity_name_snake_case}_repository(\n"
        f"    session: AsyncSession = Depends(get_session),\n"
        f") -> I{entity_name}Repository:\n"
        f"    return {entity_name}Repository(session)\n"
    )
    with open(repository_file, "a") as f:
        f.write(repo_function)
    print(f"Updated {repository_file}")


    # --- Update ioc/service.py ---
    service_file = os.path.join(project_root, "src/infrastructure/ioc/service.py")
    service_imports = [
        "from fastapi import Depends",
        f"from src.application.interface.service.{entity_name_snake_case}_service import I{entity_name}Service",
        f"from src.infrastructure.ioc.repository import get_{entity_name_snake_case}_repository",
        f"from src.application.service.{entity_name_snake_case}_service import {entity_name}Service",
        f"from src.domain.interface.repository.{entity_name_snake_case}_repository import I{entity_name}Repository",
    ]
    _add_imports_if_missing(service_file, service_imports)
    service_function = (
        "\n\n"
        f"def get_{entity_name_snake_case}_service(\n"
        f"    repo: I{entity_name}Repository = Depends(get_{entity_name_snake_case}_repository),\n"
        f") -> I{entity_name}Service:\n"
        f"    return {entity_name}Service(repo)\n"
    )
    with open(service_file, "a") as f:
        f.write(service_function)
    print(f"Updated {service_file}")

def move_generated_files():
    """
    Main function to orchestrate file moving and project file updates.
    """
    entity_name = "{{ cookiecutter.entity_name }}"
    entity_name_snake_case = "{{ cookiecutter.entity_name_snake_case.lower() }}"
    temp_dir = os.getcwd()
    project_root = os.path.dirname(temp_dir)

    print(f"Project root detected: {project_root}")

    dest_paths = {
        f"{entity_name_snake_case}_repository.py": os.path.join(project_root, "src/infrastructure/data/repository"),
        f"i_{entity_name_snake_case}_repository.py": os.path.join(project_root, "src/domain/interface/repository"),
        f"{entity_name_snake_case}_service.py": os.path.join(project_root, "src/application/service"),
        f"i_{entity_name_snake_case}_service.py": os.path.join(project_root, "src/application/interface/service"),
        f"{entity_name_snake_case}_entity.py": os.path.join(project_root, "src/domain/entity"),
        f"{entity_name_snake_case}_schema.py": os.path.join(project_root, "src/application/schemas"),
        f"{entity_name_snake_case}_routes.py": os.path.join(project_root, "src/presentation/api/v1"),
        f"{entity_name_snake_case}_configuration.py": os.path.join(project_root, "src/infrastructure/data/configuration"),
    }

    for file_name, dest_folder in dest_paths.items():
        os.makedirs(dest_folder, exist_ok=True)
        source_file = os.path.join(temp_dir, file_name)
        dest_file_name = file_name[2:] if file_name.startswith("i_") else file_name
        dest_file = os.path.join(dest_folder, dest_file_name)

        if os.path.exists(source_file):
            shutil.move(source_file, dest_file)
            print(f"Moved {file_name}")
        else:
            print(f"Warning: {file_name} not found")

    # After moving files, update the project files
    update_project_files(entity_name, entity_name_snake_case, project_root)
    
    print(f"Cleaning up temporary directory: {temp_dir}")
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    move_generated_files()
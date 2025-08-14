from src.infrastructure.data.configuration.user_configuration import map_user

def configure_mappings():
    """
    Registers all application object mappings.
    This function should be called once at startup.
    """

    map_user()

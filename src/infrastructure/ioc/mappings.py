from src.infrastructure.data.configuration.user_configuration import map_user
from src.infrastructure.data.configuration.outbox_message_configuration import map_outbox_message
from src.infrastructure.data.configuration.processed_message_configuration import map_processed_message

def configure_mappings():
    """
    Registers all application object mappings.
    This function should be called once at startup.
    """

    map_user()
    map_outbox_message()
    map_processed_message()

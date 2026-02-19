from src.infrastructure.data.configuration.user_configuration import map_user
from src.infrastructure.data.configuration.outbox_message_configuration import map_outbox_message
from src.infrastructure.data.configuration.processed_message_configuration import map_processed_message
from src.infrastructure.data.configuration.product_configuration import map_product
from src.infrastructure.data.configuration.stock_configuration import map_stock
from src.infrastructure.data.configuration.cart_configuration import map_cart
from src.infrastructure.data.configuration.cart_item_configuration import map_cart_item
from src.infrastructure.data.configuration.order_configuration import map_order

def configure_mappings():
    """
    Registers all application object mappings.
    This function should be called once at startup.
    """

    map_user()
    map_product()
    map_stock()
    map_cart()
    map_cart_item()
    map_order()
    map_outbox_message()
    map_processed_message()

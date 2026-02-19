import time
import unittest
from uuid import uuid4

import requests

from tests.integration.config import (
    EVENTUAL_TIMEOUT_SECONDS,
    POLL_INTERVAL_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
)
from tests.integration.http_client import request_json, url, wait_for_api_ready


class CheckoutFlowIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        wait_for_api_ready()

    def test_checkout_end_to_end_with_workers(self) -> None:
        suffix = uuid4().hex[:10]

        user = request_json(
            "POST",
            "/users/",
            200,
            {
                "name": f"User {suffix}",
                "email": f"user-{suffix}@example.com",
                "password": "secret123",
                "phone_number": "+15550000000",
            },
        )
        user_id = int(user["id"])

        product = request_json(
            "POST",
            "/products/",
            200,
            {
                "name": f"Product {suffix}",
                "sku": f"SKU-{suffix}",
                "price": "19.90",
                "active": True,
            },
        )
        product_id = int(product["id"])

        request_json(
            "POST",
            "/stocks/",
            200,
            {
                "product_id": product_id,
                "available_quantity": 10,
                "reserved_quantity": 0,
            },
        )

        cart = request_json(
            "POST",
            "/carts/",
            200,
            {
                "user_id": user_id,
            },
        )
        cart_id = int(cart["id"])

        cart_with_item = request_json(
            "POST",
            f"/carts/{cart_id}/items",
            200,
            {
                "product_id": product_id,
                "quantity": 2,
            },
        )
        self.assertEqual(cart_with_item["id"], cart_id)
        self.assertGreaterEqual(len(cart_with_item["items"]), 1)

        checkout_result = request_json("POST", f"/carts/{cart_id}/checkout", 200)
        self.assertEqual(checkout_result["status"], "checkout_requested")

        deadline = time.time() + EVENTUAL_TIMEOUT_SECONDS
        matched_order: dict | None = None

        while time.time() < deadline:
            orders = request_json("GET", "/orders/", 200)
            for order in orders:
                if int(order["cart_id"]) == cart_id:
                    matched_order = order
                    break

            if matched_order and matched_order.get("status") == "completed":
                break

            time.sleep(POLL_INTERVAL_SECONDS)

        self.assertIsNotNone(matched_order, "Order was not created from checkout event.")
        self.assertEqual(matched_order["status"], "completed")

        stock_after = request_json("GET", f"/stocks/{product_id}", 200)
        self.assertEqual(int(stock_after["available_quantity"]), 8)
        self.assertEqual(int(stock_after["reserved_quantity"]), 0)

        cart_after = request_json("GET", f"/carts/{cart_id}", 200)
        self.assertEqual(cart_after["status"], "ordered")

        second_checkout = requests.post(
            url(f"/carts/{cart_id}/checkout"),
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        self.assertEqual(second_checkout.status_code, 400)


if __name__ == "__main__":
    unittest.main()

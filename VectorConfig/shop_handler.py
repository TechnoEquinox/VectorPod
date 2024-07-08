#!/usr/bin/env python3

import json
import os

class ShopHandler:
    def __init__(self):
        self.robot_config_path = os.path.join(os.path.expanduser("~"), "wire-pod/chipper/webroot/robot_config.json")
        self.shop_items_path = os.path.join(os.path.expanduser("~"), "wire-pod/chipper/webroot/shop_items.json")

    def read_json_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    def write_json_file(self, filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def validate_purchase(self, robot_data, item):
        if robot_data["robot_wallet"] < item["cost"]:
            return False, "Purchase invalidated. Not enough coins."
        # Additional validation logic can be added here (e.g., inventory space)
        return True, "Purchase validated."

    def handle_purchase(self, item_id):
        robot_data = self.read_json_file(self.robot_config_path)
        shop_items = self.read_json_file(self.shop_items_path)

        item = next((item for item in shop_items if item["id"] == item_id), None)
        if not item:
            return False, "Item not found. (This shouldn't happen)"

        is_valid, message = self.validate_purchase(robot_data, item)
        if not is_valid:
            return False, message

        robot_data["robot_wallet"] -= item["cost"]
        robot_data.setdefault("items", []).append(item_id)  # Assuming robot_data has an "items" field

        self.write_json_file(self.robot_config_path, robot_data)
        return True, "Purchase successful."

import json

# Define a ShopItem class to hold item details
class ShopItem:
    def __init__(self, item_id, name, description, price, **kwargs):
        self.id = item_id
        self.name = name
        self.description = description
        self.price = price
        self.attributes = kwargs

# Shop class to manage shop operations
class Shop:
    def __init__(self, items):
        self.items = items

    def display_items(self):
        for index, item in enumerate(self.items, start=1):
            print(f"{index}. {item.name} - {item.description} - {item.price} coins")

    def purchase_item(self, item_index, robot_data):
        if item_index < 1 or item_index > len(self.items):
            print("Invalid item choice!")
            return

        item = self.items[item_index - 1]

        if robot_data["robot_wallet"] < item.price:
            print(f"You don't have enough coins to buy {item.name}!")
            return

        robot_data["robot_wallet"] -= item.price
        robot_data.setdefault("items", []).append(item.name)
        print(f"Purchased {item.name} for {item.price} coins!")

        # Save changes to the JSON file
        with open('../VectorConfig/robot_config.json', 'w') as file:
            json.dump(robot_data, file, indent=4)

# Load robot data from JSON
def load_robot_data():
    with open('../VectorConfig/robot_config.json', 'r') as file:
        return json.load(file)

def main():
    robot_data = load_robot_data()

    # Create some shop items with IDs
    items = [
        ShopItem(1, "Juice Box", "Will refill 10 energy when used", 5, energy_refill=10),
        ShopItem(2, "Red Bull", "Will refill 30 energy when used", 8, energy_refill=30),
        ShopItem(3, "Wild Grass Seed", "A seed to grow wild grass! Grows in 4 hours and doesn't require water!", 10, grow_time="4 hours", num_times_water=0),
        ShopItem(4, "Sunflower", "A seed to grow a sunflower! Grows in 8 hours and requires water!", 20, grow_time="8 hours", num_times_water=1)
    ]

    shop = Shop(items)

    while True:
        print("\n=== Vector's Shop ===")
        shop.display_items()
        print("0. Exit")

        choice = int(input("Enter the number of the item you want to purchase: "))

        if choice == 0:
            break

        shop.purchase_item(choice, robot_data)

if __name__ == "__main__":
    main()
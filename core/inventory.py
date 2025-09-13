# player inventory class, this goes into the inventory screen
class PlayerInventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        # Debug
        """if isinstance(item, str):
            print(f"Tried to add string to inventory: {item}")
        else:
            print(f"Added item to inventory: {item.name}")"""
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def list_items(self):
        return self.items
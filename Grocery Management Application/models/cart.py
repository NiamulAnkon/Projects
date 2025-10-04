class Cart:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, item_name, price):
        self.items.append((item_name, price))
        self.total += price

    def remove_item(self, item_name):
        for item in self.items:
            if item[0] == item_name:
                self.total -= item[1]
                self.items.remove(item)
                break

    def get_total(self):
        return self.total

    def get_items(self):
        return self.items

    def clear_cart(self):
        self.items = []
        self.total = 0

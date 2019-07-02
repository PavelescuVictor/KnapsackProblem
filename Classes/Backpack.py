class Backpack:

    def __init__(self):
        self.backpack_storage = []
        self.max_weight = 0

    def get_element_by_index(self, index):
        return self.backpack_storage[index]

    def add_item(self, item):
        self.backpack_storage.append(item)

    def get_backpack(self):
        return self.backpack_storage

    def get_max_weight(self):
        return self.max_weight

    def set_max_weight(self, max_weight):
        self.max_weight = max_weight

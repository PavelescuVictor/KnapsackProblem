class Item:

    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def get_value(self):
        return self.value

    def get_weight(self):
        return self.weight

    def to_string(self):
        return "Value: " + str(self.value) + " Weight: " + str(self.weight)

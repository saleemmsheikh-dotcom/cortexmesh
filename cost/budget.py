class Budget:

    def __init__(self, limit=10):
        self.limit = limit
        self.count = 0

    def tick(self):
        self.count += 1

    def exceeded(self):
        return self.count >= self.limit
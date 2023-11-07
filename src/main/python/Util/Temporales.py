class Temporales:

    def __init__(self):
        self.counter = 0

    def next_temporal(self):
        temporal = f't{self.counter}'
        self.counter += 1
        return temporal


class Player:
    def __init__(self, order):
        self.money = 3000
        self.gpa = 3.0
        self.local = 0
        self.stop = 0
        self.count = 0
        if order == 0:
            self.name = 'Litell E'
        elif order == 1:
            self.name = 'Pikachu'
        elif order == 2:
            self.name = 'Psyduck'
        elif order == 3:
            self.name = 'Little Yellow Chicken'


#transform.py
import math

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @classmethod
    def zero(cls):
        return cls(x=0, y=0)

    def t_pos(self) -> list[float]:
        return [self.x, self.y]

    def vector2(self):
        return Vector2(self.x, self.y)

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def normalize(self) -> list:
        magnitude = math.sqrt(self.x ** 2 + self.y ** 2)

        if(magnitude == 0):
            self.x = 0
            self.y = 0

        if(self.x != 0 and self.y != 0):
            self.x = self.x / magnitude
            self.y = self.y / magnitude

    @classmethod
    def zero(cls) -> None:
        return cls(x=0, y=0)

    def point(self):
        return Point(self.x, self.y)
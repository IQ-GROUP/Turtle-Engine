#shapes.py
import turtle as t
from general.objects import Object
from maths.transform import Point

class Circle():
    def __init__(self, world_position=Point.zero(), radius=10, color="black", fill=False, canvas=None, name: str = "Square"):
        self.world_position = world_position
        self.radius = round(radius)
        self.color = color
        self.fill = fill
        self.canvas = canvas
        self.name = name

    def __circle(self, _t):
        _t.setheading(270)
        _t.penup()
        _t.forward(self.radius)
        _t.pendown()

        _t.setheading(0)

        if (self.fill):
            _t.fillcolor(self.color)
            _t.begin_fill()
        _t.color(self.color)
        _t.circle(self.radius)
        if(self.fill):
            _t.end_fill()

    def object(self):
        return Object(
            canvas=self.canvas,
            data={
                "id": self.canvas.generate_object_id(),
                "name": self.name,
                "position": self.canvas.world_to_screen(self.world_position),
                "world_position": self.world_position,
                "instruction": self.__circle,
                "size": {
                    "width": self.radius * 2,
                    "height": self.radius * 2
                },
                "spawned": False
            }
        )


class Square():
    def __init__(self, world_position=Point.zero, height=10, width=10, color="black", fill=False, canvas=None, name: str = "Square"):
        self.world_position = world_position
        self.height = round(height)
        self.width = round(width)
        self.color = color
        self.fill = fill
        self.canvas = canvas
        self.name = name

    def __square(self, _t):
        _t.backward(self.width / 2)
        _t.left(90)
        _t.forward(self.height / 2)

        if (self.fill):
            _t.fillcolor(self.color)
            _t.begin_fill()

        _t.setheading(0)
        _t.color(self.color)

        c = True
        for i in range(4):
            _t.forward(self.width if c else self.height)
            _t.right(90)
            c = not c

        if (self.fill):
            _t.end_fill()

    def object(self):
        return Object(
            canvas=self.canvas,
            data={
                "id": self.canvas.generate_object_id(),
                "name": self.name,
                "position": self.canvas.world_to_screen(self.world_position),
                "world_position": self.world_position,
                "instruction": self.__square,
                "size": {
                    "width": self.width,
                    "height": self.height
                },
                "spawned": False
            }
        )
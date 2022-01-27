#!/usr/bin/python3.8
# -*-coding:utf-8 -*-

#Une approche assez procédurale !!

class NoSuchShapeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Point():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class Square():
    def __init__(self, top_left: Point, side: float) -> None:
        self.top_left = top_left
        self.side = side


class Rectangle():
    def __init__(self, top_left: Point, height: float, width: float) -> None:
        self.top_left = top_left
        self.height = height
        self.width = width


class Circle():
    def __init__(self, center: Point, radius: float) -> None:
        self.center = center
        self.radius = radius


class Geometry():
    PI = 3.141592653589793

    def __init__(self, object_geo) -> None:
        self.object_geo = object_geo

    def area(self):
        if isinstance(self.object_geo, Square):
            return self.object_geo.side * self.object_geo.side
        else:
            if isinstance(self.object_geo, Rectangle):
                return self.object_geo.height * self.object_geo.width
            else:
                if isinstance(self.object_geo, Circle):
                    return self.PI * self.object_geo.radius * self.object_geo.radius
                else:
                    raise NoSuchShapeException()

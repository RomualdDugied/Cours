#!/usr/bin/python3.8
#-*- coding:utf-8 -*-

#APPROCHE OBJET

class NoSuchShapeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Point():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class Square():
    def __init__(self, top_left: Point, side: float) -> None:
        self.__top_left = top_left
        self.__side = side
        
    def origine(self)->Point:
        return self.__top_left
        
    def area(self)->float:
        return self.__side * self.__side
    
    def perimeter(self)->float:
        return self.__side * 4


class Rectangle():
    def __init__(self, top_left: Point, height: float, width: float) -> None:
        self.__top_left = top_left
        self.__height = height
        self.__width = width
    
    def origine(self)->Point:
        return self.__top_left
        
    def area(self)->float:
        return self.__height * self.__width
    
    def perimeter(self)->float:
        return (2 * self.__height) + (2 * self.__width)


class Circle():
    PI = 3.141592653589793
    
    def __init__(self, center: Point, radius: float) -> None:
        self.__center = center
        self.__radius = radius
        
    def origine(self)->Point:
        return self.__center
        
    def area(self)->float:
        return self.__height * self.__width
    
    def perimeter(self)->float:
        return self.PI * self.__radius * self.__radius


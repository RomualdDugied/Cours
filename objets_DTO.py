#!/usr/bin/python3.8
# -*-coding:utf-8 -*-

class Point1():
    """Dans cet exemple l'implémentation est exposé.

        Même avec l'ajout d'ascesseurs (get/set) l'interface serait exposé
    """

    def __init__(self, x: float, y: float) -> None:
        self.x_coordinate = x
        self.y_coordinate = y


class Point():
    """Dans cet exemple, l'implémentation est masquée et l'interface
    ne permet pas de savoir comment sont stockés les coordonnées. L'interface
    propose 2 façon de les exprimés. Elles sont consultables indépendamment mais
    réglable de façon atomique.
    """

    def __init__(self) -> None:
        pass

    def get_x_coordinate(self) -> float:
        pass

    def get_y_coordinate(self) -> float:
        pass

    def set_cartesian(self, x: float, y: float) -> None:
        pass

    def get_radius(self) -> float:
        pass

    def get_theta(self) -> float:
        pass

    def set_polar(self, radius: float, theta: float) -> None:
        pass

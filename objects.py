# Contains objects that will be used by the Romo project
import math

class Point:
    def __init__(self, startX, startY):
        self.currX = startX
        self.currY = startY
        self.repair()
    def setX(self, newX):
        self.currX = newX
        self.repair()
    def setY(self, newY):
        self.currY = newY
        self.repair()
    def repair(self):
        self.pair = (self.currX, self.currY)

class Vector:
    def __init__(self, startPoint1, startPoint2):
        self.point1 = startPoint1
        self.point2 = startPoint2
        
class LandingZone:
    def __init__(self, bottomLeft, width, height):
        self.bottomLeft = bottomLeft
        self.width = width
        self.height = height
        
class TargetObject:
    def __init__(self, bottomLeft, width, height, color):
        self.bottomLeft = bottomLeft
        self.width = width
        self.height = height
        self.color = color
            
class Romo:
    def __init__(self, bottomLeft, width, height, rotation):
        self.bottomLeft = bottomLeft
        self.width = width
        self.height = height
        self.rotation = rotation

        theta = math.atan(self.height/self.width)
        d = self.height/math.sin(theta)
        x = bottomLeft.currX + (d/2) * math.cos(theta + math.radians(self.rotation))
        y = bottomLeft.currY + (d/2) * math.sin(theta + math.radians(self.rotation))

        self.center = Point(x, y)
    def setX(self, newX):
        self.bottomLeft.currX = newX
        self.repair()
    def setY(self, newY):
        self.bottomLeft.currY = newY
        self.repair()
    def repair(self):
        theta = math.atan(self.height/self.width)
        d = self.height/math.sin(theta)
        x = self.bottomLeft.currX + (d/2) * math.cos(theta + math.radians(self.rotation))
        y = self.bottomLeft.currY + (d/2) * math.sin(theta + math.radians(self.rotation))
        self.center = Point(x, y)

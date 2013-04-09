# Contains objects that will be used by the Romo project

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
    def __init__(self, topLeft, width, height):
        self.topLeft = topLeft
        self.width = width
        self.height = height
        
class TargetObject:
    def __init__(self, topLeft, width, height):
        self.topLeft = topLeft
        self.width = width
        self.height = height
        self.centerOfMass = Point(self.topLeft.currX + self.width/2, self.topLeft.currY + self.height/2)
    def isInLandingZone(self, zone):
        if (self.centerOfMass.currX > zone.topLeft.currX and self.centerOfMass.currX < zone.topLeft.currX + width and self.centerOfMass.currY > zone.topLeft.currY and self.centerOfMass.currY < zone.topLeft.currY + height):
            
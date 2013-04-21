# Run with wx interpreter!
# GUI runs into problems when you attempt to close the window or enter a command in 
# maybe run a lop for command or implement threading?
# ask others about using path vector to find intersection point of collisions instead of using steps.

import numpy as np
import time
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation
import pylab
from numpy import sin, cos, pi

rect2 = matplotlib.patches.Rectangle((20,5),3,3)
block_list= [rect2]

fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
rect = matplotlib.patches.Rectangle((5,5),3,3)
ax.add_patch(rect)
ax.add_patch(rect2)
a = 0
x = rect.get_x()
y = rect.get_y()
plt.plot(3,30)
plt.show()

collision_list=[]
"""
romo = rect
check_collision(romo)
while a < 100:
    rect.set_x(x+a*2)
    for elem in collision_list:
        elem.set_x(x+a*2)
    time.sleep(1)
    #ax.add_patch(rect)
    a += 1
    #rect.figure.canvas.draw()
    #if collision(rect)
    plt.draw()
"""     
class Block: 
    def __init__(self,x,y,rotation,width,height): #x and y are lower left vertex
        self.rect = matplotlib.patches.Rectangle((x,y),width,width)
    #vertices are clockwise starting with lower left
        self.v1 = (x,y)
        self.rotation = (rotation*pi)/180
        if rotation != 0:
            trans = matplotlib.transforms.Affine2D().rotate_deg_around(rect.get_x(), rect.get_y(), rotation) + ax.transData
            rect.set_transform(trans)
            self.v2 = (x-height*cos(rotation),y+height*sin(rotation))
            self.v3 = (self.v2[0]+width*cos(rotation),self.v2[1]+width*sin(rotation))
            self.v4 = (x + width*cos(rotation),y+width*sin(rotation))
        else:
            self.v2 = (x,y+height)
            self.v3 = (x+width,y+height)
            self.v4 = (x + width, y)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        #self.animate = False
        ax.add_patch(self.rect)
        plt.draw() 

class Romo(Block):
    def __init__(self,x,y,rotation,width,height): #x and y are lower left vertex
        Block.__init__(self,x,y,rotation,width,height)          
class Segment:
    def __init__(self,p1,p2,block):
         self.block = block
         self.x1 = p1[0]
         self.y1 = p1[1]
         self.x2 = p2[0]
         self.y2 = p2[1]
         if self.x1 == self.x2:
             self.slope = "vertical"
             #self.b = 0
         else:
             self.slope = (self.y2-self.y1)/(self.x2-self.x1)
             self.b = -1*self.x1*(self.slope) + self.y1
             self.function = lambda x: self.slope*x + self.b
         
         # block is an integer value that represents the block's index in the block list.
    def check_intersect(self,seg2):
        if self.slope == "vertical" or seg2.slope == "vertical":
            if seg2.slope == "vertical" and self.slope == "vertical":
                if self.contains(seg2.x1) or self.contains(seg2.x2) or seg2.contains(self.x1) or seg2.contains(self.x2): 
                      return True
                return False
            elif seg2.slope == "vertical":
                if self.contains(seg2.x1):
                    return True
                return False
            elif self.slope == "vertical":
                if seg2.contains(self.x1):
                    return True
                return False
        elif self.slope-seg2.slope == 0: #lines are parallel
            if self.b - seg2.b == 0: #lines are the same
                if self.contains(seg2.x1) or self.contains(seg2.x2) or seg2.contains(self.x1) or seg2.contains(self.x2): 
                      return True
            else: #parallel lines don't intersect
                return False
        else:
            x = (seg2.b - self.b)/(self.slope-seg2.slope)
            if self.contains(x) and seg2.contains(x):
                return True
            return False
    def is_right_of(self, seg): #returns True if seg is to the right of or below this segment
        if self.check_intersect(seg):
            return False
        elif self.slope < 0:
            if self.function(seg.x1) < seg.y1 and self.function(seg.x2) < seg.y2:
                return True
            return False
        elif self.slope == 0:
            if self.y1 > seg.y1 and self.y2 > seg.y2:
                return True
            return False
        elif self.slope > 0:
            if self.function(seg.x1) > seg.y1 and self.function(seg.x2) > seg.y2:
                return True
            return False
        elif self.slope == 'vertical':
            if seg.x1 > self.x1 and seg.x2 > self.x1:
                return True
            return False
    def contains(self,x):
        if x >= self.x1 and x <= self.x2 or x <=self.x1 and x >= self.x2:
            return True
        return False
    def __repr__(self):
        return "Segment from ({0},{1}) to ({2},{3})".format(self.x1,self.y1,self.x2,self.y2)

def check_collision(romo): #Takes a Romo object
    # check for case where romo goes past object!
    #coordinate order is clockwise from bottom left
    r_seg1 = Segment(romo.v1,romo.v2, -1)
    r_seg2 = Segment(romo.v2,romo.v3, -1)
    r_seg3 = Segment(romo.v3,romo.v4, -1)
    r_seg4 = Segment(romo.v4,romo.v1, -1)
    romo_segments = [r_seg1,r_seg2,r_seg3,r_seg4] 
    line_list = []
    for block in block_list:
        index = block_list.get_index(block)
        seg1 = Segment(block.v1,block.v2,index)
        seg2 = Segment(block.v2,block.v3,index)
        seg3 = Segment(block.v3,block.v4,index)
        seg4 = Segment(block.v4,block.v1,index)
        line_list.extend([seg1,seg2,seg3,seg4])
        print(line_list)
        print(romo_segments)
    for seg in line_list:
        for line in romo_segments:
            #print("checking {0} {1}".format(seg,line))
            if seg.check_intersect(line) == True: #will return the first collision it sees!
                collision_list.append(block_list[seg.block])
                return True
    return False

def predict_collision(romo,distance): #only works for positive distances to the right of the Romo right now! 
    #Returns the x distance the Romo can travel in current direction before a collision occurs
    # the follwing creates a box for the Romo path:
    path_seg1 = Segment(romo.v3,(romo.v3[0] + distance*cos(romo.rotation),romo.v3[1] + distance*sin(romo.rotation)),-1)
    path_seg2 = Segment(romo.v4,(romo.v4[0] + distance*cos(romo.rotation),romo.v4[1] + distance*sin(romo.rotation)),-1)
    bound_seg1 = Segment((path_seg1.x1,path_seg1.y1),(path_seg2.x1,path_seg2.y1),-1)
    bound_seg2 = Segment((path_seg1.x2,path_seg1.y2),(path_seg2.x2,path_seg2.y2),-1)
    bounds = [path_seg1,path_seg2,bound_seg1,bound_seg2]
    seg_list = []
    colliding_segs = []
    for block in block_list: #should update this outside of function!
        index = block_list.get_index(block)
        seg1 = Segment(block.v1,block.v2,index)
        seg2 = Segment(block.v2,block.v3,index)
        seg3 = Segment(block.v3,block.v4,index)
        seg4 = Segment(block.v4,block.v1,index)
        seg_list.extend([seg1,seg2,seg3,seg4])
    for seg in seg_list:
        for bound in bounds:
            if seg.check_intersect(bound):
                colliding_segs.append(seg)
        if seg.is_right_of(bound_seg1) and seg.is_right_of(path_seg1) and not seg.is_right_of(bound_seg2) and not seg.is_right_of(path_seg2):
            colliding_segs.append(seg)
    if len(colliding_segs) == 0:
        return False #No collisions in path
    obj = colliding_segs[0]
    if path_seg1.slope == 0:
        x = min(obj.x1,obj.x2)
    elif path_seg1.slope > 0:
        perp_slope = -1/path_seg1.slope
        x = ((-1*perp_slope*obj.x1 + obj.y1) - path_seg1.b)/(path_seg1.slope - perp_slope)
    elif path_seg1.slope == 'vertical':
        if y1 < y2:
            x = obj.x1
        else:
            x = obj.x2
    return x


    
romo = Romo(5,5,0,5,5)
seg1 = Segment((3,7),(7,14),0)
seg2 = Segment((8,7),(0,15),1)

     
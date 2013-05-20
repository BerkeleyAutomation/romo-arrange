# Run with wx interpreter!
# GUI runs into problems when you attempt to close the window or enter a command in 
# maybe run a loop for command or implement threading?
# ask others about using path vector to find intersection point of collisions instead of using steps.

import numpy as np
import time
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation
import pylab
from numpy import sin, cos, pi, exp

fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
a = 0
collision_list=[]
box = []
segs = []

def animate_romo(romo,distance):
    if predict_collision(romo,distance):
        blocks = check_collision(romo)
        total = 0
        while blocks == False:
            #print(blocks)
            d = predict_collision(romo,distance)
            move_distance([romo],d+0.5)
            total += d 
            blocks = check_collision(romo)
            if blocks != False:
                break       
        move_distance([romo,blocks[0]],distance-total)
    else:
        move_distance([romo],distance)
    
def move_distance(obj_list,d):
        #while a < 5:
        print(d)
        for obj in obj_list:
            obj.rect.set_x(obj.rect.get_x() + d*cos(romo.rotation))
            obj.rect.set_y(obj.rect.get_y() + d*sin(romo.rotation))
            
            obj.x = obj.rect.get_x()
            obj.y = obj.rect.get_y()
            obj.update_fields()
        time.sleep(1)
            #ax.add_patch(rect)
            #a += 1
            #rect.figure.canvas.draw()
            #if collision(rect)
        plt.draw() 
  
class Block: #NEED to update vertex and (x,y) positions when moved :(
    def __init__(self,x,y,rotation,width,height): #x and y are lower left vertex
        self.rect = matplotlib.patches.Rectangle((x,y),width,width)
    #vertices are clockwise starting with lower left
        self.v1 = [x,y]
        self.rotation = (rotation*pi)/180
        if self.rotation != 0:
            trans = matplotlib.transforms.Affine2D().rotate_deg_around(self.rect.get_x(), self.rect.get_y(), rotation) + ax.transData
            self.rect.set_transform(trans)
            self.v2 = [x-height*sin(self.rotation),y+height*cos(self.rotation)]
            self.v3 = [self.v2[0]+width*cos(self.rotation),self.v2[1]+width*sin(self.rotation)]
            self.v4 = [x + width*cos(self.rotation),y+width*sin(self.rotation)]
        else:
            self.v2 = [x,y+height]
            self.v3 = [x+width,y+height]
            self.v4 = [x + width, y]
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        #self.animate = False
        ax.add_patch(self.rect)
        plt.draw()
    def update_fields(self):
        #if self.rotation != 0:
        self.v1 = [self.x,self.y]
        self.v2 = [self.x-self.height*sin(romo.rotation),self.y+self.height*cos(romo.rotation)]
        #print(self.y+self.height*cos(romo.rotation))
        self.v3 = [self.v2[0]+self.width*cos(romo.rotation),self.v2[1]+self.width*sin(romo.rotation)]
        self.v4 = [self.x + self.width*cos(romo.rotation),self.y+self.width*sin(romo.rotation)]
        #else:
        #    self.v2 = [self.x,self.y+self.height]
        #    self.v3 = [self.x+self.width,self.y+self.height]
        #    self.v4 = [self.x + self.width, self.y]

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
         self.p1 = list(p1)
         self.p2 = list(p2)
         if self.x1 == self.x2:
             self.slope = "vertical"
             #self.b = 0
         else:
             self.slope = (self.y2-self.y1)/(self.x2-self.x1)
             self.b = -1*self.x1*(self.slope) + self.y1
             self.function = lambda x: self.slope*x + self.b
         
         # block is an integer value that represents the block's index in the block list.
    def closest_intersection(self,seg,romo): #returns the closest point to Romo at which this segment intersects seg. False if no intersection.
        # self must be a path segment from the Romo.
        romo_front = Segment(romo.v3,romo.v4,-1)
        if not self.check_intersect(seg):
            return False
        if self.slope == 'vertical':
            if seg.slope == 'vertical':
                return romo_front.closest_to([seg.p1,seg.p2])[0]
            if seg.slope == 0:
                return (self.x1,seg.y1)
            else:
                x = (-1*seg.b)/(seg.slope - 1)
                return (x,seg.function(x))
        if self.slope == 0:
            if seg.slope == 'vertical':
                return (seg.x1,self.y1)
            if seg.slope == 0:
                return romo_front.closest_to([seg.p1,seg.p2])[0]
            else:
                x = (self.b - seg.b)/(seg.slope)
                return (x,seg.function(x))
        else: #if slope is >0 or <0
            if seg.slope == 0:
                return seg.closest_intersection(self, romo)
            if seg.slope == 'vertical':
                return seg.closest_intersection(self,romo)
            else:
                if self.slope != seg.slope:
                    x = (seg.b - self.b)/(self.slope - seg.slope)
                    return (x,self.function(x))
                else:
                    return romo_front.closest_to([seg.p1,seg.p2])[0]
                    
            
    def check_intersect(self,seg2):
        if self.slope == "vertical" or seg2.slope == "vertical":
            if seg2.slope == "vertical" and self.slope == "vertical":
                if self.contains_x(seg2.x1) or self.contains_x(seg2.x2) or seg2.contains_x(self.x1) or seg2.contains_x(self.x2): 
                      return True
                return False
            elif seg2.slope == "vertical":
                if self.contains_x(seg2.x1) and seg2.contains_y(self.function(seg2.x1)):
                    return True
                return False
            elif self.slope == "vertical":
                if seg2.contains_x(self.x1) and self.contains_y(seg2.function(self.x1)):
                    return True
                return False
        elif self.slope-seg2.slope == 0: #lines are parallel
            if self.b - seg2.b == 0: #lines are the same
                if self.contains_x(seg2.x1) or self.contains_x(seg2.x2) or seg2.contains_x(self.x1) or seg2.contains_x(self.x2): 
                      return True
            else: #parallel lines don't intersect
                return False
        else:
            x = (seg2.b - self.b)/(self.slope-seg2.slope)
            if self.contains_x(x) and seg2.contains_x(x) and self.contains_y(seg2.function(x)) and seg2.contains_y(self.function(x)):
                return True
            return False
    
    def is_right_of(self, seg): #returns True if seg is to the right of or below this segment
        if self.check_intersect(seg):
            return False
        elif self.slope == 'vertical':
            if seg.x1 > self.x1 and seg.x2 > self.x1:
                return True
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
    
    def closest_to(self, list): #given a list of points and this segment (with points not on line) find closest point and return this and distance
        if len(list) == 0:
            return 'EMPTY LIST'
        closest = []
        lowest = 0
        if self.slope == 'vertical':
            print('here')
            closest = list[0]
            lowest = abs(self.x1 - list[0][1])
            min = abs(self.x1 - list[0][1])
            for p in list:
                curr = abs(p[0]-self.x1)
                if curr < min:
                    closest = p
                    lowest = curr
                    min = curr
            return (closest,lowest)
        if self.slope == 0:
            closest = list[0]
            lowest = abs(self.y1 - list[0][1])
            min = abs(self.y1 - list[0][1])
            for p in list:
                curr = abs(p[1]-self.y1)
                if  curr < min:
                    closest = p
                    lowest = curr
                    min = curr
            return (closest,lowest)
        else: #assuming a perpendicular through the SEGMENT will hit the point
            perp_slope = -1/self.slope
            closest = list[0]
            x = (self.b+perp_slope*closest[0] - closest[1])/(perp_slope-self.slope)
            y = self.function(x)
            d = ((x-closest[0])**2 + (y-closest[1])**2)**0.5
            lowest = d
            min = 100000
            for p in list:
                x = (self.b+perp_slope*p[0] - p[1])/(perp_slope-self.slope)
                y = self.function(x)
                d = ((x-p[0])**2 + (y-p[1])**2)**0.5
                if d < min:
                    closest = p
                    lowest = d
                    min = d
            return (closest,lowest)
                 
    def is_in_box(self,seg_list): #given list of 4 segments, determine if this segment is within the box.
        if seg_list[2].slope == 0:
            if seg_list[2].y1 < seg_list[0].y1:
                if self.is_right_of(seg_list[3]) and self.is_right_of(seg_list[0]) and not self.is_right_of(seg_list[1]) and not self.is_right_of(seg_list[2]):
                    return True
                else:
                    return False
            else:
                if self.is_right_of(seg_list[1]) and self.is_right_of(seg_list[2]) and not self.is_right_of(seg_list[3]) and not self.is_right_of(seg_list[0]):
                    return True
                else:
                    return False
        if seg_list[2].slope == 'vertical':
            if seg_list[2].x1 < seg_list[0].x1:
                if self.is_right_of(seg_list[2]) and self.is_right_of(seg_list[3]) and not self.is_right_of(seg_list[0]) and not self.is_right_of(seg_list[1]):
                    return True
                else:
                    return False
            else:
                if self.is_right_of(seg_list[0]) and self.is_right_of(seg_list[1]) and not self.is_right_of(seg_list[2]) and not self.is_right_of(seg_list[3]):
                    return True
                else:
                    return False
        if seg_list[2].slope < 0:
            if seg_list[2].x2 < romo.v4[0]:
                if self.is_right_of(seg_list[0]) and self.is_right_of(seg_list[1]) and not self.is_right_of(seg_list[2]) and not self.is_right_of(seg_list[3]):
                    return True
                return False
            else:
                if self.is_right_of(seg_list[2]) and self.is_right_of(seg_list[3]) and not self.is_right_of(seg_list[0]) and not self.is_right_of(seg_list[1]):
                    return True
                return False  
        if seg_list[2].slope > 0:
            if seg_list[2].y2 < romo.v4[0]:
                if self.is_right_of(seg_list[3]) and self.is_right_of(seg_list[0]) and not self.is_right_of(seg_list[1]) and not self.is_right_of(seg_list[2]):
                    return True
                else:
                    return False
            else:
                if self.is_right_of(seg_list[1]) and self.is_right_of(seg_list[2]) and not self.is_right_of(seg_list[3]) and not self.is_right_of(seg_list[0]):
                    return True
                return False
    def contains_x(self,x):
        if x >= self.x1 and x <= self.x2 or x <=self.x1 and x >= self.x2:
            return True
        return False
    def contains_y(self,y):
        if y >= self.y1 and y <= self.y2 or y <=self.y1 and y >= self.y2:
            return True
        return False
    def __repr__(self):
        return "Segment from ({0},{1}) to ({2},{3})".format(self.x1,self.y1,self.x2,self.y2)
        
def is_in_box(point,bounds):
    if point[0] > min(bounds[0].x1,bounds[0].x2,bounds[1].x1,bounds[1].x2) and point[0] < max(bounds[0].x1,bounds[0].x2,bounds[1].x1,bounds[1].x2) and point[1] > min(bounds[0].y1,bounds[0].y2,bounds[1].y1,bounds[1].y2) and point[1] < max(bounds[0].y1,bounds[0].y2,bounds[1].y1,bounds[1].y2):
        return True
    return False

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
        index = block_list.index(block)
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
                return block_list
    return False

def predict_collision(romo,distance): #only works for positive distances to the right of the Romo right now! 
    #Returns the distance the Romo can travel in current direction before a collision occurs
    # the follwing creates a box for the Romo path:
    path_seg1 = Segment(romo.v3,(romo.v3[0] + distance*cos(romo.rotation),romo.v3[1] + distance*sin(romo.rotation)),-1)
    #print(path_seg1)
    path_seg2 = Segment(romo.v4,(romo.v4[0] + distance*cos(romo.rotation),romo.v4[1] + distance*sin(romo.rotation)),-1)
    bound_seg1 = Segment((path_seg1.x1,path_seg1.y1),(path_seg2.x1,path_seg2.y1),-1)
    bound_seg2 = Segment((path_seg1.x2,path_seg1.y2),(path_seg2.x2,path_seg2.y2),-1)
    #midpoint = ((v3[0]+v4[0])/2,(v3[1]+v4[1])/2)
    #mid_seg = Segment(midpoint,(midpoint[0] + distance*cos(romo.rotation),midpoint[1] + distance*sin(romo.rotation)),-1)
    romo_front = Segment(romo.v3,romo.v4,-1)
    bounds = [bound_seg1,path_seg1,bound_seg2,path_seg2]
    #paths = [path_seg1,path_seg2,midpoint]
    box.extend(bounds)
    seg_list = []
    colliding_segs = []
    collision_points = []
    for block in block_list: #should update this outside of function!
        index = block_list.index(block)
        seg1 = Segment(block.v1,block.v2,index)
        seg2 = Segment(block.v2,block.v3,index)
        seg3 = Segment(block.v3,block.v4,index)
        seg4 = Segment(block.v4,block.v1,index)
        seg_list.extend([seg1,seg2,seg3,seg4])
        segs.extend(seg_list)
    for seg in seg_list:
        for bound in bounds:
            if seg.check_intersect(bound) and bound.closest_intersection(seg,romo) != []: #WHY is this happening...
                print("intersect at {0} {1}".format(seg,bound))
                print('{0} {1}').format(seg,bound)
                #collision_points.append(bound.closest_intersection(seg,romo))
                collision_points.extend([seg.p1,seg.p2])
            if is_in_box(seg.p1,bounds):
                collision_points.append(seg.p1)
            if is_in_box(seg.p2,bounds):
                collision_points.append(seg.p2)
                
    print(collision_points)
    if collision_points == []:
        return False
    coll = collision_points
    collision_points = []
    return romo_front.closest_to(coll)[1]
    

block1 = Block(15,15,0,5,5)
#romo = Romo(10+9*cos((20*pi)/180),5+9*sin((20*pi)/180),20,5,5)
romo = Romo(10,10,20,5,5)// If there's fewer than two items, do nothing.
  if (low < high) {
    int pivotIndex = random number from low to high;
    Comparable pivot = a[pivotIndex];
    a[pivotIndex] = a[high];                       // Swap pivot with last item
    a[high] = pivot;

    int i = low - 1;
    int j = high;
    do {
      do { i++; } while (a[i].compareTo(pivot) < 0);
      do { j--; } while ((a[j].compareTo(pivot) > 0) && (j > low));
      if (i < j) {
        swap a[i] and a[j];
      }
    } while (i < j);

    a[high] = a[i];
    a[i] = pivot;                   // Put pivot in the middle where it belongs
    quicksort(a, low, i - 1);                     // Recursively sort left list
    quicksort(a, i + 1, high);                   // Recursively sort right list
  }
}// If there's fewer than two items, do nothing.
  if (low < high) {
    int pivotIndex = random number from low to high;
    Comparable pivot = a[pivotIndex];
    a[pivotIndex] = a[high];                       // Swap pivot with last item
    a[high] = pivot;

    int i = low - 1;
    int j = high;
    do {
      do { i++; } while (a[i].compareTo(pivot) < 0);
      do { j--; } while ((a[j].compareTo(pivot) > 0) && (j > low));
      if (i < j) {
        swap a[i] and a[j];
      }
    } while (i < j);

    a[high] = a[i];
    a[i] = pivot;                   // Put pivot in the middle where it belongs
    quicksort(a, low, i - 1);                     // Recursively sort left list
    quicksort(a, i + 1, high);                   // Recursively sort right list
  }
}
block_list= [block1]
plt.show()

#doesn't work with running into vertical lines, for some reason doesn't acknowledge collisions at smaller distances.

     
import matplotlib
import matplotlib.pyplot as plt
import objects
import drawRomo as draw
import parseCommands as parse
import sys
import math
import os

num = 0
field_width = 80
field_height = 80
obj1 = objects.TargetObject(objects.Point(24, 2), 10, 8, 'red')
obj2 = objects.TargetObject(objects.Point(60, 54), 6, 6, 'yellow')
obj3 = objects.TargetObject(objects.Point(30, 15), 5, 5, 'pink')
obj4 = objects.TargetObject(objects.Point(60, 47), 3, 3, 'green')
objs = [obj1, obj2, obj3, obj4]

romo = objects.Romo(objects.Point(20, 8), 8, 12, 45)
landing_zones = [(0, 70, 10, 10, 'pink'), (70, 70, 10, 10, 'yellow'), (70, 0, 10, 10, 'red'), (0, 0, 10, 10, 'green')]

def init():
	draw_field(landing_zones, romo, objs, field_width, field_height)

def draw_field(landing_zones, romo, objs, field_width, field_height):
	figure = plt.figure()
	translate_objects = []
	for obj in objs:
		translate_objects.append((obj.bottomLeft.currX, obj.bottomLeft.currY, obj.width, obj.height, obj.color))
	draw.draw_field(figure, figure.add_subplot(111), landing_zones, (romo.bottomLeft.currX, romo.bottomLeft.currY, romo.width, romo.height, 'grey', romo.rotation - 90), field_width, field_height, translate_objects, num)
	num = num + 1

def read_instructions():
	return parse.interpretCommands(parse.parseCommands("example.txt"))

def perform_instruction(inst):
	if len(inst) == 1:
		print "Invalid instruction provided.", inst[0]
		sys.exit()
	else:
		left = inst[0]
		right = inst[1]
		time = inst[2]
	for t in range(1, int(time) + 1):
		centerX = romo.center.currX + (.5 * (left + right) * math.cos(math.radians(romo.rotation)))
		centerY = romo.center.currY + (.5 * (left + right) * math.sin(math.radians(romo.rotation)))
		romo.rotation = romo.rotation + math.degrees((1/float(romo.width)) * (right - left))
		theta = math.atan(romo.height/romo.width)
		d = romo.height/math.sin(theta)

		x = centerX - (d/2) * math.cos(math.radians(romo.rotation) + theta)
		y = centerY - (d/2) * math.sin(math.radians(romo.rotation) + theta)
		print "Before:", romo.center.currX, romo.center.currY, romo.rotation
		romo.setX(x)
		romo.setY(y)
		print "After:", romo.center.currX, romo.center.currY, romo.rotation
		print "============"
		draw_field(landing_zones, romo, objs, field_width, field_height)

def main():
	init()
	steps = read_instructions()
	for step in steps:
		perform_instruction(step)
	os.system("ffmpeg -r 10 -i romo%d.jpg -vcodec mpeg4 sim_out.mp4")
	
if __name__ == "__main__":
    main()
    

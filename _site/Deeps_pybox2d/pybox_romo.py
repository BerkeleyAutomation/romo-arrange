#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Box2D import *
from framework import *
import time
from math import *

class Romo (Framework):
  name = "Romo"
  bodies = []
  joints = []
  
  def __init__(self):
    super(Romo,self).__init__()
    self.world.gravity = (0,0)
    self.pressed = False
    ground = self.world.CreateBody(
                    shapes=b2LoopShape(vertices=[(-50,-50),(-50,50),(50,50),(50,-50)]),
                     )

    self.obstacle=self.world.CreateDynamicBody(
      position=(10,10),
      shapes=b2PolygonShape(box=(5,5)),
      )
    self.obstacle.linearDamping=20
    self.romo=self.world.CreateDynamicBody(
      position=(0,4),
      shapes=b2PolygonShape(box=(5,5)))
    self.romo.linearDamping = 20

  def Keyboard(self,key):
    if key==Keys.K_w:
      self.pressed = 'up'
    if key==Keys.K_s:
      self.pressed = 'down'
    if key==Keys.K_d:
      self.pressed = 'right'
    if key==Keys.K_a:
      self.pressed = 'left'

  def KeyboardUp(self,key):
    if key==Keys.K_w:
      self.pressed = False
      self.romo.linearVelocity = b2Vec2(0,0)
    if key==Keys.K_s:
      self.pressed = False
      self.romo.linearVelocity = b2Vec2(0,0)
    if key==Keys.K_d:
      self.pressed = False
      self.romo.angularVelocity = 0
    if key==Keys.K_a:
      self.pressed = False 
      self.romo.angularVelocity = 0

  def Step(self,settings):
    if self.pressed == 'up':
      self.romo.linearVelocity = b2Vec2(-20*cos(self.romo.angle),-20*sin(self.romo.angle))        
    if self.pressed == 'down':
      self.romo.linearVelocity = b2Vec2(20*cos(self.romo.angle),20*sin(self.romo.angle))     
    if self.pressed == 'right':
      self.romo.angularVelocity=-1
    if self.pressed == 'left':
      self.romo.angularVelocity=1
    super(Romo,self).Step(settings)

if __name__=="__main__":
     main(Romo)
        

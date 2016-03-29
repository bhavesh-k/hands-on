"""
Animation
Authors: Bhavit Patel, Bhavesh Kakwani, Tom Yang
Date Created: January 2016
Version 1

OpenGL real-time hand animation. Multi-threading with parseSerialData and pseudoMain
to run the entire HandsOn application
"""

import HandsOn
import share_var

import serial
import pygame
from pygame.locals import *

import threading

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GL.VERSION.GL_1_0 import glTranslatef
#from direct.leveleditor.AnimGlobals import FRAME
#global pitch, yaw, roll

## Draw the 3D hand based on parsed serial data
def drawBox(width,height,depth):
    vertices = (
        (width/2,-height/2,-depth/2),
        (width/2,height/2,-depth/2),
        (-width/2,height/2,-depth/2),
        (-width/2,-height/2,-depth/2),
        (width/2,-height/2,depth/2),
        (width/2,height/2,depth/2),
        (-width/2,-height/2,depth/2),
        (-width/2,height/2,depth/2)
        )

    edges = (
        (0,1),
        (0,3),
        (0,4),
        (2,1),
        (2,3),
        (2,7),
        (6,3),
        (6,4),
        (6,7),
        (5,1),
        (5,4),
        (5,7)
        )

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])

    glEnd()

def drawHand():
    # draw the 3D hand

    # clear previous rotations and reset scene
    glLoadIdentity()
    gluPerspective(90, 1, 1.0, 50.0)
    glTranslatef(0.0, 0.0, -4) # move cube away from screen (zoom out)

    # rotate using Euler angles
    glRotatef(share_var.pitch, 1, 0, 0)
    glRotatef(share_var.yaw, 0, 1, 0)
    glRotatef(share_var.roll, 0, 0, 1)
    
    # draw the palm
    drawBox(3,1,2.2)
    
    # store the current orientation for use in the next frame
    curr_pitch = share_var.pitch
    curr_yaw = share_var.yaw
    curr_roll = share_var.roll
    
    ## draw knuckles and fingers
    # index knuckle
    glTranslatef(-1.7,0,-1)
    glRotatef(-share_var.indexKnuckleDeg, 1, 0, 0)
    glTranslatef(0,0,-1.1)
    drawBox(0.6,1,2)
    glTranslatef(0,0,1.1)
    glRotatef(share_var.indexKnuckleDeg, 1, 0, 0)
    glTranslatef(1.7,0,1)
    
    return curr_pitch,curr_yaw,curr_roll
    
    

def main():
    pygame.init()
    
    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        
    # view angle, aspect ratio, z_near, z_far (z's are clipping planes)
    gluPerspective(90, 1, 1.0, 50.0)
    glTranslatef(0.0, 0.0, -4) # move cube away from screen (zoom out)
    glRotatef(0, 0, 0, 0)
    
    # Open serial port and parse serial input inside a thread
    #ser = serial.Serial('COM3', 9600) # Bhavit's PORT
    ser = serial.Serial('/dev/ttyACM0', 9600) #Bhavesh's PORT
    serialThread = threading.Thread(target=HandsOn.parseSerialHandData, args=(ser,))
    serialThread.setDaemon(True)
    serialThread.start()

    pseudoMainThread = threading.Thread(target=HandsOn.pseudoMain)
    pseudoMainThread.setDaemon(True)
    pseudoMainThread.start()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                ser.close()
                quit()
        
        # clear GL frame
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        # draw 3D hand and also update the pitch, yaw and roll
        drawHand()
        
        # refresh the frame
        pygame.display.flip()
        
        # pygame.time.wait(20) # wait 20ms
        
if __name__ == "__main__":
    main()
        

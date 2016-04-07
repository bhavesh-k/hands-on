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

def drawBox(width,height,depth,touched):
    """Draw a 3D box using provided width, height, depth and touched (boolean)"""

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

    surfaces = (
        (0,1,2,3),
        (3,2,7,6),
        (6,7,5,4),
        (4,5,1,0),
        (1,5,7,2),
        (4,0,3,6)
    )

    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            if not(touched):
                glColor3fv((1,1,1)) # white by default
            else: glColor3fv((0,0.5,1)) # blue if touched
            glVertex3fv(vertices[vertex])
    glEnd()

    # glBegin(GL_LINES)
    # for edge in edges:
    #     for vertex in edge:
    #         glColor3fv((1,1,1))
    #         glVertex3fv(vertices[vertex])
    # glEnd()

## end drawBox

def drawHand():
    """Draws the 3D hand using euler angles and finger joint angles"""

    touchThres = 2000

    # clear previous rotations and reset scene
    glLoadIdentity()
    gluPerspective(90, 1, 1.0, 50.0)
    glTranslatef(0.0, 0.0, -20) # move cube away from screen (zoom out)

    # rotate using Euler angles
    glRotatef(share_var.pitch, 1, 0, 0)
    glRotatef(share_var.yaw, 0, 1, 0)
    glRotatef(share_var.roll, 0, 0, 1)

    ## draw knuckles and fingers

    # pinky knuckle
    glTranslatef(3.0,0,-3.5)
    glRotatef(-share_var.flexPinkyFinger, 1, 0, 0)
    glTranslatef(0,0,-2.0)
    drawBox(1,1,4,share_var.touchPinkySide > touchThres)
    # pinky finger
    glTranslatef(0,0,-2.0)
    glRotatef(-share_var.flexPinkyFinger,1,0,0)
    glTranslatef(0,0,-1.5)
    drawBox(1,1,3,share_var.touchPinkyTop > touchThres)
    glTranslatef(0,0,1.5)
    glRotatef(share_var.flexPinkyFinger,1,0,0)
    glTranslatef(0,0,2.0)
    # end pinky finger
    glTranslatef(0,0,2.0)
    glRotatef(share_var.flexPinkyFinger, 1, 0, 0)
    glTranslatef(-3.0,0,3.5)
    # end pinky knuckle

    # ring knuckle
    glTranslatef(1.6,0,-3.0)
    glRotatef(-share_var.flexRingKnuckle, 1, 0, 0)
    glTranslatef(0,0,-2.5)
    drawBox(1,1,5,share_var.touchRing > touchThres)
    # ring finger
    glTranslatef(0,0,-3.5)
    glRotatef(-share_var.flexRingFinger,1,0,0)
    glTranslatef(0,0,-2.0)
    drawBox(1,1,4,False)
    glTranslatef(0,0,2.0)
    glRotatef(share_var.flexRingFinger,1,0,0)
    glTranslatef(0,0,3.5)
    # end ring finger
    glTranslatef(0,0,2.5)
    glRotatef(share_var.flexRingKnuckle, 1, 0, 0)
    glTranslatef(-1.6,0,3.0)
    # end ring knuckle

    # middle knuckle
    glTranslatef(-0.2,0,-3.5)
    glRotatef(-share_var.flexMiddleKnuckle, 1, 0, 0)
    glTranslatef(0,0,-3.0)
    drawBox(1,1,6.0,share_var.touchMidSide > touchThres)
    # middle finger
    glTranslatef(0,0,-3.5)
    glRotatef(-share_var.flexMiddleFinger,1,0,0)
    glTranslatef(0,0,-2.5)
    drawBox(1,1,5,share_var.touchMidTop > touchThres)
    glTranslatef(0,0,2.5)
    glRotatef(share_var.flexMiddleFinger,1,0,0)
    glTranslatef(0,0,3.5)
    # end middle finger
    glTranslatef(0,0,3.0)
    glRotatef(share_var.flexMiddleKnuckle, 1, 0, 0)
    glTranslatef(0.2,0,3.5)
    # end middle knuckle

    # index knuckle
    glTranslatef(-2.0,0,-3.0)
    glRotatef(-share_var.flexIndexKnuckle, 1, 0, 0)
    glTranslatef(0,0,-2.5)
    drawBox(1,1,5,share_var.touchIndSide > touchThres)
    # index finger
    glTranslatef(0,0,-3.5)
    glRotatef(-share_var.flexIndexFinger,1,0,0)
    glTranslatef(0,0,-2.0)
    drawBox(1,1,4,share_var.touchIndTop > touchThres)
    glTranslatef(0,0,2.0)
    glRotatef(share_var.flexIndexFinger,1,0,0)
    glTranslatef(0,0,3.5)
    # end index finger
    glTranslatef(0,0,2.5)
    glRotatef(share_var.flexIndexKnuckle, 1, 0, 0)
    glTranslatef(2.0,0,3.0)
    # end index knuckle

    # thumb knuckle
    glTranslatef(-3.2,0,-1.5)
    glRotatef(40,0,1,0) # rotate thumb sideways
    glRotatef(-share_var.flexThumbKnuckle, 0.3, 0, -0.1)
    glTranslatef(0,0,-2.0)
    drawBox(1,1,3.5,False)
    # thumb
    glTranslatef(0,0,-2.0)
    glRotatef(-share_var.flexThumb,1,0,0)
    glTranslatef(0,0,-1.0)
    drawBox(1,1,2,False)
    glTranslatef(0,0,1.0)
    glRotatef(share_var.flexThumb,1,0,0)
    glTranslatef(0,0,2.0)
    # end thumb
    glTranslatef(0,0,2.0)
    glRotatef(share_var.flexThumbKnuckle, 0.3, 0, -0.1)
    glRotatef(-40,0,1,0) # become parallel to palm again
    glTranslatef(3.2,0,1.5)
    # end thumb knuckle

    ## draw the palm
    drawBox(6,1,6,False)

## end drawHand

def main():
    pygame.init()

    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    # view angle, aspect ratio, z_near, z_far (z's are clipping planes)
    gluPerspective(90, 1, 1.0, 50.0)
    glTranslatef(0.0, 0.0, -20) # move cube away from screen (zoom out)
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

        # draw 3D hand
        drawHand()

        # refresh the frame
        pygame.display.flip()

## end main

if __name__ == "__main__":
    main()

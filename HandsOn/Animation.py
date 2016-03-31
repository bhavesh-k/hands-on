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

def drawBox(width,height,depth):
    """Draw a 3D box using provided width, height and depth"""

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

## end drawBox

def drawHand():
    """Draws the 3D hand using euler angles and finger joint angles"""

    # clear previous rotations and reset scene
    glLoadIdentity()
    gluPerspective(90, 1, 1.0, 50.0)
    glTranslatef(0.0, 0.0, -20) # move cube away from screen (zoom out)

    # rotate using Euler angles
    glRotatef(share_var.pitch, 1, 0, 0)
    glRotatef(share_var.yaw, 0, 1, 0)
    glRotatef(share_var.roll, 0, 0, 1)

    ## draw the palm
    drawBox(6,1,6)

    ## draw knuckles and fingers

    # thumb knuckle
    glTranslatef(-3.2,0,-1.5)
    glRotatef(80,0,1,0) # rotate thumb sideways
    glRotatef(-share_var.thumbKnuckleDeg, 1, 0, 0)
    glTranslatef(0,0,-2.0)
    drawBox(1,1,3.5)
    # thumb
    glTranslatef(0,0,-2.0)
    glRotatef(-share_var.thumbDeg,1,0,0)
    glTranslatef(0,0,-1.0)
    drawBox(1,1,2)
    glTranslatef(0,0,1.0)
    glRotatef(share_var.thumbDeg,1,0,0)
    glTranslatef(0,0,2.0)
    # end thumb
    glTranslatef(0,0,2.0)
    glRotatef(share_var.thumbKnuckleDeg, 1, 0, 0)
    glRotatef(-80,0,1,0) # become parallel to palm again
    glTranslatef(3.2,0,1.5)
    # end thumb knuckle

    # index knuckle
    glTranslatef(-2.0,0,-3.0)
    glRotatef(-share_var.indexKnuckleDeg, 1, 0, 0)
    glTranslatef(0,0,-2.5)
    drawBox(1,1,5)
    # index finger
    glTranslatef(0,0,-3.5)
    glRotatef(-share_var.indexFingerDeg,1,0,0)
    glTranslatef(0,0,-2.0)
    drawBox(1,1,4)
    glTranslatef(0,0,2.0)
    glRotatef(share_var.indexFingerDeg,1,0,0)
    glTranslatef(0,0,3.5)
    # end index finger
    glTranslatef(0,0,2.5)
    glRotatef(share_var.indexKnuckleDeg, 1, 0, 0)
    glTranslatef(2.0,0,3.0)
    # end index knuckle

    # middle knuckle
    glTranslatef(-0.2,0,-3.5)
    glRotatef(-share_var.middleKnuckleDeg, 1, 0, 0)
    glTranslatef(0,0,-3.0)
    drawBox(1,1,6.0)
    # middle finger
    glTranslatef(0,0,-3.5)
    glRotatef(-share_var.middleFingerDeg,1,0,0)
    glTranslatef(0,0,-2.5)
    drawBox(1,1,5)
    glTranslatef(0,0,2.5)
    glRotatef(share_var.middleFingerDeg,1,0,0)
    glTranslatef(0,0,3.5)
    # end middle finger
    glTranslatef(0,0,3.0)
    glRotatef(share_var.middleKnuckleDeg, 1, 0, 0)
    glTranslatef(0.2,0,3.5)
    # end middle knuckle

    # ring knuckle
    glTranslatef(1.6,0,-3.0)
    glRotatef(-share_var.ringKnuckleDeg, 1, 0, 0)
    glTranslatef(0,0,-2.5)
    drawBox(1,1,5)
    # ring finger
    glTranslatef(0,0,-3.5)
    glRotatef(-share_var.ringFingerDeg,1,0,0)
    glTranslatef(0,0,-2.0)
    drawBox(1,1,4)
    glTranslatef(0,0,2.0)
    glRotatef(share_var.ringFingerDeg,1,0,0)
    glTranslatef(0,0,3.5)
    # end ring finger
    glTranslatef(0,0,2.5)
    glRotatef(share_var.ringKnuckleDeg, 1, 0, 0)
    glTranslatef(-1.6,0,3.0)
    # end ring knuckle

    # pinky knuckle
    glTranslatef(3.0,0,-3.5)
    glRotatef(-share_var.pinkieFingerDeg, 1, 0, 0)
    glTranslatef(0,0,-2.0)
    drawBox(1,1,4)
    # pinky finger
    glTranslatef(0,0,-2.0)
    glRotatef(-share_var.pinkieFingerDeg,1,0,0)
    glTranslatef(0,0,-1.5)
    drawBox(1,1,3)
    glTranslatef(0,0,1.5)
    glRotatef(share_var.pinkieFingerDeg,1,0,0)
    glTranslatef(0,0,2.0)
    # end pinky finger
    glTranslatef(0,0,2.0)
    glRotatef(share_var.pinkieFingerDeg, 1, 0, 0)
    glTranslatef(-3.0,0,3.5)
    # end pinky knuckle

## end drawHand

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

## end main

if __name__ == "__main__":
    main()

import HandsOn
import share_var

import serial
import pygame
from pygame.locals import *

import threading

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GL.VERSION.GL_1_0 import glTranslatef
from direct.leveleditor.AnimGlobals import FRAME

#global pitch, yaw, roll

## Draw the 3D hand based on parsed serial data
def drawBox():
    vertices = (
        (1,-1,-1),
        (1,1,-1),
        (-1,1,-1),
        (-1,-1,-1),
        (1,-1,1),
        (1,1,1),
        (-1,-1,1),
        (-1,1,1)
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

def main():
    pygame.init()
    
    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        
    # view angle, aspect ratio, z_near, z_far (z's are clipping planes)
    gluPerspective(45, 1, 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5) # move cube away from screen (zoom out)
    glRotatef(0, 0, 0, 0)
    
    ser = serial.Serial('/dev/ttyACM0', 9600) #Open serial port
    serialThread = threading.Thread(target=HandsOn.parseSerialHandData, args=(ser,))
    serialThread.setDaemon(True)
    serialThread.start()
    
    curr_pitch = curr_yaw = curr_roll = 0.0 # initialize
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                ser.close()
                quit()
                
        glRotatef(share_var.pitch - curr_pitch, 1, 0, 0)
        glRotatef(share_var.yaw - curr_yaw, 0, 1, 0)
        glRotatef(share_var.roll - curr_roll, 0, 0, 1)
        
        curr_pitch = share_var.pitch
        curr_yaw = share_var.yaw
        curr_roll = share_var.roll
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) # clear GL frame
        
        drawBox()
        pygame.display.flip()
        
        # pygame.time.wait(20) # wait 20ms
        
if __name__ == "__main__":
    main()
        
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtOpenGLWidgets import QOpenGLWidget

import sys, os, time, subprocess, shutil, copy
import numpy as np
import pandas as pd

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import scipy as sp
from scipy.spatial.transform import Rotation as R

from lib.core.state.functions import bind_state

class StructureOpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Structure Preview")
        self.eye = sp.array([5.0,5.0,5.0])
        self.setMouseTracking(True)

    def mousePressEvent(self,e):
        if (e.buttons() & Qt.RightButton) or (e.buttons() & Qt.LeftButton):
            self.x0 = e.x()
            self.y0 = e.y()

    def mouseMoveEvent(self,e):
        if (e.buttons() & Qt.RightButton) or (e.buttons() & Qt.LeftButton):
            dphi = (e.x()-self.x0)*0.02
            dtheta = (e.y()-self.y0)*0.02
            if (e.buttons() & Qt.RightButton):         
                x = self.eye[0]
                y = self.eye[1]
                z = self.eye[2]
                r = (self.eye[:2]**2).sum()**0.5
                self.eye = R.from_euler('z',dphi).apply(self.eye)
                self.eye = R.from_euler('x',dtheta*y/r).apply(self.eye)
                self.eye = R.from_euler('y',dtheta*x/r).apply(self.eye)
                self.x0 = e.x()
                self.y0 = e.y()
            self.update()

    def wheelEvent(self,e):
        if e.angleDelta().y() > 0:
            self.eye *= 1/1.1
        elif e.angleDelta().y() < 0:
            self.eye *= 1.1
        print(self.eye)
        self.update()

    def initializeGL(self):
        glClearColor(0.135, 0.145, 0.175, 1.6)
        self.setCamera()

    def setCamera(self):
        display = (500,500)
        glLoadIdentity()
        gluPerspective(45, display[0]/display[1], 0.1, 50.0)
        gluLookAt(self.eye[0],self.eye[1],self.eye[2],
                  0,0,0,
                  0,0,1)

    def paintGL(self):
        self.setCamera()
        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if "entity" in self.__dict__:
            entity=self.entity
            x0 = 0
            y0 = 0
            for i in range(len(entity)):
                unit = entity.iloc[i]
                if unit['target'] in ["main","drude"]:
                    if (unit['d0']>10)*(unit['d1']>10)*(unit['d2']>10):
                        pass
                    elif unit['fname']=='block':
                        self.drawBlock(x0+unit['x'],y0+unit['y'],unit['z'],unit['d0'],unit['d1'],unit['d2'],unit['vname'],unit['v'])
                    elif unit['fname']=='disk':
                        self.drawDisk(x0+unit['x'],y0+unit['y'],unit['z'],unit['d0'],unit['d1'],unit['vname'],unit['v'])
                    elif unit['fname']=='ring':
                        self.drawRing(x0+unit['x'],y0+unit['y'],unit['z'],unit['d0'],unit['d1'],unit['d2'],unit['vname'],unit['v'])
                    else:
                        pass
            glFlush()
        else:
            pass


    def drawBlock(self, x, y, z, dx, dy, dz, vname="gray", v=0.1):


        vertices = [(x+(-0.5+int((i%2)))*dx,
                    y+(-0.5+int((i%4)/2))*dy,
                    z+(-0.5+int((i%8)/4))*dz) for i in range(8)]

        self.setColorFromV(vname, v)
        glBegin(GL_TRIANGLES)
        edges = [(0,1,2),(3,2,1),(4,5,6),(7,6,5),
                 (4,5,0),(1,0,5),(6,7,2),(3,2,7),
                 (6,4,2),(0,2,4),(7,5,3),(1,3,5)]
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

        self.setColorFromV("gray", 0.0)
        glBegin(GL_LINES)
        edges = [(0,1),(2,3),(4,5),(6,7),(0,2),(1,3),(4,6),(5,7),(0,4),(1,5),(2,6),(3,7)]
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()



    def drawDisk(self, x, y, z, r, h, vname="gray", v=0.1):
        self.setColorFromV(vname, v)

        quad = gluNewQuadric()
        gluQuadricDrawStyle(quad,GL_TRIANGLES)

        glTranslate(x, y, z-0.5*h)
        gluCylinder(quad, r,r, h, 12, 1)
        gluDisk(quad, 0,r, 24, 1)       
        glTranslate(-x, -y, -(z-0.5*h))

        glTranslate(x, y, z+0.5*h)
        gluDisk(quad, 0,r, 24, 1)       
        glTranslate(-x, -y, -(z+0.5*h))

        gluDeleteQuadric(quad)


        self.setColorFromV("gray", 0.0)
        quad = gluNewQuadric()
        gluQuadricDrawStyle(quad,GLU_LINE)

        glTranslate(x, y, z-0.5*h)
        gluDisk(quad, r,r, 24, 1)       
        glTranslate(-x, -y, -(z-0.5*h))

        glTranslate(x, y, z+0.5*h)
        gluDisk(quad, r,r, 24, 1)       
        glTranslate(-x, -y, -(z+0.5*h))

        gluDeleteQuadric(quad)



    def drawRing(self, x, y, z, r, h, w, vname="gray", v=0.1):
        self.setColorFromV(vname, v)

        quad = gluNewQuadric()
        gluQuadricDrawStyle(quad,GL_TRIANGLES)

        glTranslate(x, y, z-0.5*h)
        gluCylinder(quad, r+0.5*w, r+0.5*w, h, 24, 1)
        gluCylinder(quad, r-0.5*w, r-0.5*w, h, 24, 1)
        gluDisk(quad, r-0.5*w, r+0.5*w, 24, 1)       
        glTranslate(-x, -y, -(z-0.5*h))

        glTranslate(x, y, z+0.5*h)
        gluDisk(quad, r-0.5*w, r+0.5*w, 24, 1)       
        glTranslate(-x, -y, -(z+0.5*h))

        gluDeleteQuadric(quad)


        self.setColorFromV("gray", 0.0)
        quad = gluNewQuadric()
        gluQuadricDrawStyle(quad,GLU_LINE)

        glTranslate(x, y, z-0.5*h)
        gluDisk(quad, r-0.5*w, r-0.5*w, 24, 1)       
        gluDisk(quad, r+0.5*w, r+0.5*w, 24, 1)       
        glTranslate(-x, -y, -(z-0.5*h))

        glTranslate(x, y, z+0.5*h)
        gluDisk(quad, r-0.5*w, r-0.5*w, 24, 1)       
        gluDisk(quad, r+0.5*w, r+0.5*w, 24, 1)       
        glTranslate(-x, -y, -(z+0.5*h))

        gluDeleteQuadric(quad)

    def setColorFromV(self, vname, v):
        if vname=="metal":
            if v == 0:
                glColor3f(1.0,1.0,1.0)
            else:
                glColor3f(1.0,0.843,0)
        elif vname=="eps":
            glColor3f(0.0,float((v-1)/11.5), float((12.5-v)/11.5))
        elif vname=="gray":
            glColor3f(v,v,v)    

    def setData(self,structureTensorData):
        self.entity = structureTensorData.exportDataFrame()

    def updateFigure(self):
        self.update()

    def showData(self,structureTensorData):
        self.entity = structureTensorData.exportDataFrame()
        self.update()

    def show_structure_df(self,structure_df):
        self.entity = structure_df
        self.update()


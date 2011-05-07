import json
import simplejson as json
import sdxf
import math

dxfdir="processDXF/"
passageWidth = 5
xCells = 13;
yCells = 6;
jstr = '[[1,1,1,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,1,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]'



#cell utility class
class Cell():

    def __init__(self,x,y,passage):
        self.x = x
        self.y = y
        self.passage = passage

    def is_passage(self):
        return self.passage

    def is_neighbour_passage(self,dir):
        if dir == "LEFT": 
             if self.x > 0:
                if maze[self.x-1][self.y].is_passage():
                    return True
        if dir == "RIGHT": 
             if self.x < xCells - 1:
                if maze[self.x+1][self.y].is_passage():
                    return True
        if dir == "TOP": 
             if self.y > 0:
                if maze[self.x][self.y-1].is_passage():
                    return True
        if dir == "BOTTOM": 
             if self.y < yCells -1:
                if maze[self.x][self.y+1].is_passage():
                    return True
        return False

#functions for drawing
def endShape():
    global linePoints,drawColor
    #import pdb; pdb.set_trace()
    d.append(sdxf.LwPolyLine(points=linePoints,flag=1,color=drawColor)) 
    linePoints = []

def vertex(x,y):
    #mirror
    y = 0 - y
    #rotate; thanks http://en.wikipedia.org/wiki/Rotation_matrix#Basic_rotations
    angle = math.pi / 2
    rotX = x * math.cos(angle) - y * math.sin(angle)
    rotY = x * math.sin(angle) + y * math.cos(angle)
    x = rotX
    y = rotY
    #translate
    global transX, transY
    x = x+transX
    y = y+transY
    linePoints.append([x,y])

def drawLines(x,y, dir, lineStarted):
    if maze[x][y].passage and not maze[x][y].is_neighbour_passage(dir):
        if not lineStarted:
            #beginShape()
            lineStarted = True
            drawVertex(dir,x,y)
    else:
        drawVertex(dir,x,y)
        endShape()
        lineStarted = False

    return lineStarted

def drawVertex( dir, x,y ):
    if dir == "LEFT" : 
        vertex(x*passageWidth,y*passageWidth)
    if dir == "RIGHT" :
        vertex(x*passageWidth+passageWidth,y*passageWidth)
    if dir == "TOP":
        vertex(x*passageWidth,y*passageWidth)
    if dir == "BOTTOM":
        vertex(x*passageWidth,y*passageWidth+passageWidth)

def drawMaze():
    lineStarted = False
    for dir in range(2):
        for x in range(xCells):
            for y in range(yCells):
                lineStarted = drawLines(x,y,dirs[dir],lineStarted);

            if lineStarted:
                lineStarted = False
                drawVertex(dirs[dir],x,yCells)
                endShape()

    # top and bottom lines are missing when we hit the wall on the right
    for dir in range(2,4):
        for y in range(yCells):
            for x in range(xCells):
                lineStarted = drawLines(x,y,dirs[dir],lineStarted)

            if lineStarted:
                lineStarted = False
                drawVertex(dirs[dir],xCells,y)
                endShape()



##main start
#prep drawing
d=sdxf.Drawing()

#import the maze
matrix = json.loads( jstr )
maze = [[Cell(x,y,matrix[x][y]) for y in range(yCells)] for x in range(xCells)]

dirs = [ "LEFT", "RIGHT", "TOP", "BOTTOM" ]
linePoints = []
transX = 10
transY = 125
drawColor = 0
drawMaze()
drawColor = 3
transX = 10 + 140
transY = 125 + 100
drawMaze()
d.saveas(dxfdir+'maze.dxf')

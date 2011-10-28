# thanks to kellbot for info on the sdxf library: http://www.kellbot.com/sdxf-python-library-for-dxf/
import sdxf
import sys
from django.conf import settings
dxfdir=settings.ROOT_DIR + "mazepuzzlebox/DXF/processDXF/"

laserBurnGap = 0.16 #depends on laser cutter
"""
0.07 for smooth
0.11 for snug
0.14 for push fit
0.16 for tight fit
"""
boxWidth = 100
boxLength = 140
#if hinges don't fit in then adjust this, lower == larger
#notch needs moving slightly, lower = move notch away from the bottom.
notchCorrection = + 0.3 

cutColor = settings.CUTCOLOR

def drawRef():
    linePoints = [(-2,0),(2,0)]
    d.append(sdxf.Line(points=linePoints,color=cutColor)) 
    linePoints = [(0,-2),(0,2)]
    d.append(sdxf.Line(points=linePoints,color=cutColor))

def drawHinge(x,y):
    d.append(sdxf.Circle(center=(x+10,y+thickness * 5.5),radius=2,color=cutColor))
    d.append(sdxf.Arc(center=(x+10,y+thickness * 8 - 10),radius=10,startAngle=0,endAngle=180,color=cutColor))
    linePoints = [(x+0,y+thickness * 8 - 10 ),(x+0,y+0),(x+20,y+0),(x+20,y+thickness * 8 - 10)]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor)) 

def drawCatch(x,y):
    notchDepth = 3
    linePoints = [(x+0,y+0),(x+30,y+0),(x+30,y+thickness + laserBurnGap ),(x+20+laserBurnGap,y+thickness + laserBurnGap ),(x+20+laserBurnGap,y+thickness * 7 + laserBurnGap ),(x+10-laserBurnGap,y+thickness * 7 + laserBurnGap ),
    #notch
    (x+10-laserBurnGap,y+thickness * 6 - laserBurnGap + notchCorrection),(x+10 + notchDepth,y+ thickness * 6 - laserBurnGap + notchCorrection),(x+10 + notchDepth,y+ thickness * 5 + notchCorrection),(x+10-laserBurnGap, y+thickness * 5 +notchCorrection),
    #finish
    (x+10-laserBurnGap,y+thickness + laserBurnGap ),(x+0,y+ thickness + laserBurnGap),
    ]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor,flag=1)) 

#give x and y for top left corner of box
def drawHingeSlot(x,y):
    linePoints = [(x+boxLength,y+10),(x+boxLength-20,y+10),(x+boxLength-20,y+10+thickness),(x+boxLength,y+10+thickness)]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor)) 
    linePoints = [(x+boxLength,y+boxWidth-10),(x+boxLength-20,y+boxWidth-10),(x+boxLength-20,y+boxWidth-10-thickness),(x+boxLength,y+boxWidth-10-thickness)]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor)) 

#give x and y for top left corner of box
#slightly narrower for a tight fit
def drawHingeSlotLid(x,y):
    linePoints = [(x+boxLength,y+10+laserBurnGap),(x+boxLength-20,y+10+laserBurnGap),(x+boxLength-20,y+10+thickness-laserBurnGap),(x+boxLength,y+10+thickness-laserBurnGap)]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor)) 
    linePoints = [(x+boxLength,y+boxWidth-10-laserBurnGap),(x+boxLength-20,y+boxWidth-10-laserBurnGap),(x+boxLength-20,y+boxWidth-10-thickness+laserBurnGap),(x+boxLength,y+boxWidth-10-thickness+laserBurnGap)]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor))

def drawLidCatchSlot(x,y):
    linePoints = [(x+15-thickness/2+laserBurnGap,y+40),(x+15+thickness/2-laserBurnGap,y+40),(x+15+thickness/2-laserBurnGap,y+40+30),(x+15-thickness/2+laserBurnGap,y+40+30)]
    #d.append(sdxf.Line(points=linePoints,color=cutColor)) 
    d.append(sdxf.LwPolyLine(points=linePoints,flag=1,color=cutColor)) 

def drawLowerLidCatchSlot(x,y):
    linePoints = [(x+15-thickness/2+laserBurnGap,y+40+10),(x+15+thickness/2-laserBurnGap,y+40+10),(x+15+thickness/2-laserBurnGap,y+40+20),(x+15-thickness/2+laserBurnGap,y+40+20)]
    d.append(sdxf.LwPolyLine(points=linePoints,flag=1,color=cutColor)) 
    #d.append(sdxf.Line(points=linePoints,color=cutColor)) 

def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L
def testHoleSize( t ):
    global d,thickness
    thickness = t
    print "using thickness %f" % thickness
    d=sdxf.Drawing()
    startpoint = 0
    for i in frange(0.00,0.20 ,0.01 ):
        global laserBurnGap
        laserBurnGap = i
        print laserBurnGap
        startpoint = startpoint +10 
        drawLowerLidCatchSlot(startpoint,0)

    d.saveas(dxfdir+'pieces.dxf')

def make_pieces( t ):
    global d, thickness
    thickness = t
    print "using thickness %f" % thickness
    d=sdxf.Drawing()
    #drawRef()
    drawHinge(205,40)
    drawHinge(230,40)
    drawCatch(60,40)
    spacing = 5
    drawLidCatchSlot((boxLength+spacing)*1,(boxWidth+spacing)*3)
    drawLowerLidCatchSlot(boxLength*0,0)
    for col in range(2):
        for row in range(4):
            if (row == 3 and col == 1) or (row == 0 and col == 0):
                drawHingeSlotLid((boxLength+spacing)*col,(boxWidth+spacing)*row)
            else:
                drawHingeSlot((boxLength+spacing)*col,(boxWidth+spacing)*row)
    d.saveas(dxfdir+'pieces.dxf')

# thanks to kellbot for info on the sdxf library: http://www.kellbot.com/sdxf-python-library-for-dxf/
import sdxf
import sys
from django.conf import settings
dxfdir=settings.ROOT_DIR + "mazepuzzlebox/DXF/processDXF/"

laserBurnGap = 0.3 #depends on laser cutter
boxWidth = 100
boxLength = 140
#if hinges don't fit in then adjust this, lower == larger
lidHingeSlotReducer = 0.15
#notch needs moving slightly, lower = move notch away from the bottom.
notchCorrection = + 0.1 

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
    linePoints = [(x+0,y+0),(x+30,y+0),(x+30,y+thickness + laserBurnGap ),(x+20,y+thickness + laserBurnGap ),(x+20,y+thickness * 7 ),(x+10,y+thickness * 7 ),
    #notch
    (x+10,y+thickness * 6 - laserBurnGap + notchCorrection),(x+10 + notchDepth,y+ thickness * 6 - laserBurnGap + notchCorrection),(x+10 + notchDepth,y+ thickness * 5),(x+10, y+thickness * 5 ),
    #finish
    (x+10,y+thickness + laserBurnGap ),(x+0,y+ thickness + laserBurnGap),
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
    linePoints = [(x+boxLength,y+10+lidHingeSlotReducer),(x+boxLength-20,y+10+lidHingeSlotReducer),(x+boxLength-20,y+10+thickness-lidHingeSlotReducer),(x+boxLength,y+10+thickness-lidHingeSlotReducer)]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor)) 
    linePoints = [(x+boxLength,y+boxWidth-10-lidHingeSlotReducer),(x+boxLength-20,y+boxWidth-10-lidHingeSlotReducer),(x+boxLength-20,y+boxWidth-10-thickness+lidHingeSlotReducer),(x+boxLength,y+boxWidth-10-thickness+lidHingeSlotReducer)]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor))

def drawCatchSlot1(x,y):
    linePoints = [(x+15-thickness/2+laserBurnGap,y+40),(x+15+thickness/2-laserBurnGap,y+40),(x+15+thickness/2-laserBurnGap,y+40+30),(x+15-thickness/2+laserBurnGap,y+40+30)]
    #d.append(sdxf.Line(points=linePoints,color=cutColor)) 
    d.append(sdxf.LwPolyLine(points=linePoints,flag=1,color=cutColor)) 

def drawCatchSlot2(x,y):
    linePoints = [(x+15-thickness/2+laserBurnGap,y+40+10),(x+15+thickness/2-laserBurnGap,y+40+10),(x+15+thickness/2-laserBurnGap,y+40+20),(x+15-thickness/2+laserBurnGap,y+40+20)]
    d.append(sdxf.LwPolyLine(points=linePoints,flag=1,color=cutColor)) 
    #d.append(sdxf.Line(points=linePoints,color=cutColor)) 

def make_pieces( t ):
    global d, thickness
    thickness = t
    print "using thickness %f" % thickness
    d=sdxf.Drawing()
    #drawRef()
    drawHinge(200,40)
    drawHinge(225,40)
    drawCatch(60,40)
    drawCatchSlot1(boxLength*1,boxWidth*3)
    drawCatchSlot2(boxLength*1,0)
    for col in range(2):
        for row in range(4):
            if (row == 3 and col == 1) or (row == 0 and col == 1):
                drawHingeSlotLid(boxLength*col,boxWidth*row)
            else:
                drawHingeSlot(boxLength*col,boxWidth*row)
    d.saveas(dxfdir+'pieces.dxf')

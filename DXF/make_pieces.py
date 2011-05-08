# thanks to kellbot for info on the sdxf library: http://www.kellbot.com/sdxf-python-library-for-dxf/
import sdxf
import sys
dxfdir="processDXF/"
# globals
if len(sys.argv) != 2:
    print "give thickness on the command line"
    sys.exit(1)
thickness = float(sys.argv[1]) #3.72 #thickness of material

print "using thickness", thickness, "mm"
laserBurnGap = 0.3 #depends on laser cutter
boxWidth = 100
boxLength = 140

cutColor = 0
etchColor = 2
patternColor = 3

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
    (x+10,y+thickness * 6 - laserBurnGap),(x+10 + notchDepth,y+ thickness * 6 - laserBurnGap),(x+10 + notchDepth,y+ thickness * 5),(x+10, y+thickness * 5 ),
    #finish
    (x+10,y+thickness + laserBurnGap ),(x+0,y+ thickness + laserBurnGap),
    ]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor,flag=1)) 

#give x and y for top left corner of box
def drawHingeSlot(x,y):
    linePoints = [(x+boxLength,y+10),(x+boxLength-20,y+10),(x+boxLength-20,y+10+thickness),(x+boxLength,y+10+thickness)]
    #d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor)) 
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor,flag=1)) 
    linePoints = [(x+boxLength,y+boxWidth-10),(x+boxLength-20,y+boxWidth-10),(x+boxLength-20,y+boxWidth-10-thickness),(x+boxLength,y+boxWidth-10-thickness)]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor,flag=1)) 
#    d.append(sdxf.Line(points=linePoints,color=cutColor)) 

#give x and y for top left corner of box
#slightly narrower for a tight fit
def drawHingeSlotLid(x,y):
    linePoints = [(x+boxLength,y+10+laserBurnGap),(x+boxLength-20,y+10+laserBurnGap),(x+boxLength-20,y+10+thickness-laserBurnGap),(x+boxLength,y+10+thickness-laserBurnGap)]
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor,flag=1)) 
#    d.append(sdxf.Line(points=linePoints,color=cutColor)) 
    linePoints = [(x+boxLength,y+boxWidth-10-laserBurnGap),(x+boxLength-20,y+boxWidth-10-laserBurnGap),(x+boxLength-20,y+boxWidth-10-thickness+laserBurnGap),(x+boxLength,y+boxWidth-10-thickness+laserBurnGap)]
    #d.append(sdxf.Line(points=linePoints,color=cutColor)) #flag=1 means close the polyline
    d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor,flag=1)) #flag=1 means close the polyline

def drawCatchSlot1(x,y):
    linePoints = [(x+15-thickness/2+laserBurnGap,y+40),(x+15+thickness/2-laserBurnGap,y+40),(x+15+thickness/2-laserBurnGap,y+40+30),(x+15-thickness/2+laserBurnGap,y+40+30)]
    #d.append(sdxf.Line(points=linePoints,color=cutColor)) 
    d.append(sdxf.LwPolyLine(points=linePoints,flag=1,color=cutColor)) 

def drawCatchSlot2(x,y):
    linePoints = [(x+15-thickness/2+laserBurnGap,y+40+10),(x+15+thickness/2-laserBurnGap,y+40+10),(x+15+thickness/2-laserBurnGap,y+40+20),(x+15-thickness/2+laserBurnGap,y+40+20)]
    d.append(sdxf.LwPolyLine(points=linePoints,flag=1,color=cutColor)) 
    #d.append(sdxf.Line(points=linePoints,color=cutColor)) 

d=sdxf.Drawing()
#drawRef()
drawHinge(200,40)
drawHinge(225,40)
drawCatch(60,40)
drawCatchSlot1(boxLength*1,boxWidth*3)
drawCatchSlot2(boxLength*1,0)
for col in range(2):
    for row in range(4):
        if row == 3:
            drawHingeSlotLid(boxLength*col,boxWidth*row)
        else:
            drawHingeSlot(boxLength*col,boxWidth*row)
d.saveas(dxfdir+'boxmaze.dxf')

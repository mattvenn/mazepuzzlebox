import sdxf
cutColor=2
thickness = 4
#define the block, a Solid and an Arc

#create a new drawing
d=sdxf.Drawing()
#d.append(DXF.Circle(center=(10,10),radius=2,color=4))
#d.append(DXF.Circle(center=(20,20),radius=4,color=5))
#d.append(DXF.Arc(center=(10,thickness * 8 - 10),radius=10,startAngle=0,endAngle=180,color=cutColor))

thickness = 3.72 #thickness of material
laserBurnGap = 0.3 #depends on laser cutter
boxWidth = 100
boxLength = 140
x=0
y=0
d.append(sdxf.Circle(center=(x+10,y+thickness * 5.5),radius=2,color=cutColor))
d.append(sdxf.Arc(center=(x+10,y+thickness * 8 - 10),radius=10,startAngle=0,endAngle=180,color=cutColor))
linePoints = [(x+0,y+thickness * 8 - 10 ),(x+0,y+0),(x+20,y+0),(x+20,y+thickness * 8 - 10)]
d.append(sdxf.LwPolyLine(points=linePoints,color=cutColor)) 

#d.append(Line(points=[(0,0,0),(1,1,1)]))
d.saveas('polytest.dxf')


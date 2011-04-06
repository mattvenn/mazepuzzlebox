import sdxf
d=sdxf.Drawing()
linePoints = [(0,0),(0,10),(10,10),(10,0),(0,0)]
d.append(sdxf.LwPolyLine(points=linePoints,color=0,flag=0)) 
d.saveas('polytest.dxf')

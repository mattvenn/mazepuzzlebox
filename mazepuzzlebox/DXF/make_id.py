import ezdxf
import sys
import math
from django.conf import settings
dxfdir=settings.ROOT_DIR + "mazepuzzlebox/DXF/processDXF/"

char_width = 3
char_height = 4
char_spacing = 1
char_color = settings.PATTERNCOLOR
x_offset = 188 #183
y_offset = 230 #220
#shift routine
def shift(shift_x,shift_y,array):
    angle = - math.pi / 2
    for i in range(len(array)):
        x = array[i][0]
        y = array[i][1]
        x = x + shift_x
        y = y + shift_y
        rotX = x * math.cos(angle) - y * math.sin(angle)
        rotY = x * math.sin(angle) + y * math.cos(angle)
        array[i] = (rotX + x_offset, rotY + y_offset)

    return array

#char defs
def create_num(x,y,n):
    if n == 0:
        linePoints = [(0,0),(char_width,0),(char_width,char_height),(0,char_height),(0,0)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
    if n == 1:
        linePoints = [(0,0),(char_width,0)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
        linePoints = [(char_width/2,0),(char_width/2,char_height),(0,char_height)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
    if n == 2:
        linePoints = [(0,char_height),(char_width,char_height),(char_width,char_height/2),(0,char_height/2),(0,0),(char_width,0)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
    if n == 3:
        linePoints = [(0,char_height),(char_width,char_height),(char_width,0),(0,0)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
        linePoints = [(0,char_height/2),(char_width,char_height/2)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
    if n == 4:
        linePoints = [(0,char_height),(0,char_height/2),(char_width,char_height/2)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
        linePoints = [(char_width,char_height),(char_width,0)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
    if n == 5:
        linePoints = [(char_width,char_height),(0,char_height),(0,char_height/2),(char_width,char_height/2),(char_width,0),(0,0)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
    if n == 6:
        linePoints = [(0,char_height),(0,0),(char_width,0),(char_width,char_height/2),(0,char_height/2)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
    if n == 7:
        linePoints = [(0,char_height),(char_width,char_height),(char_width,0)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
    if n == 8:
        linePoints = [(0,0),(char_width,0),(char_width,char_height),(0,char_height),(0,0)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
        linePoints = [(0,char_height/2),(char_width,char_height/2)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})
    if n == 9:
        linePoints = [(char_width,0),(char_width,char_height),(0,char_height),(0,char_height/2),(char_width,char_height/2)]
        linePoints = shift(x,y,linePoints)
        modelspace.add_polyline2d(linePoints,dxfattribs={'color': char_color})

#do it
def make_id( id ):
    global modelspace 
    drawing = ezdxf.new(dxfversion='AC1024')
    modelspace = drawing.modelspace()
    print "using id %d" % id
    id_str = str(id)
    for i in range( len( id_str )):
        print id_str[i]
        x = i * char_width + char_spacing * i
        create_num( x, 0, int(id_str[i]) )

    drawing.saveas(dxfdir+'id_numbers.dxf')
        

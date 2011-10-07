from django.conf import settings
import drawMaze
import make_id
import make_pieces
import joinDXF
from mazepuzzlebox.createbox.models import Box
#jstr = '[[1,1,1,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,1,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]'
id = 100
thickness=4
make_pieces.make_pieces(float(thickness))
"""
DXF.drawMaze.drawMaze( box.maze,box )
DXF.make_id.make_id(box.id)
DXF.joinDXF.joinDXF(box.id)
"""

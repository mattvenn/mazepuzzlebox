from django.conf import settings
import drawMaze
import make_id
import make_pieces
import joinDXF
import Box
#from mazepuzzlebox.createbox.models import Box
#jstr = '[[1,1,1,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,1,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]'
id = 37
thickness=3.76
#make_pieces.testHoleSize(thickness)
box = Box.objects.get(pk=id)
drawMaze.drawMaze( box.maze,box )
#DXF.make_id.make_id(box.id)
#DXF.joinDXF.joinDXF(box.id)

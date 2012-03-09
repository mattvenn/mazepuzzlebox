from django.conf import settings
import drawMaze
import make_id
import make_pieces
import joinDXF
import drawMazeSVG
#import Box
from mazepuzzlebox.createbox.models import Box
#jstr = '[[1,1,1,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,1,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]'
id = 37
thickness=3.76
try:
    box = Box.objects.get(pk=id)
except:
    print "first instantiate failed... why?"
    box = Box.objects.get(pk=id)
drawMazeSVG.drawMaze( box.maze, box )
drawMaze.drawMaze( box.maze,box )
make_pieces.make_pieces(thickness)
make_id.make_id(box.id)
joinDXF.joinDXF(box.id)

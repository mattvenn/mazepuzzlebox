from django.conf import settings
import drawMaze
"""
import make_mazeSVG
import make_piecesSVG
import drawInstructionsMaze
import buildInstructions
import make_idSVG
"""
import make_id
import make_pieces
import ezjoinDXF
#import Box
from mazepuzzlebox.createbox.models import Box
id = 40
thickness=3.72
try:
    box = Box.objects.get(pk=id)
except:
    print "first instantiate failed... why?"
    box = Box.objects.get(pk=id)

#the (not so?) awful DXFs - switched to ezdxf
drawMaze.drawMaze( box.maze,box )
make_pieces.make_pieces(thickness)
make_id.make_id(box.id)
ezjoinDXF.joinDXF(box.id)

#the instructions as an SVG
"""
drawInstructionsMaze.drawMaze( box.maze, box )
buildInstructions.buildInstructions(box.id)

#SVG version, hopefully better!
make_piecesSVG.make_pieces(thickness)
make_mazeSVG.make_maze(box.maze,box)
make_idSVG.make_id(box.id)
buildInstructions.buildBox(box.id)
"""

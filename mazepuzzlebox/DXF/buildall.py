from django.conf import settings
import drawMaze
import make_mazeSVG
import make_id
import make_pieces
import make_piecesSVG
import joinDXF
import drawInstructionsMaze
import buildInstructions
import make_idSVG
#import Box
from mazepuzzlebox.createbox.models import Box
id = 37
thickness=3.76
try:
    box = Box.objects.get(pk=id)
except:
    print "first instantiate failed... why?"
    box = Box.objects.get(pk=id)

#the awful DXFs
drawMaze.drawMaze( box.maze,box )
make_pieces.make_pieces(thickness)
make_id.make_id(box.id)
joinDXF.joinDXF(box.id)

#the instructions as an SVG
drawInstructionsMaze.drawMaze( box.maze, box )
buildInstructions.buildInstructions(box.id)

#SVG version, hopefully better!
make_piecesSVG.make_pieces(thickness)
make_mazeSVG.make_maze(box.maze,box)
make_idSVG.make_id(box.id)
buildInstructions.buildBox(box.id)

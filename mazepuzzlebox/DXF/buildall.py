import drawMaze
import make_pieces
import make_id
import joinDXF

jstr = '[[1,1,1,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,1,1],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,1,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]'
drawMaze.drawMaze( jstr )
make_pieces.make_pieces(4)
make_id.make_id(401)
joinDXF.joinDXF(100)

"""
draws the maze for the website
"""
from PIL import Image, ImageDraw
import json
import simplejson as json
from django.conf import settings

#TODO
xCells = 13
yCells = 6


def drawMaze( jstr, id ):
    
    cellWidth = 20
    startCell = (0, 0, cellWidth,cellWidth)
    endCell = ( (xCells-3) * cellWidth,1 * cellWidth, (xCells-3) * cellWidth + cellWidth, 1 * cellWidth + cellWidth )

    img = Image.new( "RGB", (cellWidth * xCells,cellWidth*yCells))
    draw = ImageDraw.Draw(img)

    maze = json.loads( jstr )
    for x in range(0,xCells):
        for y in range(0,yCells):
            if maze[x][y]:
                draw.rectangle([(x*cellWidth,y*cellWidth),(x*cellWidth+cellWidth,y*cellWidth+cellWidth)],(128,128,128))
    
    #draw starting circle
    draw.ellipse( startCell, fill =( 255,0,0 ))
    #draw ending square
    draw.rectangle( endCell, fill = (255,0,0 ))
    path = settings.ROOT_DIR + "mazePNGs/"
    img_path = path + str(id) + ".png"
    img.save(img_path)


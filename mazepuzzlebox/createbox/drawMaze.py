"""
draws the maze for the website
"""
from PIL import Image
import ImageDraw
import json
import simplejson as json

xCells = 13
yCells = 6

def checkJSON(jstr):
    try:
        maze = json.loads( jstr )
    except:
        raise Exception( "bad json string" )
    try:
        if len( maze ) != xCells:
            raise Exception( "wrong number of columns in json array" )
        for i in range( xCells ):
            if len( maze[i] ) != yCells:
                raise Exception( "wrong number of rows in json array" )
    except:
        raise Exception( "json doesn't represent an array" )

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
    path = "/home/matthew/work/python/mazepuzzlebox/mazePNGs/"
    img_path = path + str(id) + ".png"
    img.save(img_path)


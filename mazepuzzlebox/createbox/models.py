from django.db import models
import json
import simplejson as json

#TODO
xCells = 13
yCells = 6

startX = 2
startY = 4
endX = 12
endY = 5
noGoStartX = 4
noGoStartY = 2
noGoEndX = 9
noGoEndY = 6
# Create your models here.
class Box(models.Model):
    pub_date = models.DateTimeField('date published')
    maze = models.CharField(max_length=400)

    #we want the maze in columns of rows not rows of columns
    def htmlMaze(self):
        maze = json.loads( self.maze )
        #initalize new array
        outmaze = [[ 0 for x in range(xCells)]for y in range(yCells)]
        for x in range(xCells):
            for y in range(yCells):
                if x > noGoStartX and x < noGoEndX and y > noGoStartY and y < noGoEndY:
                    outmaze[y][x] = 'no-go'
                if maze[x][y]:
                    outmaze[y][x] = 'gone'
                if x == startX and y == startY:
                    outmaze[y][x] = 'start'
                if x == endX and y == endY:
                    outmaze[y][x] = 'end'
                
        return outmaze

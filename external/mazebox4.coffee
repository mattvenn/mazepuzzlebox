class MazeDesigner
    constructor: (maze, breakableCells, allCells) ->
        
        @directions = ['up', 'down', 'left', 'right']
        @pathStatus = $('#path-status')
        @islandStatus = $('#island-status')
        @deltas =
            up: [0,1]
            down: [0,-1]
            left: [-1,0]
            right: [1,0]
        
        @action = false
        @grid = null

        # Make the maze unselectable
        maze.attr('unselectable', 'on')
            .css('MozUserSelect', 'none')
            .bind 'selectstart.ui', -> return false
        
        ###
        Events
        ###
        $(document).mouseup =>
            if @action
                path = false 
                islands = false
                @grid = @gridGen allCells
                if @checkPath()
                    path = true
                    @setStatus('path', 'good')
                else
                    @setStatus('path', 'bad')
                
                if @checkIslands()
                    @setStatus('island', 'bad')
                else
                    @setStatus('island', 'good')
                    islands = true

                if path and islands
                    json = @makeJson @grid
                    $('#json').text(json)
                    document.createmaze.mazejson.value = json
                    document.createmaze.mazebutton.disabled = false
                else
                    document.createmaze.mazebutton.disabled = true

            @action = false
                

        breakableCells.mousedown (e) =>
            cell = $(e.target)
            if cell.hasClass('gone')
                @action = 'restoring'
            else
                @action = 'breaking'

            @update cell
            @setStatus('path', 'thinking')
            @setStatus('island', 'thinking')

        breakableCells.mouseenter (e) =>
            cell = $(e.target)
            if @action
                @update cell
    
    makeJson: (grid) ->
        json = grid
        for row, y in grid
            for cell, x in row
                if cell is 'X' then json[y][x] = 0
                if cell is 'E' or cell is 'S' then json[y][x] = 1
        
        json = ((row[i] for row in json) for i in [0...json[0].length])

        return JSON.stringify(json)

    setStatus: (type, status) ->
        if type is 'path'
            @pathStatus.attr('class', status)
        else if type is 'island'
            @islandStatus.attr('class', status)

    hasTuple: (list, tuple) ->
        for [x,y] in list
            if tuple[0]==x and tuple[1]==y then return true
        return false

    gridGen: (cells) ->
        grid = [[],[],[],[],[],[]]
        cells.each (i, el) =>
            cell = $(el)
            [x, y] = @coords(cell)
            #if x == 15 then console.log(cell.attr('class'))
            switch cell.attr('class')
                when undefined then s = 0
                when '' then s = 0
                when 'gone' then s = 1
                #deal with multi classes in a bad way!
                when 'gone no-go' then s = 1
                when 'no-go' then s = 'X'
                when 'start' then s = 'S'
                when 'end' then s = 'E'

            grid[y][x] = s

        return grid

    update: (cell) ->
        if @action is 'restoring' and cell.hasClass('gone')
            cell.removeClass('gone')
        else if @action is 'breaking' and not cell.hasClass('gone')
            cell.addClass('gone')

    gridVal: (x, y) ->
        @grid[y][x]

    coords: (cell) ->
        [cell.index(), cell.parent().index()]

    withinMaze: (x, y) ->
        #changed for bigger maze
        16 > x >= 0 and 6 > y >= 0

    checkPath: ->
        @visited = []
        #changed the start point 
        return @hunt([15,5], 1, 'E')
    
    checkIslands: ->
        @visited = []

        for row, y in @grid
            for cell, x in row
                if cell is 0 and not @hasTuple(@visited, [x,y])
                    if @hunt([x,y], 0, 'X')
                    else return true
        # If no islands have been found, return false        
        return false



    hunt: (start, follow, target) ->
        @queue = [start]
        foundit = false
        while @queue.length > 0
            new_queue = []
            for [xb, yb] in @queue
                for direction in @directions
                    [xd,yd] = @deltas[direction]
                    [x,y] = [xb+xd, yb+yd]

                    continue if @hasTuple(@visited, [x,y])

                    if not @withinMaze(x,y)
                        cellType = 'X'
                    else
                        cellType = @gridVal(x,y)
                        @visited.push([x,y])

                    if cellType is follow
                        new_queue.push([x,y])
                    else if cellType is target
                        foundit = true
            @queue = new_queue
        return foundit

$ ->
    breakableCells = $('#maze td:not(.no-go, .start, .end)')
    allCells = $('#maze td')
    maze = $('#maze')

    mazeDesigner = new MazeDesigner(maze, breakableCells, allCells)

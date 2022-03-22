import random


def generateMaze(height, width):
    wall = 0
    path = 1
    unvisited = 'x'
    maze = []
    walls = []

    def printMaze(maze):
        maze_str = ""
        for i in range(0, height):
            for j in range(0, width):
                maze_str += str(maze[i][j])
                maze_str += " "
            maze_str += '\n'
        return maze_str

    def surroundingPathCells(cell):
        # Find number of surrounding path cells
        surrounding_path_cells_num = 0
        neighbours = []
        neighbours = setNeighbours(cell[0], cell[1])
        for neighbour in neighbours:
            if maze[neighbour[0]][neighbour[1]] == path:
                surrounding_path_cells_num += 1

        return surrounding_path_cells_num

    def countCellNeighbours(cell_height, cell_width):
        neighbour_num = 4
        if cell_width == 0 or cell_width == width-1:
            neighbour_num -= 1
        if cell_height == 0 or cell_height == height-1:
            neighbour_num -= 1
        return neighbour_num

    def setNeighbours(cell_height, cell_width):
        neighbours = []

        def update_neighbours(count, first_value_to_add, second_value_to_add):
            for i in range(count):
                neighbours.append(
                    (cell_height+first_value_to_add[i], cell_width+second_value_to_add[i]))

        if cell_width == 0 and cell_height == 0:
            update_neighbours(2, (0, 1), (1, 0))
        elif cell_width == 0 and cell_height == height-1:
            update_neighbours(2, (0, -1), (1, 0))
        elif cell_width == width-1 and cell_height == 0:
            update_neighbours(2, (0, -1), (-1, 0))
        elif cell_width == width-1 and cell_height == height-1:
            update_neighbours(2, (0, 1), (-1, 0))
        elif cell_width == 0:
            update_neighbours(3, (1, -1, 0), (0, 0, 1))
        elif cell_height == 0:
            update_neighbours(3, (0, 0, 1), (-1, 1, 0))
        elif cell_width == width-1:
            update_neighbours(3, (1, -1, 0), (0, 0, -1))
        elif cell_height == height-1:
            update_neighbours(3, (0, 0, -1), (-1, 1, 0))
        else:
            update_neighbours(4, (-1, 1, 0, 0), (0, 0, -1, 1))

        if countCellNeighbours(cell_height, cell_width) != len(neighbours):
            print("[ERROR]: wrong neighbours number")

        return neighbours

    def initMaze(height, width):
        for i in range(0, height):
            line = []
            for j in range(0, width):
                line.append(unvisited)
            maze.append(line)

    def cellIntoWall(rand_wall, val_added_to_x, val_added_to_y):
        if (maze[rand_wall[0]+val_added_to_x][rand_wall[1]+val_added_to_y] != path):
            maze[rand_wall[0]+val_added_to_x][rand_wall[1]+val_added_to_y] = wall
        if ([rand_wall[0]+val_added_to_x, rand_wall[1]+val_added_to_y] not in walls):
            walls.append([rand_wall[0]+val_added_to_x,
                         rand_wall[1]+val_added_to_y])

    def upperCellIntoWall(rand_wall):
        if (rand_wall[0] != 0):
            cellIntoWall(rand_wall, -1, 0)

    def bottomCellIntoWall(rand_wall):
        if (rand_wall[0] != height-1):
            cellIntoWall(rand_wall, 1, 0)

    def leftmostCellIntoWall(rand_wall):
        if (rand_wall[1] != 0):
            cellIntoWall(rand_wall, 0, -1)

    def rightmostCellIntoWall(rand_wall):
        if (rand_wall[1] != width-1):
            cellIntoWall(rand_wall, 0, 1)

    def deleteWall(rand_wall):
        # Delete the wall from the list
        for w in walls:
            if (w[0] == rand_wall[0] and w[1] == rand_wall[1]):
                walls.remove(w)

    def setEntranceAndExit():
        for i in range(0, width):
            if (maze[1][i] == path):
                maze[0][i] = 'I'
                break

        for i in range(width-1, 0, -1):
            if (maze[height-2][i] == path):
                maze[height-1][i] = 'O'
                break

    def unvisitedCellsToWalls():
        for i in range(0, height):
            for j in range(0, width):
                if (maze[i][j] == unvisited):
                    maze[i][j] = wall

    initMaze(height, width)

    # Random starting cell
    starting_cell = (random.randint(1, height-1), random.randint(1, width-1))
    maze[starting_cell[0]][starting_cell[1]] = path

    walls = setNeighbours(starting_cell[0], starting_cell[1])
    for w in walls:
        maze[w[0]][w[1]] = wall

    while (walls):
        # Pick a random wall
        rand_wall = walls[random.randint(0, len(walls)-1)]

        def CellsIntoWalls(rand_wall, not_wall_cell):
            if not_wall_cell != 'u':
                upperCellIntoWall(rand_wall)
            if not_wall_cell != 'b':
                bottomCellIntoWall(rand_wall)
            if not_wall_cell != 'l':
                leftmostCellIntoWall(rand_wall)
            if not_wall_cell != 'r':
                rightmostCellIntoWall(rand_wall)

        def CreatePath(rand_wall, values_to_add, not_wall_cell):
            if (maze[rand_wall[0]+values_to_add[0][0]][rand_wall[1]+values_to_add[0][1]] == unvisited and maze[rand_wall[0]+values_to_add[1][0]][rand_wall[1]+values_to_add[1][1]] == path):

                path_cell_neighbours_num = surroundingPathCells(rand_wall)
                if (path_cell_neighbours_num < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = path

                    CellsIntoWalls(rand_wall, not_wall_cell)

                deleteWall(rand_wall)

        if rand_wall[1] != 0 and rand_wall[1] != width-1:
            # It isn't a left wall of a maze
            CreatePath(rand_wall, ((0, -1), (0, 1)), 'r')
            # [unvisited][rand wall][path]

        if (rand_wall[0] != 0 and rand_wall[0] != height-1):
            # It isn't upper wall
            CreatePath(rand_wall, ((-1, 0), (1, 0)), 'b')

        # Check the bottom wall
        if (rand_wall[0] != height-1):
            CreatePath(rand_wall, ((1, 0), (-1, 0)), 'u')

        # Check the right wall
        if (rand_wall[1] != width-1):
            CreatePath(rand_wall, ((0, 1), (0, -1)), 'l')

        deleteWall(rand_wall)

    unvisitedCellsToWalls()
    setEntranceAndExit()
    return printMaze(maze)

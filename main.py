import pygame
import random

# Define colors
BLACK = (0,     0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (0,   255,   0)
BLUE  = (0,     0, 255)

TILELENGTH = 20
WINDOWLENGTH = 1000
NUM_SQUARES = int(WINDOWLENGTH / TILELENGTH)

# Functions to calculate if neighbour is turned on (Value of 1)
# If index is out of range or value of neighbour is 0, return 0
# If neighbour has a value of 1, return 1
def upValue(row, col):
    try:
        if (grid[row][col-1] == 1): return 1
        else: return 0
    except IndexError:
        return 0
def downValue(row, col):
    try:
        if grid[row][col+1] == 1: return 1
        else: return 0
    except IndexError:
        return 0
def leftValue(row, col):
    try:
        if grid[row-1][col] == 1: return 1
        else: return 0
    except IndexError:
        return 0
def rightValue(row, col):
    try:
        if grid[row+1][col] == 1: return 1
        else: return 0
    except IndexError:
        return 0
def leftUpValue(row, col):
    try:
        if grid[row-1][col-1] == 1: return 1
        else: return 0
    except IndexError:
        return 0
def rightUpValue(row, col):
    try:
        if grid[row+1][col-1] == 1: return 1
        else: return 0
    except IndexError:
        return 0
def leftDownValue (row, col):
    try:
        if grid[row-1][col+1] == 1: return 1
        else: return 0
    except IndexError:
        return 0
def rightDownValue(row, col):
    try:
        if grid[row+1][col+1] == 1: return 1
        else: return 0
    except IndexError:
        return 0

# Function to calculate updated grid
# Calculates neighbours population for each tile
# Returns the updated grid to be displayed
def calculateNewGrid(grid):
    newgrid = []
    for row in range(len(grid)): 
        newgrid.append([])
        for column in range(len(grid)):
            newgrid[row].append(0)

    for row in range(len(grid)): 
        for col in range(len(grid)):

            population = leftUpValue(row,col) + upValue(row,col) + rightUpValue(row,col) + \
                         leftValue(row,col) +                        rightValue(row,col) + \
                         leftDownValue(row,col) +downValue(row,col) + rightDownValue(row,col) 
            
            # Conway's Game of Life Rules:
            # 1. Any live cell with two or three neighbors survives.
            # 2. Any dead cell with three live neighbors becomes a live cell.
            # 3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.
            if population < 2 or population > 3:
                newgrid[row][col] = 0
            elif population == 3:
                newgrid[row][col] = 1
            else:
                newgrid[row][col] = grid[row][col]
    return newgrid

# Create a 2 dimensional array
grid = []
for row in range(NUM_SQUARES): 
    grid.append([])
    for column in range(NUM_SQUARES):
        rand = random.randint(0,10)
        if rand > 3:
            grid[row].append(0)
        else:
            grid[row].append(1)
 
# Initialize pygame
# Set the HEIGHT and WIDTH of the screen
# Set title of screen
pygame.init()
screen = pygame.display.set_mode([WINDOWLENGTH, WINDOWLENGTH])
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# Loop until the user clicks the close button.
done = False
runSimulation = True

# Function to color in boxes while the mouse is pressed down
def drawBoxes():
    draw = True
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0] == True:
        print(cur)
        xTileIndex = int(cur[1] / TILELENGTH)
        yTileIndex = int(cur[0] / TILELENGTH)
        grid[xTileIndex][yTileIndex] = 1

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            runSimulation = False # If mouse button is down, stop simulating
        if event.type == pygame.MOUSEBUTTONUP:
            runSimulation = True # If mouse button is up, start simulating

    screen.fill(WHITE)
 
    # Draw the grid
    for row in range(NUM_SQUARES): 
        for column in range(NUM_SQUARES): 
            if grid[row][column] == 1:
                square = pygame.Rect(TILELENGTH * column, TILELENGTH * row, TILELENGTH, TILELENGTH)
                pygame.draw.rect(screen, BLACK, square)
            else:
                square = pygame.Rect(TILELENGTH * column, TILELENGTH * row, TILELENGTH, TILELENGTH)
                pygame.draw.rect(screen, WHITE, square)

    pygame.display.flip()
    # If true, calculate new grid and limit clock to 25
    if runSimulation:
        grid = calculateNewGrid(grid)
        clock.tick(25)
    # If false, let user use mouse to make tiles active and increase clock to 120 to reduce input lag
    else:
        drawBoxes()
        clock.tick(120)

pygame.quit()
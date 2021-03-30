import pygame
import random
import timeit
import os 
from numba import jit
import numpy as np

# Define colors
BLACK = (0,     0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (0,   255,   0)
BLUE  = (0,     0, 255)

BACKGROUND_COLOR = BLACK
TILE_COLOR = WHITE

TILE_LENGTH = 8
NUM_X_SQUARES = 100
NUM_Y_SQUARES = 185
INIT_FILLED = 5 # 0-11, 0 means no filled tiled at beginning, 11 means all tiles are filled at beginning

# Function to calculate updated grid
# Calculates neighbours population for each tile
# Returns the updated grid to be displayed
@jit(nopython=True)
def calculateNewGrid(grid):
    newgrid = np.zeros((NUM_X_SQUARES, NUM_Y_SQUARES))

    for row in range(NUM_X_SQUARES): 
        for col in range(NUM_Y_SQUARES):

            population = grid[(row-1)%NUM_X_SQUARES][(col-1)%NUM_Y_SQUARES]     + grid[row][(col-1)%NUM_Y_SQUARES] +    grid[(row+1)%NUM_X_SQUARES][(col-1)%NUM_Y_SQUARES] + \
                         grid[(row-1)%NUM_X_SQUARES][col] +                                                             grid[(row+1)%NUM_X_SQUARES][col] + \
                         grid[(row-1)%NUM_X_SQUARES][(col+1)%NUM_Y_SQUARES]     + grid[row][(col+1)%NUM_Y_SQUARES] +    grid[(row+1)%NUM_X_SQUARES][(col+1)%NUM_Y_SQUARES]
            
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

# Function to color in boxes while the mouse is pressed down
def drawBoxes():
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0] == True:
        xTileIndex = int(pos[1] / TILE_LENGTH)
        yTileIndex = int(pos[0] / TILE_LENGTH)
        grid[xTileIndex][yTileIndex] = 1

if __name__ == "__main__":     
    # Initialize random 2D array
    grid = np.zeros((NUM_X_SQUARES, NUM_Y_SQUARES))
    for row in range(NUM_X_SQUARES): 
        for column in range(NUM_Y_SQUARES):
            rand = random.randint(0,10)
            if rand < INIT_FILLED:
                grid[row][column] = 1
    
    # Initialize pygame
    # Set the HEIGHT and WIDTH of the screen
    # Set title of screen
    pygame.init()
    screen = pygame.display.set_mode([NUM_Y_SQUARES * TILE_LENGTH, NUM_X_SQUARES * TILE_LENGTH])
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()

    # Loop until the user clicks the close button.
    done = False
    drawing = False

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True # If mouse button is down, stop simulating
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False # If mouse button is up, start simulating

        screen.fill(BACKGROUND_COLOR)
    
        start_time = timeit.default_timer()

        # Draw the grid
        for row in range(NUM_X_SQUARES): 
            for column in range(NUM_Y_SQUARES): 
                if grid[row][column] == 1:
                    square = pygame.Rect(TILE_LENGTH * column, TILE_LENGTH * row, TILE_LENGTH, TILE_LENGTH)
                    pygame.draw.rect(screen, TILE_COLOR, square)
                else:
                    square = pygame.Rect(TILE_LENGTH * column, TILE_LENGTH * row, TILE_LENGTH, TILE_LENGTH)
                    pygame.draw.rect(screen, BACKGROUND_COLOR, square)

        pygame.display.flip()

        # Calculate new grid
        if not(drawing):
            os.system('cls')
            grid = calculateNewGrid(grid)
            print("Time between updates: ", timeit.default_timer() - start_time)
            clock.tick(40)
        # Let user use mouse to make tiles active
        else:
            drawBoxes()

    pygame.quit()
import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
TILELENGTH = 25
MARGIN = 2
WINDOWLENGTH = 675
 
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range((WINDOWLENGTH // TILELENGTH) * (1 + MARGIN)): 
    grid.append([])
    for column in range((WINDOWLENGTH // TILELENGTH) * (1 + MARGIN)):
        grid[row].append([random.randint(0,1)])
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
screen = pygame.display.set_mode([WINDOWLENGTH, WINDOWLENGTH])
 
# Set title of screen
pygame.display.set_caption("Conway's Game of Life")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
mouseDown = False

def calculateAliveAround(grid, x, y):
    #return (grid[y][x])
    pass

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
    
    if mouseDown:
        pos = pygame.mouse.get_pos()
        column = pos[0] // (TILELENGTH + MARGIN)
        row = pos[1] // (TILELENGTH + MARGIN)
        # Set that location to one
        grid[row][column] = 1
        print("Click ", pos, "Grid coordinates: ", row, column)
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    for row in range(WINDOWLENGTH // TILELENGTH):
        for column in range(WINDOWLENGTH // TILELENGTH):
            color = WHITE
            if grid[row][column] == 1:
                color = BLACK
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + TILELENGTH) * column + MARGIN,
                              (MARGIN + TILELENGTH) * row + MARGIN,
                              TILELENGTH,
                              TILELENGTH])
            
            print(calculateAliveAround(grid, row, column))

    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
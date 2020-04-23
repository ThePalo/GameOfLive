import pygame
import numpy as np
import time

# Initialize the pygame library
pygame.init()

# Variables
width = 1000
height = 1000
pauseGame = False

#Num cells
nCx = 60
nCy = 60
#Dim cells
dimCx = width/nCx
dimCy = height/nCy

#State cells, live = 1, dead = 0
gameState = np.zeros((nCx, nCy))

# Set up the drawing window
screen = pygame.display.set_mode([width + 1, height + 1])

# Run until the user asks to quit
running = True
while running:

    #new gamestate
    new_gameState = np.copy(gameState)

    # Fill the background with white
    screen.fill((0, 0, 0))
    time.sleep(0.1)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pauseGame = not pauseGame
        if event.type == pygame.MOUSEBUTTONDOWN:  
            # left button --> live cell
            if event.button == 1:
                x,y = event.pos
                x, y = int(np.floor(x/dimCx)), int(np.floor(y/dimCy))
                new_gameState[x,y] = 1
            # right button --> dead cell
            elif event.button == 3:
                x,y = event.pos
                x, y = int(np.floor(x/dimCx)), int(np.floor(y/dimCy))
                new_gameState[x,y] = 0
                print(x, y)

    for y in range(0, nCx):
        for x in range(0, nCy):
            if not pauseGame:
                #Compute neightbors
                n_neigh = gameState[(x-1)   % nCx, (y-1)    % nCy] + \
                          gameState[(x)     % nCx, (y-1)    % nCy] + \
                          gameState[(x+1)   % nCx, (y-1)    % nCy] + \
                          gameState[(x-1)   % nCx, (y)      % nCy] + \
                          gameState[(x+1)   % nCx, (y)      % nCy] + \
                          gameState[(x-1)   % nCx, (y+1)    % nCy] + \
                          gameState[(x)     % nCx, (y+1)    % nCy] + \
                          gameState[(x+1)   % nCx, (y+1)    % nCy]
                
                #Rule 1
                if gameState[x,y] == 0 and n_neigh == 3:
                    new_gameState[x,y] = 1
                
                #Rule 2
                if gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    new_gameState[x,y] = 0

            #Draw gird
            poly = [(x       * dimCx, y     * dimCy),
                    ((x+1)   * dimCx, y     * dimCy),
                    ((x+1)   * dimCx, (y+1) * dimCy),
                    (x       * dimCx, (y+1) * dimCy)]
            if new_gameState[x,y] == 0:
                pygame.draw.polygon(screen, (128,128,128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255,255,255), poly, 0)

    #Update game state
    gameState = np.copy(new_gameState)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
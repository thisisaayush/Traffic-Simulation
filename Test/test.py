import pygame

# initialize pygame
pygame.init()

# create size of a display window.
screen = pygame.display.set_mode((900, 725))

pygame.display.set_caption("Highway Image")

# load the image
map_image = pygame.image.load("highway_image.png")

# run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # clear the screen
    screen.fill((255, 255, 255))

    # render the map
    screen.blit(map_image, (0, 0))

    # update the display
    pygame.display.update()

# quit pygame
pygame.quit()

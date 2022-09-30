import pygame
import random
import math

pygame.init()
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
COLOR = WHITE  # Current color

# Width, Height
size = (1200, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("2D Game")
screen.fill(BLACK)

random.seed(pygame.time.Clock())


class Toucan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.toucan = [pygame.image.load('toucan_0.png'), pygame.image.load('toucan_1.png'),
                       pygame.image.load('toucan_2.png'), pygame.image.load('toucan_3.png')]
        self.curr_frame = 0
        self.image = self.toucan[self.curr_frame]
        self.rect = self.image.get_rect()
        self.x = 100
        self.y = 100
        self.rect.topleft = [self.x, self.y]

    # Updates each frame for sprite
    def update(self):
        pygame.draw.rect(screen, BLACK,
                         [self.rect.topleft[0], self.rect.topleft[1], self.rect.bottomright[0] - self.rect.topleft[0],
                          self.rect.bottomright[1] - self.rect.topleft[
                              1]])  # Clear the old sprite from the page without clearing the whole page
        self.curr_frame += 1  # Increment sprite frame
        self.curr_frame %= 4  # Makes sure curr_frame doesn't go out of arr bounds
        self.image = self.toucan[self.curr_frame]
        self.x += 10
        if self.x > 1150:
            self.x = 0
            self.y = random.randint(10, 750)
        self.rect.topleft = [self.x, self.y]


sprites = pygame.sprite.Group()  # Create group for sprites
toucan = Toucan()  # Create toucan object
sprites.add(toucan)  # Add toucan to sprite group
sprites.draw(screen)  # Draw sprite
pygame.display.flip()  # Update screen


def draw_house():
    # ----------------------------- [x,   y,   width,height], border_radius
    pygame.draw.rect(screen, COLOR, [200, 300, 500, 400], 0)

    # Triangle roof
    for i in range(250):
        pygame.draw.line(screen, COLOR, [200 + i, 300 - i], [700 - i, 300 - i], 3)

    pygame.draw.aaline(screen, BLACK, [200, 300], [700, 300], blend=3)  # Line under roof
    pygame.draw.rect(screen, BLACK, [450, 500, 200, 200], 0)  # Door
    pygame.draw.rect(screen, BLACK, [280, 500, 100, 100], 0)  # Window rect
    pygame.draw.line(screen, COLOR, [330, 500], [330, 600], 3)  # Window vertical line
    pygame.draw.line(screen, COLOR, [280, 550], [380, 550], 3)  # Window horizontal line
    pygame.draw.line(screen, COLOR, [550, 500], [550, 700], 3)  # Line between doors
    pygame.draw.circle(screen, COLOR, [540, 610], 5)  # Left door knob
    pygame.draw.circle(screen, COLOR, [560, 610], 5)  # Right door knob
    pygame.display.flip()  # Update screen


# Displays text on screen
font = pygame.font.Font('freesansbold.ttf', 32)  # Font of text
text = font.render('Ritik Kadyan', True, GREEN, BLACK)  # Text to display with color green and black background
textRect = text.get_rect()  # Text rectangle
textRect.center = (600 // 2, 100 // 2)  # Center text
screen.blit(text, textRect)  # Add text to screen

# Draw an ellipse
pygame.draw.ellipse(screen, RED, ((150, 200), (150, 100)), 0)  # Inside ellipse
pygame.draw.ellipse(screen, BLUE, ((150, 200), (150, 100)), 5)  # Outline ellipse

pygame.draw.arc(screen, GREEN, [400, 400, 300, 25], 0, 5, width=1)  # Draw an arc

clock = pygame.time.Clock()
keepGoing = True
mode = 'rect'
while keepGoing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False  # Stop the while loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 'line':
                lineStart = pygame.mouse.get_pos()
            elif mode == 'rect':
                rect_corner_one = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if mode == 'line':
                lineEnd = pygame.mouse.get_pos()
                pygame.draw.line(screen, COLOR, lineStart, lineEnd, 3)  # Draw a line when user mouse bottom went up
            elif mode == 'rect':
                rect_corner_two = pygame.mouse.get_pos()

                # If corner one on left side
                if rect_corner_one[0] < rect_corner_two[0]:
                    # Top left to bottom right
                    if rect_corner_one[1] < rect_corner_two[1]:
                        rect_top_left = rect_corner_one
                        rect_bottom_right = rect_corner_two
                    else:  # corner 1 below
                        # Bottom left to top right
                        rect_top_left = [rect_corner_one[0], rect_corner_two[1]]
                        rect_bottom_right = [rect_corner_two[0], rect_corner_one[1]]
                else:
                    # Top right to bottom left
                    if rect_corner_one[1] < rect_corner_two[1]:
                        rect_top_left = [rect_corner_two[0], rect_corner_one[1]]
                        rect_bottom_right = [rect_corner_one[0], rect_corner_two[1]]
                    else:
                        # Bottom right to top left
                        rect_top_left, rect_bottom_right = rect_corner_two, rect_corner_one

                # Width and height of rectangle
                width = abs(rect_top_left[0] - rect_bottom_right[0])
                height = abs(rect_top_left[1] - rect_bottom_right[1])

                pygame.draw.rect(screen, COLOR, [rect_top_left[0], rect_top_left[1], width, height], 0)
        elif event.type == pygame.MOUSEMOTION:  # If mouse moves get mouse position
            lineEnd = pygame.mouse.get_pos()
        elif event.type == pygame.KEYDOWN:  # If user pressed key
            if event.key == pygame.K_r:
                # Set color to red
                COLOR = RED
            elif event.key == pygame.K_c:
                # Clear the screen
                screen.fill(BLACK)
                pygame.display.flip()
            elif event.key == pygame.K_h:
                # Draw a house
                draw_house()
            elif event.key == pygame.K_w:
                # Set color to white
                COLOR = WHITE
            elif event.key == pygame.K_g:
                # Set color to green
                COLOR = GREEN
            elif event.key == pygame.K_b:
                # Set color to blue
                COLOR = BLUE
            elif event.key == pygame.K_q:
                # Stops the while loop
                keepGoing = False
            elif event.key == pygame.K_l:
                # Switch shape mode to line
                mode = 'line'
            elif event.key == pygame.K_s:
                # Switch shape mode to rectangle
                mode = 'rect'

    # Update sprite
    sprites.update()
    # Redraw sprite
    sprites.draw(screen)
    # Refresh display
    pygame.display.flip()
    # 30fps
    clock.tick(30)

pygame.quit()

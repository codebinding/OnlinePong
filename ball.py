import pygame
from random import randint
BLACK = (0,0,0)
 
class PygameBall(pygame.sprite.Sprite):
    #This class represents a ball. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, x, y, width, height, velocity):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the ball (a rectangle!)
        self.color = color
        self.width = width
        self.height = height
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.velocity = velocity
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)

class SimpleBall:
    def __init__(self, pygame_ball):
        self.x = pygame_ball.rect.x
        self.y = pygame_ball.rect.y
        self.width = pygame_ball.width
        self.height = pygame_ball.height
        self.velocity = pygame_ball.velocity
        self.color = pygame_ball.color

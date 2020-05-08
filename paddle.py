import pygame
BLACK = (0,0,0)
 
class PygamePaddle(pygame.sprite.Sprite):
    #This class represents a paddle. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, x, y, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the paddle, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the paddle (a rectangle!)
        self.color = color
        self.width = width
        self.height = height
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Define the velocity of the paddle
        self.velocity = 5

    def moveUp(self):
        self.rect.y -= self.velocity
		#Check that you are not going too far (off the screen)
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self):
        self.rect.y += self.velocity
	    #Check that you are not going too far (off the screen)
        if self.rect.y > 400:
          self.rect.y = 400

class SimplePaddle:
    def __init__(self, pygame_paddle):
        self.x = pygame_paddle.rect.x
        self.y = pygame_paddle.rect.y
        self.width = pygame_paddle.width
        self.height = pygame_paddle.height
        self.velocity = pygame_paddle.velocity
        self.color = pygame_paddle.color

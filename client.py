import pygame
from network import ClientNetwork
from paddle import PygamePaddle
from ball import PygameBall

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()

# Set the initial state of both paddles and the ball
ball = 0
scores = [0, 0]

try:
    client_network = ClientNetwork()
    m, s, b = client_network.connect()
    me = PygamePaddle(m.color, m.x, m.y, m.width, m.height)
    h, s, b = client_network.send(me)
    he = PygamePaddle(h.color, h.x, h.y, h.width, h.height)
    ball = PygameBall(b.color, b.x, b.y, b.width, b.height, b.velocity)
    scores[0] = s[0]
    scores[1] = s[1]
except:
    client_network.close()
    print('Failed to connect server!')
    pygame.quit()
    exit(1)

def main():
    global me, he, ball

    # Open a new window
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong")

    #This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()
    
    # Add the paddles to the list of sprites
    all_sprites_list.add(me)
    all_sprites_list.add(he)
    all_sprites_list.add(ball)

    # The loop will carry on until the user exit the game (e.g. clicks the close button).
    carry_on = True

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    while carry_on:

        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carry_on = False # Flag that we are done so we exit this loop
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                    carry_on=False  
        
        #Moving the paddles when the user uses the arrow keys (player A) or "W/S" keys (player B) 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            me.moveUp()
        if keys[pygame.K_DOWN]:
            me.moveDown()

        h, s, b = client_network.send(me)
        he.rect.x = h.x
        he.rect.y = h.y
        ball.rect.x = b.x
        ball.rect.y = b.y
        ball.velocity = b.velocity
        scores[0] = s[0]
        scores[1] = s[1]

        # --- Game logic should go here
        #all_sprites_list.update()
        
        # --- Drawing code should go here
        # First, clear the screen to black. 
        screen.fill(BLACK)
        #Draw the net
        pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
        
        #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen) 
    
        #Display scores:
        font = pygame.font.Font(None, 74)
        text = font.render(str(scores[0]), 1, WHITE)
        screen.blit(text, (250,10))
        text = font.render(str(scores[1]), 1, WHITE)
        screen.blit(text, (420,10))

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        # --- Limit to 60 frames per second
        clock.tick(60)

    pygame.quit()

main()
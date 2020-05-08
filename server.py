import socket
import threading
import pickle
import pygame
from random import randint
from paddle import PygamePaddle
from ball import PygameBall
from network import ServerNetwork

LINE_WIDTH = 80
column = 0

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED =(255, 0, 0)
BLUE = (0, 0, 255)

# Initailize the socket
try:
    server_network = ServerNetwork()
    print('Server started, waiting for a connection ...')
except:
    print('Failed to start server!')
    exit(1)

pygame.init()

# Set the initial state of both paddles and the ball
paddles = [PygamePaddle(RED, 20, 200, 10, 100), PygamePaddle(BLUE, 670, 200, 10, 100)]
ball = PygameBall(WHITE, 345, 195, 10,10, [randint(4,8),randint(-8,8)])
scores = [0, 0]
player_list = []

# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
# Add the paddles to the list of sprites
all_sprites_list.add(paddles[0])
all_sprites_list.add(paddles[1])
all_sprites_list.add(ball)

def threaded_client(conn, player):
    global column
    player_list.append(player)
    
    try:
        server_network.send(conn, paddles[player], scores, ball)   # paddle, scores, ball

        while True:
            p = server_network.recv(conn)     # paddle

            if not p:
                print("\nDisconnected")
                break
            else:
                paddles[player].rect.x = p.x
                paddles[player].rect.y = p.y
                print('<', end='')
                column += 1
                server_network.send(conn, paddles[1-player], scores, ball)

            print('>', end='')
            column += 1

            if column >= LINE_WIDTH:
                column = 0
                print()
    except:
        print("Lost connection")
    
    player_list.remove(player)
    conn.close()

def main():
    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    while True:
        # Waiting for both players to join
        if len(player_list) != 2:
            conn, address = server_network.accept()
            print('Connected to: ', address)
            if not 0 in player_list:
                player = 0
            else:
                player = 1
            scores[0] = 0
            scores[1] = 0
            threading.Thread(target=threaded_client, args=(conn, player)).start()

        # Game started
        # --- Game logic should go here
        all_sprites_list.update()

        #Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x>=690:
            scores[0]+=1
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x<=0:
            scores[1]+=1
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y>490:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y<0:
            ball.velocity[1] = -ball.velocity[1] 

        #Detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(ball, paddles[0]) or pygame.sprite.collide_mask(ball, paddles[1]):
            ball.bounce()

        # --- Limit to 60 frames per second
        clock.tick(60)

    pygame.quit()

main()
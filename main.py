#Import the pygame library and initialise the game engine
import pygame
#Let's import the Paddle Class & the Ball Class
from paddle import Paddle
from ball import Ball
from brick import Brick
 

def build_bricks(sprites, bricks):
    colors = [MAROON, PINK, PURPLE, BLUE, MINT, GREEN, ORANGE, YELLOW]
    coord = 40
    for color in colors:
        for i in range(7):
            brick = Brick(color,80,30)
            brick.rect.y = coord
            brick.rect.x = 60 + i* 100
            sprites.add(brick)
            bricks.add(brick)
        coord +=35


pygame.init()
 
# Define some colors
WHITE = (255,255,255)
LIGHTBLUE = (0,176,240)
PINK = (235,97,214)
ORANGE = (250,178,62)
YELLOW = (251,253,116)
MAROON = (223, 48, 151)
PURPLE = (126, 79, 226)
GREEN = (34, 212, 31)
BLUE = (13, 90, 215)
MINT = (22, 216, 207)

# Define dimensions
WIDTH = 800
HEIGHT = 600

score = 0
lives = 5
level = 1
speed = 30
paddle_speed = 10

# Sound effects and background music
effect_lose_life = pygame.mixer.Sound('media/lose_life.wav')
effect_gameover = pygame.mixer.Sound('media/gameover.wav')
effect_next_level = pygame.mixer.Sound('media/next_level.wav')
effect_win = pygame.mixer.Sound('media/win.mp3')
effect_pock = pygame.mixer.Sound('media/pock.wav')
effect_success = pygame.mixer.Sound('media/success.wav')

# Background
background = pygame.image.load("media/space.jpg")
 
# Open a new window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
#Create the Paddle
paddle = Paddle(LIGHTBLUE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560
 
#Create the ball sprite
ball = Ball(WHITE,10,10)
ball.rect.x = WIDTH/2
ball.rect.y = HEIGHT/2
 
all_bricks = pygame.sprite.Group()
build_bricks(all_sprites_list, all_bricks)
 
# Add paddle and ball to the list of sprites
all_sprites_list.add(paddle)
all_sprites_list.add(ball)
 
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            while True: #Infinite loop that will be broken when the user press the space bar again
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    break #Exit infinite loop
 
    #Moving the paddle when the use uses the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(paddle_speed)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(paddle_speed)
 
    # --- Game logic should go here
    all_sprites_list.update()
 
    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>590:
        ball.rect.center = (WIDTH / 2, HEIGHT / 2)
        ball.velocity[0] = -ball.velocity[0]
        lives -= 1
        effect_lose_life.play()
        if lives == 0:
            #Display Game Over Message for 8 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (250,300))
            effect_gameover.play()
            pygame.display.flip()
            pygame.time.wait(8000)
            pygame.quit()
 
    # Bounce off the horizontal line
    if ball.rect.y<40:
        ball.velocity[1] = -ball.velocity[1]
 
    # Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddle):
      effect_pock.play()
      ball.rect.x -= ball.velocity[0]
      ball.rect.y -= ball.velocity[1]
      ball.bounce()
 
    # Check if there is the ball collides with any of bricks
    brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
    for brick in brick_collision_list:
      effect_success.play() 
      ball.bounce()
      score += 100
      brick.kill()
      if len(all_bricks)==0:
           # Display Level Complete Message for 3 seconds
            if level<3:
                font = pygame.font.Font(None, 74)
                text = font.render("LEVEL COMPLETE", 1, WHITE)
                screen.blit(text, (200,300))
                pygame.display.flip()
                effect_next_level.play()
                pygame.time.wait(3000)
                level +=1
                speed +=15
                paddle_speed +=5
                build_bricks(all_sprites_list, all_bricks)
            else:
                font = pygame.font.Font(None, 74)
                text = font.render("YOU WON!", 1, WHITE)
                screen.blit(text, (200,300))
                pygame.display.flip()
                effect_win.play()
                pygame.time.wait(8000)
                carryOn=False

    # Drawing code go here
    # Add background and horizontal line
    screen.blit(pygame.transform.scale(background, (800, 600)), (0, 0))    
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)
 
    # Display the score, the number of lives and hint for pausing the game at the top of the screen
    font = pygame.font.Font(None, 34)
    text = font.render("Score: " + str(score), 1, WHITE)
    screen.blit(text, (20,10))
    text = font.render("Level: " + str(level), 1, WHITE)
    text_rect = text.get_rect(center=(400, 22))
    screen.blit(text, text_rect)
    text = font.render("Lives: " + str(lives), 1, WHITE)
    screen.blit(text, (650,10))
    font = pygame.font.Font(None, 26)
    text = font.render("Press spacebar to pause", 1, YELLOW)
    text_rect = text.get_rect(center=(400, 580))
    screen.blit(text, text_rect)
 
    # Now let's draw all the sprites in one go
    all_sprites_list.draw(screen)
 
    # Update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(speed)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()

import pygame
import os
pygame.font.init()
pygame.mixer.init()

"""
https://github.com/techwithtim/PygameForBeginners.git
I took a lot of inspiration from Tech with Tim and his youtube channel. The link above is from his github that I used as
a massive inspiration for my project. I created the same game and watched the whole tutorial to gain a better understanding
of Pygame.
"""


# create title. Set window size define borders
width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Battle!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

window = pygame.Rect(width//2 - 5, 0, 10, height)

# I added thee into the code but I didn't like how often you could hear the sounds especially when
# testing in public so I commented them out
#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')


# set game font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# set the game running speed or FPS
FPS = 60
# set player movement speed
VEL = 5
# set bullet speed and bullet limit
BULLET_VEL = 7
MAX_BULLETS = 3
# define size of the ships
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# load ship images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# load the background from assets
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (width, height))

def main():
    # director function everything is run from here
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 5
    yellow_health = 5

    clock = pygame.time.Clock()
    run = True

    # main game play loop    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


            # this part of the code lets the yellow space ship shoot a bullet at the red spaceship
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()


                # this part does the same for the red spaceship towards the yellow one
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

            # when player gets hit lower player health
            if event.type == RED_HIT:
                red_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                #BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        elif yellow_health <= 0:
            winner_text = "Red Wins!"
        else:
            winner_text = "The game is a draw"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # this is to handle all player movements
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        # this is to handle all bullets fired by either player
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # this will redraw the window every time something changes and the screen needs to be updated
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # this function is used to display all updates that happen in the visuals up to 60 time a second
    # 60 FPS
    win.blit(SPACE, (0, 0))
    pygame.draw.rect(win, BLACK, window)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    win.blit(red_health_text, (width - red_health_text.get_width() - 10, 10))
    win.blit(yellow_health_text, (10, 10))

    win.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    win.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(win, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(win, YELLOW, bullet)

    # since this function is called in a loop this last line lets all changes actually be displayed
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # yellow move left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < window.x:  # yellow move right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # yellow move up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < height - 15:  # yellow move down
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > window.x + window.width:  # red move left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < width:  # red move right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # red move up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < height - 15:  # red move down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # this function ensures that once the bullets have either collided with a ship or the wall at the edge
    # of the screen that they are removed from the visuals and any information is also updated.
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > width:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    # this function displays the winner of the game through a text that appears on the screen and then resets
    # the game to play again
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    win.blit(draw_text, (width/2 - draw_text.get_width() /2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

main()

if __name__ == "__main__":
    main()

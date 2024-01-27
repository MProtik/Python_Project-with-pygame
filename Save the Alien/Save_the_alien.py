import pygame
import sys
import os
import time
import random
import json

pygame.init()
pygame.font.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()

WIDTH, HEIGHT = info.current_w, info.current_h

# player variable
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 90
PLAYER_VAL = 7

# star variable
STAR_WIDTH = 20
STAR_HEIGHT = 100
STAR_VAL = 5.5

WIN = pygame.display.set_mode((WIDTH, HEIGHT - 80))
pygame.display.set_caption('Save The Alien')
pygame.display.set_icon(pygame.image.load('Save the Alien\\img\\Bye.jpg'))

# Player creation
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load('Save the Alien\\img\\SpaceShip.png'),
                                     (PLAYER_WIDTH, PLAYER_HEIGHT))
player = pygame.Rect((WIDTH / 2 - PLAYER_WIDTH / 2 - 230, (HEIGHT - PLAYER_HEIGHT) - 200, 40, 50))
# Background image
BG = pygame.transform.scale(pygame.image.load('Save the Alien\\img\\BG.jpg'), (WIDTH, HEIGHT))
INTRO = pygame.transform.scale(pygame.image.load('Save the Alien\\img\\Bye.jpg'), (WIDTH, HEIGHT))

# Font
FONT = pygame.font.SysFont("comicsans", 30)
NAME_FONT = pygame.font.SysFont("comicsans", 40)

# scores from a JSON file
FILE = 'high_scores.json'
if os.path.exists(FILE):
    with open(FILE, 'r') as f:
        high_scores = json.load(f)
else:
    high_scores = []


def animation():
    l = []
    for i in range(1, 20):
        if i + 1 == 4:
            continue
        l.append(pygame.transform.scale(pygame.image.load(f'Save the Alien\\PNG fireball\\{i + 1}.png'),
                                        (STAR_WIDTH, STAR_HEIGHT)))
    return l


# Sequence of images to make animation
fireball = animation()


def draw(elapse_time, stars, bg_y):
    WIN.blit(BG, (0, bg_y))
    WIN.blit(BG, (0, bg_y - HEIGHT))

    time_text = FONT.render(f"Time: {round(elapse_time)}s", 1, 'white')
    WIN.blit(time_text, (WIDTH - 150, 10))
    WIN.blit(PLAYER_IMAGE, player)

    for star in stars:
        WIN.blit(random.choice(fireball), star)

    pygame.display.update()


def intro_screen():
    intro_font = pygame.font.SysFont("comicsans", 50)
    intro_font = pygame.font.SysFont("comicsans", 50)
    name_font = pygame.font.SysFont("Boulder", 40)
    name_text = intro_font.render("Help the Alien to go to his home planet", 1, 'blue')
    intro_text = intro_font.render("Press any key to start", 1, 'black')
    devoloper_name = name_font.render("Developed by Protik", 1, 'black')
    WIN.blit(INTRO, (0, 0))
    WIN.blit(name_text, (WIDTH / 2 - name_text.get_width() / 2, (HEIGHT / 2 - name_text.get_height() / 2) - 100))
    WIN.blit(intro_text, (WIDTH / 2 - intro_text.get_width() / 2, HEIGHT / 2 - intro_text.get_height() / 2))
    WIN.blit(devoloper_name, (WIDTH - 300, HEIGHT - 150))
    pygame.display.update()

    wait_for_key()


def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                break


def input_name():
    input_font = pygame.font.SysFont("comicsans", 50)
    input_text = input_font.render("Enter your name:", 1, 'white')
    #WIN.blit(BG, (0, 0))  
    WIN.fill((0, 0, 200))  # Clear the windows and making it white
    WIN.blit(input_text, (WIDTH / 2 - input_text.get_width() / 2, HEIGHT / 2 - input_text.get_height() / 2))
    pygame.display.update()

    name = ""
    clivking = True
    while clivking:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    clivking = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

                #to display the letters while typing
                WIN.fill((0, 0, 200))
                updated_text = input_font.render(f"Enter your name: {name}", 1, 'white')
                WIN.blit(updated_text, (WIDTH / 2 - updated_text.get_width() / 2, HEIGHT / 2 - updated_text.get_height() / 2))
                pygame.display.update()                   


    return name


def display_scores():
    high_scores.sort(key=lambda x: x['score'], reverse=True)
    top_scores = high_scores[:10]

    scores_font = pygame.font.SysFont("comicsans", 30)
    scores = scores_font.render("Here is the Top Scores...", 1, 'white')
    WIN.blit(BG, (0, 0))  # Clear the screen
    WIN.blit(scores, ((WIDTH / 2 - scores.get_width())-50 / 2, 100-40))

    y_position = 100
    for idx, score in enumerate(top_scores, start=1):
        score_text = scores_font.render(f"{idx}. {score['name']}: {score['score']}", 1, 'white')
        WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, y_position))
        y_position += 40

    pygame.display.update()
    pygame.time.delay(2000)  # Display the scores for 5 seconds
    #the delay is too much. i might lower it a bit later

#file function (json)
def save_scores(name, score):
    high_scores.append({'name': name, 'score': score})
    high_scores.sort(key=lambda x: x['score'], reverse=True) # I will change the function

    # Save top 10 scores to the JSON file
    with open(FILE, 'w') as f:
        json.dump(high_scores[:10], f)


def confirm_screen():
    confirm_font = pygame.font.SysFont("comicsans", 40)
    confirm_text = confirm_font.render("Do you want to play again? (Y/N)", 1, 'white')
    WIN.blit(confirm_text, (WIDTH / 2 - confirm_text.get_width() / 2, (HEIGHT / 2 - confirm_text.get_height() / 2) + 100))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False


def main():
    name = ""
    while True:
        intro_screen()

        clock = pygame.time.Clock()
        start_time = time.time()
        elapse_time = 0

        star_add_increment = 2000
        star_count = 0

        stars = []
        hit = False
        bg_y = 0

        run = True
        while run:
            star_count += clock.tick(60)
            elapse_time = time.time() - start_time

            if star_count > star_add_increment:
                for _ in range(random.randint(1, 4)):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT - (random.randint(0, 100)), STAR_WIDTH - 10, STAR_HEIGHT - 15)
                    stars.append(star)
                    
                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VAL >= 0:
                player.x -= PLAYER_VAL
            elif keys[pygame.K_RIGHT] and player.x + PLAYER_VAL + player.width <= WIDTH:
                player.x += PLAYER_VAL
            elif keys[pygame.K_UP] and player.y - PLAYER_VAL >= 0:
                player.y -= PLAYER_VAL
            elif keys[pygame.K_DOWN] and player.y + player.height <= HEIGHT - 10:
                player.y += PLAYER_VAL

            bg_y += 1
            if bg_y >= HEIGHT:
                bg_y = 0

            for star in stars[:]:
                star.y += STAR_VAL
                if star.y > HEIGHT:
                    stars.remove(star)
                elif star.y + star.height >= player.y and star.colliderect(player):
                    stars.remove(star)
                    hit = True
                    break

            if hit:
                player_name = input_name()
                save_scores(player_name, round(elapse_time))

                display_scores()

                play_again = confirm_screen()
                if play_again:
                    main()
                else:
                    pygame.quit()
                    sys.exit()
                    

            draw(elapse_time, stars, bg_y)

        pygame.quit()


if __name__ == '__main__':
    main()

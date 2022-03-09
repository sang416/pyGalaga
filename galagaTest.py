import pygame
import random
from time import sleep

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
pad_width = 480
pad_height = 640
fight_width = 36
fight_height = 38
enemy_width = 26
enemy_height = 20
highscore = 0


def init_game():
    global gamepad, fighter, clock
    global bullet, enemy

    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption("MyGalaga")
    fighter = pygame.image.load("fighter.png")
    enemy = pygame.image.load("enemy.png")
    bullet = pygame.image.load("bullet.png")
    clock = pygame.time.Clock()


def gameover():
    global gamepad
    dispmessage("Game Over")


def playsound(filename):
    fire_sound = pygame.mixer.Sound(filename)
    fire_sound.play()


def drawscore(count):
    global gamepad
    font = pygame.font.SysFont('arial', 20)
    text = font.render("Score : " + str(count), True, WHITE)
    gamepad.blit(text, (5, 5))


def drawhighscore(score):
    global gamepad
    font = pygame.font.SysFont('arial', 20)
    text = font.render("High Score : " + str(score), True, RED)
    gamepad.blit(text, (300, 5))


def dispmessage(text):
    global gamepad
    textfont = pygame.font.SysFont("stencil", 50)
    text = textfont.render(text, True, RED)
    textpos = text.get_rect()
    textpos.center = (pad_width / 2, pad_height / 2)
    gamepad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    run_game()


def crash():
    global gamepad
    dispmessage("Game Over")


def drawobject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))


def run_game():
    global gamepad, fighter, clock
    global bullet, enemy, highscore

    isShot = False
    shotcount = 0
    enemypassed = 0

    fighter_x = pad_width * 0.45
    fighter_y = pad_height * 0.9
    x_change = 0

    bullet_xy = []
    enemy_x = random.randrange(0, pad_width - enemy_width)
    enemy_y = 0
    enemy_speed = 3

    ongame = False
    while not ongame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongame = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change -= 5

                elif event.key == pygame.K_RIGHT:
                    x_change += 5

                elif event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                    playsound("fighter_fire.ogg")
                    if len(bullet_xy) < 4:
                        bullet_x = fighter_x + fight_width / 2
                        bullet_y = fighter_y - fight_height
                        bullet_xy.append([bullet_x, bullet_y])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        gamepad.fill(BLACK)

        fighter_x += x_change
        if fighter_x < 0:
            fighter_x = 0
        elif fighter_x > pad_width - fight_width:
            fighter_x = pad_width - fight_width

        if fighter_y < enemy_y + enemy_height:
            if (enemy_x > fighter_x and enemy_x < fighter_x + fight_width) or (
                enemy_x + enemy_width > fighter_x
                and enemy_x + enemy_width < fighter_x + fight_width):
                playsound("explosion.ogg")
                if highscore < shotcount:
                    highscore = shotcount
                crash()

        drawobject(fighter, fighter_x, fighter_y)

        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[1] -= 10
                bullet_xy[i][1] = bxy[1]

                if bxy[1] < enemy_y:
                    if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width:
                        bullet_xy.remove(bxy)
                        playsound("enemy_hit.ogg")
                        isShot = True
                        shotcount += 100

                if bxy[1] <= 0:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawobject(bullet, bx, by)

        drawscore(shotcount)
        drawhighscore(highscore)

        enemy_y += enemy_speed
        if enemy_y > pad_height:
            enemy_x = random.randrange(0, pad_width - enemy_width)
            enemy_y = 0
            enemypassed += 1

        if isShot:
            enemy_speed += 1
            if enemy_speed >= 10:
                enemy_speed = 10

            enemy_x = random.randrange(0, pad_width - enemy_width)
            enemy_y = 0
            isShot = False

        drawobject(enemy, enemy_x, enemy_y)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    init_game()
    run_game()

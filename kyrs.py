import pygame
from random import randrange
import pygame_menu


# основные настройки

RES = 800


img1 = pygame.image.load('formenu.png')
pygame.init()
screen = pygame.display.set_mode([RES, RES])
timer = pygame.time.Clock()
font_score = pygame.font.SysFont('Verdana.ttf', 36, bold=True)
font_end = pygame.font.SysFont('Verdana.ttf', 66, bold=True)
img = pygame.image.load('forbackground.jpg.').convert()


# закрытие игры


def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


# игра

def start_the_game():
    # основные настройки
    RES = 800
    SIZE = 50

    x, y = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    length = 1
    snake = [(x, y)]
    dx, dy = 0, 0
    fps = 55
    dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
    total = 0
    speed_count = 0
    snake_speed = 10

    while True:
        screen.blit(img, (0, 0))

        # отрисовка змеи и яблок

        [pygame.draw.rect(screen, pygame.Color('purple'), (i, j, SIZE - 1, SIZE - 1)) for i, j in snake]
        pygame.draw.rect(screen, pygame.Color('green'), (*apple, SIZE, SIZE))

        # отрисовка очков

        render_score = font_score.render(f'TOTAL: {total}', 1, pygame.Color('white'))
        screen.blit(render_score, (5, 5))

        # движение змеи

        speed_count += 1
        if not speed_count % snake_speed:
            x += dx * SIZE
            y += dy * SIZE
            snake.append((x, y))
            snake = snake[-length:]

        # поедание еды

        if snake[-1] == apple:
            apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
            length += 1
            total += 1
            snake_speed -= 1
            snake_speed = max(snake_speed, 4)

        # конец игры

        if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
            while True:
                render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
                screen.blit(render_end, (RES // 2 - 200, RES // 3))
                pygame.display.flip()
                close_game()

        pygame.display.flip()
        timer.tick(fps)
        close_game()

        # управление

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            if dirs['W']:
                dx, dy = 0, -1
                dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
        elif key[pygame.K_s]:
            if dirs['S']:
                dx, dy = 0, 1
                dirs = {'W': False, 'S': True, 'A': True, 'D': True, }
        elif key[pygame.K_a]:
            if dirs['A']:
                dx, dy = -1, 0
                dirs = {'W': True, 'S': True, 'A': True, 'D': False, }
        elif key[pygame.K_d]:
            if dirs['D']:
                dx, dy = 1, 0
                dirs = {'W': True, 'S': True, 'A': False, 'D': True, }

    pass


menu = pygame_menu.Menu('', 300, 150,
                       theme=pygame_menu.themes.THEME_BLUE)


menu.add.text_input('Name :', default='Your Name')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)



while True:

    screen.blit(img1, (0,0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()

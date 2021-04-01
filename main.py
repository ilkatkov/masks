import pygame
import math
import random
import time
import pygame.mixer
from tkinter import *
from tkinter import messagebox as mb

pygame.init()

# создаем невидимое окно tkinter
Tk().wm_withdraw()


class Object(pygame.sprite.Sprite):
    def __init__(self, img, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed


width = 800
height = 600

# игровое окно
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Маски!")
pygame.display.set_icon(pygame.image.load("nuclear.ico"))

pygame.mixer.music.load("sounds/main.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

mb.showinfo("Маски!", "Во время COVID-19 необходимо пользоваться средствами индивидуальной защиты органов дыхания. Надень людям маски, чтобы предотвратить пандемию!")

# текст
score_font = pygame.font.Font(None, 35)
score_text = score_font.render("Маски: 0", True, pygame.Color("yellow"))
lives_font = pygame.font.Font(None, 30)
lives_text = lives_font.render("Жизни: 3", True, pygame.Color("yellow"))

bg = pygame.transform.scale(
    pygame.image.load("images/bg.png"), (width, height))

player_img = pygame.transform.scale(
    pygame.image.load("images/player.png"), (64, 64))
boy = pygame.transform.scale(pygame.image.load("images/npc_boy.png"), (32, 32))
boy_mask = pygame.transform.scale(
    pygame.image.load("images/npc_boy_mask.png"), (32, 32))
girl = pygame.transform.scale(
    pygame.image.load("images/npc_girl.png"), (32, 32))
girl_mask = pygame.transform.scale(
    pygame.image.load("images/npc_girl_mask.png"), (32, 32))
explorergirl = pygame.transform.scale(
    pygame.image.load("images/npc_explorergirl.png"), (32, 32))
explorergirl_mask = pygame.transform.scale(
    pygame.image.load("images/npc_explorergirl_mask.png"), (32, 32))
darkguy = pygame.transform.scale(
    pygame.image.load("images/npc_darkguy.png"), (32, 32))
darkguy_mask = pygame.transform.scale(
    pygame.image.load("images/npc_darkguy_mask.png"), (32, 32))
oldman = pygame.transform.scale(
    pygame.image.load("images/npc_oldman.png"), (32, 32))
oldman_mask = pygame.transform.scale(
    pygame.image.load("images/npc_oldman_mask.png"), (32, 32))
guy = pygame.transform.scale(
    pygame.image.load("images/npc_guy.png"), (32, 32))
guy_mask = pygame.transform.scale(
    pygame.image.load("images/npc_guy_mask.png"), (32, 32))

# группы спрайтов
all_sprites = pygame.sprite.Group()
humans = pygame.sprite.Group()

# создание объектов
player = Object(player_img, 0, 0, 0)
correction_angle = 90  # т.к. нос корабля смотрит вверх
all_sprites.add(player)

create_time = 1.5  # время появления жителей
start_time = time.time()  # начало времени
lives = 3  # жизни
score = 0  # баллы
run = True  # флаг игры

while run:

    window.blit(bg, (0, 0))

    # выходим из игры при проигрыше
    if lives <= 0:
        mb.showerror("Маски!", "Вы проиграли :(\nВаш счет: " + str(score))
        run = False

    # кнопка выхода
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # поворот игрока
    player_pos = window.get_rect().center
    player_rect = player.image.get_rect(center=player_pos)

    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - player_rect.centerx, my - player_rect.centery
    angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

    rot_image = pygame.transform.rotate(player_img, angle)
    rot_image_rect = rot_image.get_rect(center=player_rect.center)
    player.image = rot_image
    player.rect = rot_image_rect

    # появление жителей
    if create_time > 0.5:
        create_time -= 0.0001
    step_time = time.time()
    if step_time - start_time > create_time:
        rand_x = random.randint(32, 736)
        rand_y = random.randint(0, 32)
        rand_img = random.randint(1, 6)
        if rand_img == 1:
            human_img = boy
        elif rand_img == 2:
            human_img = girl
        elif rand_img == 3:
            human_img = darkguy
        elif rand_img == 4:
            human_img = oldman
        elif rand_img == 5:
            human_img = guy
        elif rand_img == 6:
            human_img = explorergirl
        human = Object(human_img, rand_x, rand_y, 1)
        humans.add(human)
        all_sprites.add(human)
        start_time = step_time

    for human in humans:
        # при нажатии надеваем маску
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # надеваем маску только если человек был без маски
            if human.rect.collidepoint(x, y) and (human.image == boy or human.image == girl or human.image == darkguy or human.image == oldman or human.image == guy or human.image == explorergirl):
                score += 1
                if score % 10 == 0:
                    lives += 1
                    lives_text = lives_font.render(
                        ("Жизни: " + str(lives)), True, pygame.Color("yellow"))
                if human.image == boy:
                    human.image = boy_mask
                elif human.image == girl:
                    human.image = girl_mask
                elif human.image == darkguy:
                    human.image = darkguy_mask
                elif human.image == oldman:
                    human.image = oldman_mask
                elif human.image == guy:
                    human.image = guy_mask
                elif human.image == explorergirl:
                    human.image = explorergirl_mask
                score_text = score_font.render(
                    ("Маски: " + str(score)), True, pygame.Color("yellow"))



        # люди ходят
        human.rect.y += human.speed
        # проверка на маску и удаление объектов после выхода за границу окна
        if human.rect.y > 600:
            if human.image != boy_mask and human.image != girl_mask and human.image != darkguy_mask and human.image != oldman_mask and human.image != guy_mask and human.image != explorergirl_mask:
                lives -= 1
                lives_text = lives_font.render(
                    ("Жизни: " + str(lives)), True, pygame.Color("yellow"))
            humans.remove(human)
            all_sprites.remove(human)

    all_sprites.draw(window)
    all_sprites.update()
    window.blit(score_text, (650, 30))
    window.blit(lives_text, (650, 60))
    pygame.display.update()

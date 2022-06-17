import pygame
from sys import exit
from random import choice
from pygame.locals import *

pygame.init()
SCREEN_SIZE = (640,480)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('LOCKED')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

level = 0
TILE_SIZE = 40
true_scroll = [0,0]
enemies_list = []

with open(f'maps/map_{level}.txt','r') as f: Game_map = [list(row) for row in f.read().split('\n')]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player1 = pygame.image.load('images/player/animation/0.png').convert_alpha()
        self.player1 = pygame.transform.scale(self.player1,(int(self.player1.get_width() * 1.3),int(self.player1.get_height()*1.3)))
        self.player2 = pygame.image.load('images/player/animation/1.png').convert_alpha()
        pygame.display.set_icon(self.player2)
        self.player2 = pygame.transform.scale(self.player2,(int(self.player2.get_width() * 1.3),int(self.player2.get_height()*1.3)))
        self.frames = [self.player1,self.player2]
        self.index = 0
        self.right_sprite = self.frames[self.index]
        self.left_sprite = pygame.transform.flip(self.right_sprite,True,False)
        self.image = self.right_sprite
        self.rect = self.image.get_rect(topleft = (340,200))
        self.is_right = True
        self.gravity = 0.25
        self.fall = 0
        self.Jumps = 2
        self.can_jump = True
        self.is_jump = False
        self.Dash = 2
        self.can_dash = True
        self.seconds = 0
        self.coins = 0
        self.speed = 0

    def Inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.is_right = False
            self.speed = -3

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed = 3
            self.is_right = True

        else: self.speed = 0

    def Animation(self):
        if self.fall > 1: self.is_jump = True
        if self.is_jump:
            self.right_sprite = self.frames[1]
            self.left_sprite = pygame.transform.flip(self.right_sprite,True,False)
            if self.is_right: self.image = self.right_sprite
            else: self.image = self.left_sprite
            self.rect = self.image.get_rect(topleft = (self.rect.x,self.rect.y))
        else:
            self.index += 0.03
            if self.index >= len(self.frames): self.index = 0
            self.right_sprite = self.frames[int(self.index)]
            self.left_sprite = pygame.transform.flip(self.right_sprite,True,False)
            if self.is_right: self.image = self.right_sprite
            else: self.image = self.left_sprite
            self.rect = self.image.get_rect(topleft = (self.rect.x,self.rect.y))

    def Get_Dash(self):
        if self.Dash < 2:
            self.seconds += 0.1
            if self.seconds >= 100:
                self.Dash += 1
                self.can_dash = True
                self.seconds = 0

    def Show_power_up(self):
        if self.Dash == 2:
            Dash_image = Dash_img
        elif self.Dash == 1:
            Dash_image = half_dash
        elif self.Dash == 0:
            Dash_image = no_dash

        Dash_image_rect = Dash_image.get_rect(topleft = (560,20))
        screen.blit(Dash_image,Dash_image_rect)
        pygame.draw.rect(screen,WHITE,(Dash_image_rect.x-1,Dash_image_rect.y-1,Dash_image.get_width()+1,Dash_image.get_height()+1),2)

    def Check_collision(self,rect,tiles):
        return [tile for tile in tiles if rect.colliderect(tile)]

    def Move(self,tiles,rect):
        rect.x += self.speed
        collission = self.Check_collision(rect,tiles)
        for tile in collission:
            if self.speed > 0: self.rect.right = tile.left
            elif self.speed < 0: self.rect.left = tile.right
            
        self.rect.y += self.fall
        collission = self.Check_collision(rect,tiles)
        for tile in collission:
            if self.fall > 0 and not self.rect.top >= tile.bottom:
                self.rect.bottom = tile.top
                self.Jumps = 2
                self.can_jump = True
                self.fall = 0
                self.is_jump = False

            elif self.fall < 0 and not self.rect.bottom <= tile.top:
                self.rect.top = tile.bottom
                self.fall = 0

        return rect

    def Apply_gravity(self):
        self.fall += self.gravity
        if self.fall >= 5:
            self.fall = 5

    def draw(self):
        screen.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def update(self):
        self.Apply_gravity()
        self.rect = self.Move(obsticale_list, self.rect)
        self.Inputs()
        self.Animation()
        self.Get_Dash()
        self.Show_power_up()
        self.draw()

class Enemy(pygame.sprite.Sprite):
    Touch = False
    def __init__(self,x,y):
        super().__init__()
        self.index = choice((0,1))
        self.is_right = choice((True,False))
        self.enemy1 = pygame.image.load('images/enemy/0.png').convert_alpha()
        self.enemy1 = pygame.transform.scale(self.enemy1, (player.sprite.image.get_width(), player.sprite.image.get_height()))
        self.enemy2 = pygame.image.load('images/enemy/1.png').convert_alpha()
        self.enemy2 = pygame.transform.scale(self.enemy2, (player.sprite.image.get_width(), player.sprite.image.get_height()))
        self.frames = [self.enemy2, self.enemy1]
        self.right_sprite = self.frames[self.index]
        self.left_sprite = pygame.transform.flip(self.right_sprite,True,False)
        if self.is_right:
            self.image = self.right_sprite
        else: self.image = self.left_sprite
        self.rect = self.image.get_rect(topleft = (x,y - 0.5))

    def Check_collision(self):
        global timer
        if pygame.sprite.spritecollide(player.sprite, enemy_group, False) or Enemy.Touch:
            coins_group.empty()
            enemy_group.empty()
            if sound_effects:
                hurt_sound.play()
            player.sprite.fall = 0
            player.sprite.is_right = True
            player.sprite.rect.topleft = (340,200)
            with open(f'maps/map_{level}.txt','r') as f:
                Game_map = [list(row) for row in f.read().split('\n')]

            process_data(Game_map)
            player.sprite.coins = 0
            player.sprite.Jumps = 2
            player.sprite.can_jump = True
            timer = -1
            Enemy.Touch = False

    def Animation(self):
        self.index += 0.03
        if self.index >= len(self.frames): self.index = 0
        self.right_sprite = self.frames[int(self.index)]
        self.left_sprite = pygame.transform.flip(self.right_sprite,True,False)
        if self.is_right: self.image = self.right_sprite
        else: self.image = self.left_sprite
        self.rect = self.image.get_rect(topleft = (self.rect.x, self.rect.y))

    def draw(self):
        screen.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def update(self):
        self.Check_collision()
        self.Animation()
        self.draw()

class Coins(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('images/coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width() * 1.1), int(self.image.get_height() * 1.1)))
        self.rect = self.image.get_rect(topleft = (x,y + 3))

    def draw(self):
        screen.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def Check_collision(self):
        if pygame.sprite.spritecollide(player.sprite,coins_group,True):
            player.sprite.coins += 1
            if sound_effects:
                click_sound.play()

    def update(self):
        self.Check_collision()
        self.draw()

class Button:
    def __init__(self, font, text_btn, geometry, text_pos):
        self.text_pos = text_pos
        self.font_color = WHITE
        self.text = text_btn
        self.font = font
        self.rect = pygame.Rect(*geometry)

    def active(self):
        if self.rect.colliderect(*pygame.mouse.get_pos(), 1, 1):
            pygame.draw.rect(screen, WHITE, self.rect, 0, 5)
            self.font_color = BLACK
        else: self.font_color = WHITE

        text = self.font.render(self.text, False, self.font_color)
        pygame.draw.rect(screen, WHITE, self.rect, 2, 5)
        screen.blit(text, self.text_pos)

def process_data(data):
    enemies_list.clear()
    for y,row in enumerate(data):
        for x,col in enumerate(row):
            if col == '3':
                coins_group.add(Coins(x * TILE_SIZE, y * TILE_SIZE))

            elif col == '4':
                enemy_group.add(Enemy(x * TILE_SIZE, y * TILE_SIZE))
                enemies_list.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, player.sprite.image.get_width(), player.sprite.image.get_height()))

def Display_texts():
    level_text = font.render(f'Level - {level + 1}',False,WHITE)
    level_text_rect = level_text.get_rect(topleft = (10,15))

    coins_text = font.render(f'Coins  {player.sprite.coins}/{level_coins}',False,WHITE)
    coins_text_rect = coins_text.get_rect(topleft = (10,45))

    timer_text = small_font.render(f'Timer : {int(level_time - timer)}',False,WHITE)
    timer_text_rect = timer_text.get_rect(topleft = (558,50))

    fps_text = small_font.render(str(int(clock.get_fps())), False, WHITE)
    fps_text_rect = fps_text.get_rect(midtop = (SCREEN_SIZE[0] / 2, 5))

    screen.blit(level_text,level_text_rect)
    screen.blit(coins_text,coins_text_rect)
    screen.blit(timer_text,timer_text_rect)
    if show_fps: screen.blit(fps_text,fps_text_rect)

def Options_menu():
    sound_text = font40.render('Sound Effects :', False, WHITE)
    screen.blit(sound_text, (SCREEN_SIZE[0]/2 - 130, SCREEN_SIZE[1]/2- 80))

    music_text = font40.render('Music :', False, WHITE)
    screen.blit(music_text, (SCREEN_SIZE[0]/2 - 130, SCREEN_SIZE[1]/2 - 20))

    fps_text = font40.render('Show FPS : ', False, WHITE)
    screen.blit(fps_text, (SCREEN_SIZE[0]/2 - 130, SCREEN_SIZE[1]/2 + 40))

# colors
BLACK = tuple(0 for i in range(3))
WHITE = tuple(255 for i in range(3))

# sounds
click_sound = pygame.mixer.Sound('sounds/click.wav')
click_sound.set_volume(0.5)
pygame.mixer.music.load('sounds/music.wav')
pygame.mixer.music.set_volume(0.4)
sound_effects = True
Jump_sound = pygame.mixer.Sound('sounds/jump.wav')
Jump_sound.set_volume(0.4)
hurt_sound = pygame.mixer.Sound('sounds/hurt.wav')
hurt_sound.set_volume(0.5)

# fonts
font = pygame.font.Font('font/m6x11.ttf',25)
small_font = pygame.font.Font('font/m6x11.ttf',20)
mid_font = pygame.font.Font('font/m6x11.ttf',30)
big_font = pygame.font.Font('font/m6x11.ttf',100)
font2 = pygame.font.Font('font/m6x11.ttf',50)
font40 = pygame.font.Font('font/m6x11.ttf',40)

# images
Dash_img = pygame.image.load('images/player/power-up/full.png').convert_alpha()
Dash_img = pygame.transform.scale(Dash_img,(int(Dash_img.get_width()*4),int(Dash_img.get_height()*4)))

half_dash = pygame.image.load('images/player/power-up/half.png').convert_alpha()
half_dash = pygame.transform.scale(half_dash,(int(half_dash.get_width()*4),int(half_dash.get_height()*4)))

no_dash = pygame.image.load('images/player/power-up/empty.png').convert_alpha()
no_dash = pygame.transform.scale(no_dash,(int(no_dash.get_width()*4),int(no_dash.get_height()*4)))

mouse = pygame.image.load('images/cursor.png').convert_alpha()
mouse = pygame.transform.scale(mouse,(int(mouse.get_width()*0.5),int(mouse.get_height()*0.5)))

tile_image = pygame.image.load('images/tile.png').convert_alpha()
tile_image = pygame.transform.scale(tile_image,(TILE_SIZE,TILE_SIZE))

# groups
player = pygame.sprite.GroupSingle(Player())
enemy_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()

process_data(Game_map)

level_coins = len(coins_group)
level_time = level_coins * 2
timer = -1
start_menu = True
game_paused = False
sound_rect = Button(font, 'On', (455, SCREEN_SIZE[1]/2- 77, 50, 35), (470, 172))
music_rect = Button(font, 'On', (311, 223, 50, 35), (326, 231))
fps_rect = Button(font, 'On', (370, 281, 50, 35), (384, 289))
back_rect = Button(mid_font, 'Back', (10, SCREEN_SIZE[1] - 60, 120, 45), (43, SCREEN_SIZE[1] - 50))
exit_rect = Button(mid_font, 'Exit', (SCREEN_SIZE[0]/2 - 60, SCREEN_SIZE[1] - 80, 120, 45), (SCREEN_SIZE[0]/2 - 25,SCREEN_SIZE[1] - 68))
start_rect = Button(mid_font, 'Start', (SCREEN_SIZE[0]/2 - 60,SCREEN_SIZE[1] - 230,120,45), (SCREEN_SIZE[0]/2 - 31, SCREEN_SIZE[1] - 218))
options_rect = Button(mid_font, 'Options', (SCREEN_SIZE[0]/2 - 60, SCREEN_SIZE[1] - 155,120,45), (SCREEN_SIZE[0]/2 - 41, SCREEN_SIZE[1]-146))
yes_rect = pygame.Rect(SCREEN_SIZE[0]/2 - 60,SCREEN_SIZE[1]-120,120,45)
my_name = True
show_fps = True
font_color = WHITE
time = pygame.time.get_ticks()
Jump_sound.play()

while my_name:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    real_time = (pygame.time.get_ticks() - time) / 1000
    if real_time > 3:
        my_name = False
        pygame.mixer.music.play(-1)

    by_text = small_font.render('by',False,WHITE)
    my_name_text = mid_font.render('specialGames',False,WHITE)
    screen.blit(my_name_text,(SCREEN_SIZE[0]/2 - my_name_text.get_width()/2,SCREEN_SIZE[1]/2 - my_name_text.get_height()/2))
    screen.blit(by_text,(SCREEN_SIZE[0]/2 - my_name_text.get_width()/2 - by_text.get_width(),SCREEN_SIZE[1]/2 - my_name_text.get_height()/2 -by_text.get_height()))

    pygame.display.update()

while True:
    while start_menu or game_paused:
        mouse_rect = pygame.Rect(*pygame.mouse.get_pos(), 1, 1)
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if start_rect.rect.collidepoint(pos):
                    if sound_effects: click_sound.play()
                    start_menu = False
                    game_paused = False

                elif exit_rect.rect.collidepoint(pos):
                    pygame.quit()
                    exit()

                elif options_rect.rect.collidepoint(pos):
                    options_menu = True
                    if sound_effects: click_sound.play()

                    while options_menu:
                        pos = pygame.mouse.get_pos()
                        mouse_rect = pygame.Rect(*pos, 1, 1)
                        screen.fill(BLACK)                        
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                                if back_rect.rect.collidepoint(pos):
                                    options_menu = False
                                    if sound_effects: click_sound.play()
                                    break

                                if sound_rect.rect.collidepoint(pos): 
                                    sound_effects = not sound_effects
                                    if sound_rect.text == 'On': 
                                        sound_rect.text = 'Off'
                                        sound_rect.text_pos = (sound_rect.text_pos[0] - 5, sound_rect.text_pos[1])

                                    elif sound_rect.text == 'Off':
                                        sound_rect.text = 'On'       
                                        sound_rect.text_pos = (sound_rect.text_pos[0] + 5, sound_rect.text_pos[1])

                                elif music_rect.rect.collidepoint(pos): 
                                    if music_rect.text == 'On': 
                                        music_rect.text = 'Off'
                                        music_rect.text_pos = (music_rect.text_pos[0] - 5, music_rect.text_pos[1])
                                        pygame.mixer.music.fadeout(1500)

                                    elif music_rect.text == 'Off':
                                        music_rect.text = 'On'       
                                        music_rect.text_pos = (music_rect.text_pos[0] + 5, music_rect.text_pos[1])
                                        pygame.mixer.music.play(-1)

                                elif fps_rect.rect.collidepoint(pos): 
                                    show_fps = not show_fps
                                    if fps_rect.text == 'On': 
                                        fps_rect.text = 'Off'
                                        fps_rect.text_pos = (fps_rect.text_pos[0] - 5, fps_rect.text_pos[1])

                                    elif fps_rect.text == 'Off':
                                        fps_rect.text = 'On'       
                                        fps_rect.text_pos = (fps_rect.text_pos[0] + 5, fps_rect.text_pos[1])


                        Options_menu()
                        back_rect.active()
                        sound_rect.active()
                        music_rect.active()
                        fps_rect.active()

                        screen.blit(mouse,mouse_rect)
                        pygame.display.update()

        if game_paused:
            start_rect.text = 'Resume'
            start_rect.text_pos = (SCREEN_SIZE[0]/2 - 40, start_rect.text_pos[1])
            text3 = big_font.render('Game Paused', False, WHITE)
            screen.blit(text3,(85,SCREEN_SIZE[1] - 400))

        elif start_menu:
            text3 = big_font.render('LOCKED', False, WHITE)
            text3_rect = text3.get_rect(center = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]-350))
            screen.blit(text3,text3_rect)

        exit_rect.active()
        start_rect.active()
        options_rect.active()

        screen.blit(mouse,mouse_rect)
        pygame.display.update()

    screen.fill(BLACK)

    true_scroll[0] += (player.sprite.rect.x - true_scroll[0] - (320 - player.sprite.image.get_width()/2)) / 20
    true_scroll[1] += (player.sprite.rect.y - true_scroll[1] - (240 - player.sprite.image.get_height()/2)) / 20
    scroll = [int(true_scroll[0]), int(true_scroll[1])]
    timer += 0.008

    obsticale_list = []
    for y, row in enumerate(Game_map):
        for x, col in enumerate(row):
            if col == '1' or col == '2':
                rect = tile_image.get_rect(topleft = (x * TILE_SIZE, y * TILE_SIZE))
                obsticale_list.append(rect)
                screen.blit(tile_image,(x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w] and player.sprite.Jumps > 0 and player.sprite.can_jump:
                player.sprite.fall = 0
                player.sprite.fall -= 7
                player.sprite.Jumps -= 1
                player.sprite.can_jump = False
                player.sprite.is_jump = True
                if sound_effects:
                    Jump_sound.play()

            if event.key in [pygame.K_DOWN, pygame.K_s] and player.sprite.Dash > 0 and player.sprite.can_dash:
                dash_list = []
                for tile in obsticale_list:
                    if player.sprite.is_right and abs(tile.left - player.sprite.rect.right) < 150 and player.sprite.rect.top < tile.top < player.sprite.rect.bottom or tile.top < player.sprite.rect.top < tile.bottom and player.sprite.is_right and abs(tile.left - player.sprite.rect.right) < 150:
                        dash_list.append(abs(tile.left - player.sprite.rect.right))
                    
                    elif not player.sprite.is_right and abs(player.sprite.rect.left - tile.right) < 150 and player.sprite.rect.top < tile.top < player.sprite.rect.bottom or tile.top < player.sprite.rect.top < tile.bottom and not player.sprite.is_right and abs(player.sprite.rect.left - tile.right) < 150:
                        dash_list.append(abs(player.sprite.rect.left - tile.right))

                for enemy in enemies_list:
                    if dash_list:
                        if player.sprite.is_right and abs(enemy.left - player.sprite.rect.right) < min(dash_list) and player.sprite.rect.top <= enemy.top < player.sprite.rect.bottom:
                            Enemy.Touch = True
                        elif not player.sprite.is_right and abs(player.sprite.rect.left - enemy.right) < min(dash_list) and player.sprite.rect.top <= enemy.top < player.sprite.rect.bottom:
                            Enemy.Touch = True
                    else:
                        if player.sprite.is_right and abs(enemy.left - player.sprite.rect.right) < 150 and player.sprite.rect.top <= enemy.top < player.sprite.rect.bottom:
                            Enemy.Touch = True
                        elif not player.sprite.is_right and abs(player.sprite.rect.left - enemy.right) < 150 and player.sprite.rect.top <= enemy.top < player.sprite.rect.bottom:
                            Enemy.Touch = True

                if dash_list:
                    if player.sprite.is_right:
                        for i in range(6):
                            player.sprite.rect.x += min(dash_list) / 6
                            if pygame.sprite.spritecollide(player.sprite,coins_group,True):
                                player.sprite.coins += 1
                                if sound_effects:
                                    click_sound.play()

                    else:
                        for i in range(6):
                            player.sprite.rect.x -= min(dash_list) / 6
                            if pygame.sprite.spritecollide(player.sprite,coins_group,True):
                                player.sprite.coins += 1
                                if sound_effects:
                                    click_sound.play()
            
                else:
                    if player.sprite.is_right: 
                        for i in range(6):
                            player.sprite.rect.centerx += 25
                            if pygame.sprite.spritecollide(player.sprite,coins_group,True):
                                player.sprite.coins += 1
                                if sound_effects:
                                    click_sound.play()

                    else:
                        for i in range(6):
                            player.sprite.rect.centerx -= 25
                            if pygame.sprite.spritecollide(player.sprite,coins_group,True):
                                player.sprite.coins += 1
                                if sound_effects:
                                    click_sound.play()

                if sound_effects:
                    Jump_sound.play()
                player.sprite.Dash -= 1
                player.sprite.can_dash = False
                dash_list.clear()

            if event.key in [pygame.K_p, pygame.K_ESCAPE]:
                game_paused = True

            if event.key == pygame.K_r:
                coins_group.empty()
                enemy_group.empty()
                player.sprite.fall = 0
                player.sprite.is_right = True
                player.sprite.rect.topleft = (340,200)
                with open(f'maps/map_{level}.txt','r') as f:
                    Game_map = [list(row) for row in f.read().split('\n')]
                process_data(Game_map)
                player.sprite.coins = 0
                player.sprite.Jumps = 2
                player.sprite.can_jump = True
                timer = -1

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_w] and player.sprite.Jumps > 0 and not player.sprite.can_jump:
                player.sprite.can_jump = True

            if event.key in [pygame.K_DOWN, pygame.K_s] and player.sprite.Dash > 0  and not player.sprite.can_dash:
                player.sprite.can_dash = True

    Display_texts()
    enemy_group.update()
    coins_group.update()
    player.update()

    if int(level_time - timer) <= 0:
        coins_group.empty()
        enemy_group.empty()
        player.sprite.fall = 0
        player.sprite.is_right = True
        player.sprite.rect.topleft = (340,200)
        with open(f'maps/map_{level}.txt','r') as f:
            Game_map = [list(row) for row in f.read().split('\n')]

        process_data(Game_map)
        player.sprite.coins = 0
        player.sprite.Jumps = 2
        player.sprite.can_jump = True
        timer = -1

    if player.sprite.coins == level_coins and level < 8:
        coins_group.empty()
        enemy_group.empty()
        player.sprite.fall = 0
        player.sprite.is_right = True
        player.sprite.rect.topleft = (340,200)
        level += 1
        with open(f'maps/map_{level}.txt','r') as f:
            Game_map = [list(row) for row in f.read().split('\n')]

        process_data(Game_map)
        player.sprite.coins = 0
        level_coins = len(coins_group)
        level_time = level_coins * 2
        timer = -1
        player.sprite.Jumps = 2
        player.sprite.can_jump = True

    elif level_coins == player.sprite.coins and level == 8:
        over = True
        while over:
            screen.fill(BLACK)
            mouse_rect = pygame.Rect(*pygame.mouse.get_pos(), 1, 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_m:
                        if play_music:
                            play_music = False
                            pygame.mixer.music.fadeout(1500)
                        else:
                            play_music = True
                            pygame.mixer.music.play(-1)

                if event.type ==  pygame.MOUSEBUTTONUP and event.button == 1 and yes_rect.collidepoint(pygame.mouse.get_pos()):
                    coins_group.empty()
                    enemy_group.empty()
                    player.sprite.fall = 0
                    player.sprite.is_right = True
                    player.sprite.Dash = 2
                    player.sprite.can_dash = True
                    player.sprite.seconds = 0
                    player.sprite.rect.topleft = (340,200)
                    level = 0
                    with open(f'maps/map_{level}.txt','r') as f:
                        Game_map = [list(row) for row in f.read().split('\n')]

                    process_data(Game_map)
                    player.sprite.coins = 0
                    level_coins = len(coins_group)
                    timer = -1
                    player.sprite.Jumps = 2
                    player.sprite.can_jump = True
                    level_time = level_coins * 2
                    over = False

            finished_text = font2.render('You Finished The Game !', False, WHITE)
            restart_text = mid_font.render('Restart From Level 1 ?',False,WHITE)
            thanks_text = font2.render('Thanks For Playing :)',False,WHITE)
            yes_text = mid_font.render('Yes',False,font_color)
            finished_text_rect = finished_text.get_rect(center = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2-80))
            thanks_text_rect = thanks_text.get_rect(center = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2))
            restart_text_rect = restart_text.get_rect(center = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2+80))

            if mouse_rect.colliderect(yes_rect):
                font_color = BLACK
                pygame.draw.rect(screen,WHITE,yes_rect,0,5)
            else: font_color = WHITE

            screen.blit(restart_text,restart_text_rect)
            screen.blit(finished_text,finished_text_rect)
            screen.blit(thanks_text,thanks_text_rect)
            pygame.draw.rect(screen,WHITE,yes_rect,2,5)
            screen.blit(yes_text,(SCREEN_SIZE[0]/2 - 20, SCREEN_SIZE[1] - 110))
            screen.blit(mouse,mouse_rect)
            pygame.display.update()

    pygame.display.update()
    clock.tick(120)
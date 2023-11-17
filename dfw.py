import pygame
import sys
import time

from draw import Button, draw_text, draw_player
from game import *
from player import Player


pygame.init()

screen_size = (1080, 680)
role_size = (60, 60)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Monopoly - Tsinghua Journey")
map_screen = pygame.image.load('image/地图.bmp')
stop_picture = pygame.image.load('image/禁止.jpg')
stop_picture = pygame.transform.scale(stop_picture, (20, 20))

lose_sound = pygame.mixer.Sound('sound/失败.wav')
win_sound = pygame.mixer.Sound('sound/胜利.wav')
up_sound = pygame.mixer.Sound('sound/升级.wav')
click_sound = pygame.mixer.Sound('sound/按键.wav')
chances_sound = pygame.mixer.Sound('sound/事件.wav')

picture_dice = []
for i in range(6):
    picture_dice.append(pygame.image.load('image/dice/%d.jpg'%(i+1)))

map_screen = pygame.transform.scale(map_screen, screen_size)

screen.blit(map_screen, (0, 0))

play_button = Button(screen, 'start')
play_button.draw_button()

status = 0
cur_player = 0
dice_answer = 1
player = []
role = []

local_init = [0, 20, 12, 32]  # initial position
map_status = []
for i in range(8):
    map_status.append(Map(i))

while True:
    if status == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = event.pos
                #print(mouse_x, mouse_y)
                if click_button(mouse_x, mouse_y, 0):
                    click_sound.play()
                    num_player_button = Button(screen, 'Number of players(2~4)')
                    num_player_button.draw_button()
                    #           50, 'STXINGKA.TTF', pygame.Color('gold'))
                    status = 1
        pygame.display.update()
    elif status == 1:  # Select number of players
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if 258 <= event.key <= 260 or 50 <= event.key <= 52:
                    click_sound.play()
                    role.append(pygame.image.load('image/role/小e.jpg'))
                    role.append(pygame.image.load('image/role/皮卡丘.jpg'))
                    if event.key == 259 or event.key == 51:
                        role.append(pygame.image.load('image/role/可达鸭.jpg'))
                    elif event.key == 260 or event.key == 52:
                        role.append(pygame.image.load('image/role/可达鸭.jpg'))
                        role.append(pygame.image.load('image/role/小黄鸡.jpg'))
                    screen.blit(map_screen, (0, 0))
                    for i in range(len(role)):
                        role[i] = pygame.transform.scale(role[i], role_size)
                        player.append(Player(i))
                        player[i].local = local_init[i]
                    draw_player(screen, player, role, stop_picture)
                    status = 2
    elif status == 2:
        for i in range(6):
            screen.blit(picture_dice[i], (500, 400))
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
            # elif event.type == pygame.KEYDOWN:
                (mouse_x, mouse_y) = event.pos
                # print(mouse_x, mouse_y)
                if mouse_x >= 501 and mouse_x <=576 and mouse_y >= 404 and mouse_y <= 482:
                # if event.key == 273:
                    click_sound.play()
                    dice_answer = get_dice()
                    status = 3
        pygame.display.update()
    elif status == 3: #move
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for i in range(dice_answer):
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            player[cur_player].local = (player[cur_player].local + 1) % 40
            player[cur_player].count = (player[cur_player].count + 1)
            # draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            click_sound.play()
            pygame.display.update()
            time.sleep(0.5)
        if Special(player[cur_player].local):
            status = 4
        else:
            status = 2
            cur_player = (cur_player + 1) % len(player)
        if not game_over(player) == 0:
            if game_over(player) > 0:
                win_sound.play()
            else:
                lose_sound.play()
            status = 6
        pygame.display.update()
    elif status == 4: #trigger event
        if player[cur_player].local == 5: #office building
            player[cur_player].money += 500
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            # draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (800, 340), 'office building,money+500', 30, 'STXINGKA.TTF', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 15: #gas station
            player[cur_player].money -= 300
            # player[0].stop = 1
            # player[0].gpa += 0.2
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            # draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (750, 340), 'gas station,money -300', 30, 'STXINGKA.TTF', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 25: #hosipital
            player[cur_player].money -= 1000
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            # draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (800, 340), 'hosipital, money-1000', 30, 'STXINGKA.TTF', pygame.Color('grey'))
            chances_sound.play()
        elif player[cur_player].local == 35: #school
            player[cur_player].money += 200
            screen.blit(map_screen, (0, 0))
            screen.blit(picture_dice[dice_answer - 1], (500, 400))
            # draw_mapstatus(screen, player, map_status)
            draw_player(screen, player, role, stop_picture)
            draw_text(screen, (800, 340), 'school,money+200', 30, 'STXINGKA.TTF', pygame.Color('grey'))
            chances_sound.play()
        cur_player = (cur_player + 1) % len(player)
        while player[cur_player].stop == 1:
            player[cur_player].stop = 0
            cur_player = (cur_player + 1) % len(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        if not game_over(player) == 0:
            if game_over(player) > 0:
                win_sound.play()
            else:
                lose_sound.play()
            status = 6
        else:
            status = 2
    elif status == 6:  # game over
        if game_over(player) > 0:
            draw_text(screen, (540, 340), 'Game over,%s win' % player[game_over(player) - 1].name,
                      50, 'STXINGKA.TTF', pygame.Color('darkgreen'))
            draw_text(screen, (540, 440), 'One more game',
                      50, '', pygame.Color('darkgreen'))

        else:
            draw_text(screen, (540, 340), 'Game over,%s fail' % player[- game_over(player) - 1].name,
                      50, '', pygame.Color('darkgreen'))
            draw_text(screen, (540, 440), 'One more game',
                      50, '', pygame.Color('darkgreen'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = event.pos
                if click_button(mouse_x, mouse_y, 1):
                    player = []
                    role = []
                    map_status = []
                    for i in range(8):
                        map_status.append(Map(i))
                    cur_player = 0
                    click_sound.play()
                    screen.blit(map_screen, (0, 0))
                    num_player_button = Button(screen, 'Number of players(2~4)')
                    num_player_button.draw_button()
                    # draw_text(screen, (540, 440),
                    #           50, 'STXINGKA.TTF', pygame.Color('gold'))
                    status = 1
        pygame.display.update()


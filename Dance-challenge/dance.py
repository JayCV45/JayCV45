# -*- coding: utf-8 -*-
"""
Created on Sun May  8 13:08:32 2022

@author: pc
"""

import pgzrun
import pygame
import pgzero
import random
import matplotlib.animation as animate
from pgzero.builtins import Actor
from random import randint

WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT /2 

move_list=[]
display_list=[]

score1 = 0
score2 = 0
current_move = 0
count = 4
dance_length = 2
rounds = 1

show_countdown = True
moves_complete = False
game_over = False
player1 = True
player2 = False

dancer = Actor('dancer-start')
dancer.pos = CENTER_X + 5, CENTER_Y - 40

up = Actor("up")
up.pos = CENTER_X, CENTER_Y + 110
right = Actor("right")
right.pos = CENTER_X + 60, CENTER_Y + 170
down = Actor("down")
down.pos = CENTER_X, CENTER_Y + 230
left = Actor("left")
left.pos = CENTER_X - 60, CENTER_Y + 170

def draw():
    global game_over, score, player1, player2
    global count, show_countdown
    if not game_over:
        screen.clear()
        screen.blit("stage", (0, 0))
        dancer.draw()
        up.draw()
        down.draw()
        right.draw()
        left.draw()
        screen.draw.text("Player1's score: " + str(score1), color='black', topleft=(10,10))
        screen.draw.text("Player2's score: " + str(score2), color='black', topleft=(10,30))
        if show_countdown:
            screen.draw.text(str(count), color='black', topleft=(CENTER_X - 8, 150), fontsize=60)
        if player1:
            screen.draw.text("Player1", color='black', topleft=(CENTER_X - 65, 150), fontsize=60)
        if player2:
            screen.draw.text("Player2", color='black', topleft=(CENTER_X - 65, 150), fontsize=60)
    else:
        screen.clear()
        screen.blit("stage", (0,0))
        screen.draw.text("Player1's score: " + str(score1), color='black', topleft=(10,10))
        screen.draw.text("Player2's score: " + str(score2), color='black', topleft=(10,30))
        screen.draw.text("GAME OVER!", color='black', topleft=(CENTER_X - 130, 220), fontsize=60)
    return

def reset_dancer():
    global game_over
    if not game_over:
        dancer.image = "dancer-start"
        up.image = "up"
        right.image = "right"
        down.image = "down"
        left.image = "left"
    return

def update_dancer(move):
    global game_over
    if not game_over:
        if move == 0:
            up.image = "up-lit"
            dancer.image = "dancer-up"
            clock.schedule(reset_dancer, 0.5)
        elif move == 1:
            right.image = "right-lit"
            dancer.image = "dancer-right"
            clock.schedule(reset_dancer, 0.5)
        elif move == 2:
            down.image = "down-lit"
            dancer.image = "dancer-down"
            clock.schedule(reset_dancer, 0.5)         
        else:
            left.image = "left-lit"
            dancer.image = "dancer-left"
            clock.schedule(reset_dancer, 0.5)         
    return

def display_moves():
    global move_list, display_list, dance_length
    global show_countdown, current_move, player1, player2
    if display_list:
        this_move = display_list[0]
        display_list = display_list[1:]
        if this_move == 0:
            update_dancer(0)
            clock.schedule(display_moves, 1)
        elif this_move == 1:
            update_dancer(1)
            clock.schedule(display_moves, 1)        
        elif this_move == 2:
            update_dancer(2)
            clock.schedule(display_moves, 1)    
        else:
            update_dancer(3)
            clock.schedule(display_moves, 1)    
    elif (rounds % 2 == 0):
        player2 = True
        player1 = False
        show_countdown = False
    else:
        player1 = True
        player2 = False
        show_countdown = False
    return
            
def generate_moves():
    global move_list, dance_length, count
    global show_countdown, player1, player2 
    count = 4
    move_list = []
    player1 = False
    player2 = False
    for move in range(0, dance_length):
        rand_move = randint(0, 3)
        move_list.append(rand_move)
        display_list.append(rand_move)
    show_countdown = True
    countdown()
    return

def countdown():
    global count, game_over, show_countdown
    if count > 1:
        count = count - 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()
    return

def next_move():
    global dance_length, current_move, moves_complete
    if current_move < dance_length - 1:
        current_move = current_move + 1
    else:
        moves_complete = True
    return

def game_rounds():
    global rounds, moves_complete, dance_length
    if (rounds % 3 == 0):
        dance_length += 1
        moves_complete = False
        rounds += 1
    else:
        rounds += 1
    return 

def on_key_up(key):
    global score1, score2, game_over, move_list, current_move
    if key == keys.UP:
        update_dancer(0)
        if move_list[current_move] == 0:
            score1 += 1
            next_move()
        else:
            game_over = True
    elif key == keys.RIGHT:
        update_dancer(1)
        if move_list[current_move] == 1:
            score1 += 1
            next_move()
        else:
            game_over = True
    elif key == keys.DOWN:
        update_dancer(2)
        if move_list[current_move] == 2:
            score1 += 1
            next_move()
        else:
            game_over = True
    elif key == keys.LEFT:
        update_dancer(3)
        if move_list[current_move] == 3:
            score1 += 1
            next_move()
        else:
            game_over = True
    elif key == keys.W:
        update_dancer(0)
        if move_list[current_move] == 0:
            score2 += 1
            next_move()
        else:
            game_over = True
    elif key == keys.D:
        update_dancer(1)
        if move_list[current_move] == 1:
            score2 += 1
            next_move()
        else:
            game_over = True
    elif key == keys.S:
        update_dancer(2)
        if move_list[current_move] == 2:
            score2 += 1
            next_move()
        else:
            game_over = True
    elif key == keys.A:
        update_dancer(3)
        if move_list[current_move] == 3:
            score2 += 1
            next_move()
        else:
            game_over = True
    return

def update():
    global game_over, current_move, moves_complete
    if not game_over:
        if moves_complete:
            game_rounds()
            generate_moves()
            moves_complete = False
            current_move = 0
    else:
        music.stop()
        
generate_moves()
music.play("1")

pgzrun.go()
    
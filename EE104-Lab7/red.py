# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 21:54:08 2022

@author: chris.pham
"""

import pgzrun
import pygame
import pgzero
import random
from pgzero.builtins import Actor
from random import randint

#Declare constants
FONT_COLOR = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)
FINAL_LEVEL = 8
START_SPEED = 15
COLORS = ["green", "blue"]

#Music 
pygame.mixer.init()
music = pygame.mixer.music.load('MR.mp3')
pygame.mixer.music.play(-1)

#Declare global variables
game_over = False
game_complete = False
current_level = 1

#Keep track of the snowflakes on the screen
snowflakes = []
animations = []

#Draw the snowflakes
def draw():
    global snowflakes, current_level, game_over, game_complete
    screen.clear()
    screen.blit("space1", (0,0)) #add a background image to the game window
    if game_over:
        display_message("GAME OVER!", "Try again.")
    elif game_complete:
        display_message("YOU WON!", "Well done.")
    else:
        for snowflake in snowflakes:
            snowflake.draw()

def update():
    global snowflakes
    if len(snowflakes) == 0:
        snowflakes = make_snowflakes(current_level)

def make_snowflakes(number_of_extra_snowflakes):
    colors_to_create = get_colors_to_create(number_of_extra_snowflakes)
    new_snowflakes = create_snowflakes(colors_to_create)
    layout_snowflakes(new_snowflakes)
    animate_snowflakes(new_snowflakes)
    return new_snowflakes

def get_colors_to_create(number_of_extra_snowflakes):
    #return[]
    colors_to_create = ["red"]
    for i in range(0, number_of_extra_snowflakes):
        random_color = random.choice(COLORS)
        colors_to_create.append(random_color)
    return colors_to_create

def create_snowflakes(colors_to_create):
    #return[]
    new_snowflakes = []
    for color in colors_to_create:
        snowflake = Actor(color + "-snowflake")
        new_snowflakes.append(snowflake)
    return new_snowflakes

def layout_snowflakes(snowflakes_to_layout):
    #pass
    number_of_gaps = len(snowflakes_to_layout) + 1
    gap_size = WIDTH / number_of_gaps
    random.shuffle(snowflakes_to_layout)
    for index, snowflake in enumerate(snowflakes_to_layout):
        new_x_pos = (index + 1) * gap_size
        snowflake.x = new_x_pos
        if index % 2 == 0:
            snowflake.y = 0
        else:
            snowflake.y = HEIGHT 

def animate_snowflakes(snowflakes_to_animate):
    #pass
    for snowflake in snowflakes_to_animate:
        random_speed_adjustment = random.randint(0,5)
        duration = START_SPEED - current_level + random_speed_adjustment
        snowflake.anchor = ("center", "bottom")
        animation = animate(snowflake, duration=duration, on_finished=handle_game_over, y=HEIGHT)
        animations.append(animation)
        
def handle_game_over():
    global game_over 
    game_over = True
    
    
def on_mouse_down(pos):
    global snowflakes, current_level
    for snowflake in snowflakes:
        if snowflake.collidepoint(pos):
            if "red" in snowflake.image:
                red_snowflake_click()
            else:
                handle_game_over()


def red_snowflake_click():
    global current_level, snowflakes, animations, game_complete 
    stop_animations(animations)
    if current_level == FINAL_LEVEL:
        game_complete = True
    else:
        current_level = current_level + 1
        snowflakes = []
        animations = []
        
def stop_animations(animations_to_stop):
    for animation in animations_to_stop:
        if animation.running:
            animation.stop()
            
def display_message(heading_text, sub_heading_text):
    screen.draw.text(heading_text, fontsize=60, center=CENTER, color=FONT_COLOR)
    screen.draw.text(sub_heading_text,
                     fontsize=30,
                     center=(CENTER_X, CENTER_Y+30),
                     color=FONT_COLOR)


pgzrun.go()
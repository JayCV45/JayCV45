# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 15:39:04 2022

@author: jlong
"""

import pgzrun
import pygame
import pgzero
import random
import matplotlib.animation as animate
from pgzero.builtins import Actor
from random import randint

#Game dimension
display = pygame.display.set_mode((800,600))

#color
RED = (255,0,0)
GREEN = (0,255,0)

#Music
pygame.mixer.init()
music = pygame.mixer.music.load('Upbeat-Forever.mp3')
pygame.mixer.music.play(-1)

#balloon position
balloon = Actor("balloon")
balloon.pos = 400, 300

#bird position
bird = Actor("bird-up")
bird.pos = randint(800, 1600), randint(10, 200)

#house position
house = Actor("house")
house.pos = randint(800, 1600), 460

#tree position
tree = Actor("tree")
tree.pos = randint(800, 1600), 450

#global variables
bird_up = True
up = False
game_over = False 
score = 0
number_of_updates = 0
lives = 1
health = 100
alive = True

#scores array
scores = []

# Update high scores
def update_high_scores():
    global score, scores
    filename = r"high-scores.txt"
    scores=[]
    with open(filename, "r") as file:
        line = file.readline()
        high_scores = line.split()
        for high_score in high_scores:
            if (score > int(high_score)):
                scores.append(str(score) + " ")
                score = int(high_score)
            else:
                scores.append(str(high_score) + " ")
    with open(filename, "w") as file:
        for high_score in scores:
            file.write(high_score)

# Display high scores
def display_high_scores():
    screen.draw.text("HIGH SCORES", (350, 150), color="black")
    y = 175
    position = 1
    for high_score in scores:
        screen.draw.text(str(position) + ". " + high_score, (350, y), color="black")
        y += 25
        position += 1

# draw the game
def draw():
    global lives, score
    screen.clear()
    screen.blit("background", (0, 0))
    if not game_over:
        balloon.draw()
        bird.draw()
        house.draw()
        tree.draw()
        pygame.draw.rect(display, RED, (100,5,100,15))
        pygame.draw.rect(display, GREEN, (100,5,health,15))
        screen.draw.text("Lives: " +str(lives), (600, 5), color="black")
        screen.draw.text("Score: " + str(score), (700, 5), color="black")
    else:
        display_high_scores()
        
def on_mouse_down():
    global up
    up = True
    balloon.y -= 50
    
def on_mouse_up():
    global up
    up = False
    
def flap():
    global bird_up
    if bird_up:
        bird.image = "bird-down"
        bird_up = False
    else:
        bird.image = "bird-up"
        bird_up = True
            
        
def update():
    global game_over, score, number_of_updates, lives, health, alive        
    if not game_over:
        if not up:
            balloon.y += 1
            
        if bird.x > balloon.x:
            bird.x -= 5
            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            bird.x = randint(800, 1600)
            bird.y = randint(10, 200)
            score += 1
            number_of_updates = 0
            
        if house.right > balloon.x:
            house.x -= 2
        else:
            house.x = randint(800, 1600)
            score += 1
            
        if tree.right > balloon.x:
            tree.x -= 2
        else: 
            tree.x = randint(800, 1600)
            score += 1
            
        if balloon.top < 0 or balloon.bottom > 560:
            game_over = True
            update_high_scores()
            
        if balloon.collidepoint(bird.x, bird.y) or \
           balloon.collidepoint(house.x, house.y) or \
           balloon.collidepoint(tree.x, tree.y):
               if health > 0:
                   health -= 1
                   if health == 0 and lives > 0:
                       lives -=1
                       health = 100
                   elif health == 0 and lives == 0:
                       alive = False
                       game_over = True
                       update_high_scores()
            
pgzrun.go()


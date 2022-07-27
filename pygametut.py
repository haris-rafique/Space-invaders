# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 14:07:01 2022

@author: Admin
"""

import pygame 
import random
import math

from pygame import mixer
pygame.init()

screen=pygame.display.set_mode((800,600))

background= pygame.image.load("gameb.png")

pygame.display.set_caption("Space Invaders")

rock=pygame.image.load("rock.png")
rock=pygame.transform.scale(rock,(32,32))

rockX=200
rockY=-20

speed=5
icon= pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
bullet=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=8
bullet_state="ready"

#mixer.music.load('background.wav')
#player
playerImg=pygame.image.load("ship.png")
playerImg=pygame.transform.scale(playerImg,(64,64))

#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
numenemies=5

for i in range(numenemies):
    enemyImg1=pygame.image.load("enemy.png")
    enemyImg1=pygame.transform.scale(enemyImg1,(64,64))
    enemyImg.append(enemyImg1)
    enemyX.append(random.randint(0,739))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(50)

playerX= 370

playerY= 480

playerX_change=0
score=0
font=pygame.font.Font('freesansbold.ttf',32)
font1=pygame.font.Font('freesansbold.ttf',64)

def displayscore(x,y):
    scoreval=font.render("Score: "+str(score),True,(255,255,255))
    screen.blit(scoreval,(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))
    
def rocks(x,y):
    screen.blit(rock,(x,y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet,(x+16,y+10))
    

def rockcollision(rockX,rockY,playerX,playerY):
    distance=math.sqrt((math.pow(rockX-playerX,2)) + (math.pow(rockY-playerY,2)))
    #print(distance)
    if distance <=25:
        return True
    else:
        return False
    

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    #print(distance)
    if distance <=30:
        return True
    else:
        return False
    
def game_over():
    scoreval=font1.render("GAME OVER",True,(255,255,255))
    screen.blit(scoreval,(200,300))
    
rockX=random.randint(0,780)
running=True
while running:
    #screen.fill((0,0,0))
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -speed
            if event.key == pygame.K_RIGHT:
                playerX_change=speed
            if event.key == pygame.K_SPACE:
                bulletsound=mixer.Sound('laser.wav')
                bulletsound.play()
                bulletX=playerX  #variable value saved at this time; player X is independent of bulletX value
                fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change =0

    if playerX <=0:
        playerX=0
    if playerX>=740:
        playerX=740
        
        
    if bullet_state =="fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    rockY+=6
    if rockY>=850:
        rockY= -10
        rockX=random.randint(0,780)
   
    rocks(rockX,rockY)
    rockcoll=rockcollision(rockX,rockY,playerX,playerY)
    if rockcoll:
        for j in range(numenemies):
            enemyY[j]=2000
        game_over()
        running=False
    for i in range(numenemies):
        
        if enemyY[i]>=440:
            for j in range(numenemies):
                enemyY[j]=2000
                #rockY=2000
            #rockX=-200
            
            game_over()
            
            break
            #rockY=2000
        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=speed  #originally 4!!
        if enemyX[i]>=740:
            enemyX_change[i]=-speed
        if enemyX[i]<=0 or enemyX[i]>=740:
            enemyY[i]+=enemyY_change[i]
        
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            expsound=mixer.Sound('explosion.wav')
            expsound.play()
            bulletY=480
            bullet_state ="ready"
            score+=1
            #print(score)
            enemyX[i]=random.randint(0,739)
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)
    

    
    
        
    
        
    playerX+=playerX_change
    player(playerX,playerY)
    
    displayscore(10,10)
    pygame.display.update()
    
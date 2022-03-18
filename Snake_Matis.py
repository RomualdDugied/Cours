import pygame
import time
import random

pygame.init()
 
black = (0, 0, 0)
red = (213, 50, 80)
green = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
white = (255,255,255)
 
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake a l'ancienne")

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15


font_style = pygame.font.SysFont(None, 30)
score_font = pygame.font.SysFont(None, 30)

def menu(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/2, dis_height/3])

def menu3(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/3, dis_height/2.25])

def Yscore(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])

def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])
 
loose = False

def gameLoop():
    global loose
    global snake_speed
    game_over = False
    dir = ""
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Taille = 1
    score = 0
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
 
    while not game_over:

        for event in pygame.event.get():                   
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    if dir != "right":
                        dir = "left"
                        x1_change = -snake_block
                        y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    if dir != "left":
                        dir = "right"
                        x1_change = snake_block
                        y1_change = 0
                elif event.key == pygame.K_UP:
                    if dir != "down":
                        dir = "up"
                        y1_change = -snake_block
                        x1_change = 0
                elif event.key == pygame.K_DOWN:
                    if dir!= "up":
                        dir = "down"
                        y1_change = snake_block
                        x1_change = 0

        if x1 >= dis_width:
            loose = True
        elif x1 <= 0:
            loose = True
        elif y1 >=dis_height:
            loose = True
        elif y1 <= 0:
            loose = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)


        if len(snake_List) > Taille:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                loose = True
                
        snake(snake_block, snake_List)
        Yscore(Taille - 1)
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Taille += 1 
            score = score+1

        if score > 5:
            snake_speed = 15
        if score > 10:
            snake_speed = 20
        if score > 15:
            snake_speed = 25
        if score > 20:
            snake_speed = 30
        if score > 25:
            snake_speed = 35          

        while loose == True:
            dis.fill(black)
            menu("Perdu", white)
            menu3("appuie sur [SPACE] pour rejouer",white)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        loose = False
                        gameLoop()
            pygame.display.update()
    
        clock.tick(snake_speed)

    pygame.quit()
    quit()
 
gameLoop()
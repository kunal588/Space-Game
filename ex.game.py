import pygame
import random
import pygame_menu
from pygame import mixer
pygame.init()
clock=pygame.time.Clock()
FPS=60
screen=pygame.display.set_mode((1301,625))
title_size=25
font=pygame.font.SysFont("freesansbold",32)

start_ticks=pygame.time.get_ticks()
background=pygame.image.load("bg.jpg") 
mixer.music.load("bg_music.mp3") 
mixer.music.play(-1)

'''score board'''
def score_board(x,y,score):
    score_val=font.render("SCORE : " + str(score),True,(223,223,223))
    screen.blit(score_val,(x,y))
    food_val=font.render("STRENGTH : " + str(main_player.food),True,(223,223,223))
    screen.blit(food_val,(x,y+30))
textX=10
textY=10
final_score_font=pygame.font.SysFont("freesansbold",64)


'''gave over screen'''
def game_over_text(score):
        res1=final_score_font.render("SCORE : " + str(score),True,(223,223,223))
        screen.blit(res1,(500,304))
'''used grid for intitial easy implementation'''
def grid():
    for i in range(0,26):
        pygame.draw.line(screen,(0,255,255),(0,i*title_size),(1300,i*title_size))
    for i in range(0,53):    
        pygame.draw.line(screen,(0,255,255),(i*title_size,0),(i*title_size,650))


'''player class is for the player containing update,collision methods'''
class Player:
    def __init__(self,x,y):
        img=pygame.image.load('Asset 5.png')
        self.image=pygame.transform.scale(img,(50,25))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.food=20

    def update(self):
        dx=0
        dy=-1
        key= pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx=-5
        if key[pygame.K_RIGHT]:
            dx=5
        self.rect.x+=dx
        self.rect.y+=dy
        screen.blit(self.image,self.rect)
    def collision(self):
        if pygame.sprite.spritecollide(self,p_food_group,True):
            self.food+=1

        #speed -10 ki de raha hu
        if pygame.sprite.spritecollide(self,p_decspeed_group,False):
           y=-100
           dy=5
           while(y!=0):
               self.rect.y+=dy
               y+=dy
        if pygame.sprite.spritecollide(self,p_kill_group,True):
           self.food-=10



   
'''platform1 represents enemies'''
class platform1(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        p1img=pygame.image.load('Asset 2.png')
        self.image=pygame.transform.scale(p1img,(75,25))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def update(self):
        dy=1
        self.rect.y+=dy
        screen.blit(self.image,self.rect)

'''platform2 represents strength boosters'''
class platform2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        p1img=pygame.image.load('Asset 3.png')
        self.image=pygame.transform.scale(p1img,(75,25))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
    def update(self):
        dy=1
        self.rect.y+=dy
        screen.blit(self.image,self.rect)
def uniform_random(total):
    ran=0
    for i in range(total):
        ran+=random.randint(0,1)
    return ran  

'''platform3 represents springs to help player to move downwards'''
class platform3(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        p1img=pygame.image.load('Asset 4.png')   
        self.image=pygame.transform.scale(p1img,(75,25))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def update(self):
        dy=1
        self.rect.y+=dy
        screen.blit(self.image,self.rect)



'''function to generate multiple platfoms of all kinds'''
def multiple(y):
        type_list=[]
        total= random.randint(1,4)
        t1=uniform_random(total)
        t2=uniform_random(total-t1)
        t3=total-t1-t2
        type_list.append(t1)
        type_list.append(t2)
        type_list.append(t3)
        random.shuffle(type_list)
        x_list=[]
        x_list.append(random.randrange(25,1200))
        for i in range(total-1):
            match = True
            while(match):
                k=random.randrange(25,1200)
                count=0
                for j in x_list:
                    if(abs(j-k)>200):
                        count+=1
                    else:
                        break 
                if(count==len(x_list)):
                    x_list.append(k)
                    match=False  
        print(len(x_list))          
        for i in range(type_list[0]):
            platform1_ins= platform1(x_list[i], y)
            p_group.add(platform1_ins)
            p_kill_group.add(platform1_ins)
        for i in range(type_list[1]):
            platform2_ins= platform2(x_list[i+type_list[0]], y)
            p_group.add(platform2_ins)
            p_food_group.add(platform2_ins)
        for i in range(type_list[2]):
            platform3_ins= platform3(x_list[i+type_list[0]+type_list[1]], y)
            p_group.add(platform3_ins)
            p_decspeed_group.add(platform3_ins)

         
p_kill_group=pygame.sprite.Group()
p_decspeed_group=pygame.sprite.Group()
p_food_group=pygame.sprite.Group()   
p_group=pygame.sprite.Group(p_kill_group,p_decspeed_group,p_food_group)
main_player=Player(650,600)
def run():
    running=True    
    


    inc_y =-100
    while running:
        multiple(inc_y)
        clock.tick(FPS)
        screen.fill((0,0,0))
        screen.blit(background,(0,0))
        background.set_alpha(59)
        
        main_player.collision()
        if(main_player.food<=0 or main_player.rect.y==0):
            game_over_text(score) 
        else:
            main_player.update()
            for i in p_group:
                i.update()
            '''grid()'''
            inc_y-=100
            score=(pygame.time.get_ticks()-start_ticks)
            score_board(textX,textY,score)
        for event in pygame.event.get():
                if(event.type==pygame.QUIT):
                    running=False
        pygame.display.update()

menu = pygame_menu.Menu('Space_Game', 400, 300,
                       theme=pygame_menu.themes.THEME_SOLARIZED)

'''menu.add.text_input('Name :', default='Enter_Name')'''
menu.add.button('Play', run)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
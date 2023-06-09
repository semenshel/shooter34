##создай игру "Лабиринт"!
from pygame import *
from random import randint
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)





class Player_1(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_DOWN] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_heigth:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            lost = lost + 1







class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_heigth:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_heigth = 500
window = display.set_mode((win_width,win_heigth))
display.set_caption('Шутер')
background =  transform.scale(image.load('backgr22.png'),(win_width,win_heigth))




font.init()
font= font.Font(None,70)
win = font.render('YOU WIN!',True,(255,255,255))
lose = font.render('YOU LOSE!',True,(180,0,0))



img_enemy = "ufo.png"
img_bullet = "bullet.png"


win = font.render('YOU WIN!',True,(255,215,0))
lose = font.render('YOU LOSE!',True,(255,215,0))


player = Player('rocket.png',5, win_heigth - 80,65,65,4)
player_1 = Player_1('rocket.png',5, win_heigth - 80,65,65,4)
asteroids = sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    asteroid = Asteroid('asteroid.png', randint(80,win_width - 80,),-40,80,50,randint(1,3))


    monster = Enemy(img_enemy, randint(80,win_width - 80,),-40,80,50,randint(1,5))

    monsters.add(monster)
    asteroids.add(asteroid)

bullets = sprite.Group()
#asteroids = sprite.Group()

mixer.init()
mixer.music.load('new_music.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')



score = 0
lost = 0
goal = 10
max_lost = 3
life = 3

speed = 10
clock = time.Clock()
FPS = 60

game = True
finish = False
num_fire = 0
rel_time = False


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False


        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.bull5()


                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

                    
                



    if not finish:
        window.blit(background,(0,0))

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font.render('Wait reload...',1,(150,0,0))
                window.blit(reload,(260,460))

            else:
                num_fire = 0
                rel_time = False 
        

        text = font.render('Счёт: '+ str(score),1,(255,255,255))
        window.blit(text,(10,20))

        text = font.render('Пропущено: '+ str(lost),1,(255,255,255))
        window.blit(text,(10,50))
        if life == 1:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 3:
            life_color = (150,0,0)

        text_life = font.render(str(life),1,life_color)
        window.blit(text_life,(650,10))





        collides =  sprite.groupcollide(monsters, bullets,True,True)
        for c in collides:
            score  = score + 1
            monster = Enemy(img_enemy, randint(80,win_width - 80),
            -40,80,50,randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(player,monsters,False,) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score >= goal:
            finish = True
            window.blit(win,(200,200))

        if sprite.spritecollide(player,monsters,False) or sprite.spritecollide(player,asteroids,False):
            sprite.spritecollide(player,monsters,True)
            sprite.spritecollide(player,asteroids,True)
            life = life - 1

        if life ==0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))


        

        
        player_1.reset()
        player_1.update()

    
        asteroids.draw(window)
        asteroids.update()


        monsters.update()
        player.update()
        bullets.update()



        
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        display.update()
    
    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        num_fire = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)

        for i in range(1,6):

            monster = Enemy(img_enemy, randint(80,win_width - 80,),-40,80,50,randint(1,5))
            monsters.add(monster)


        clock.tick(FPS)
    time.delay(50)
    

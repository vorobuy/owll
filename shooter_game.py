from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((1000,700))
display.set_caption("Errrrr")
fon = transform.scale(image.load('galaxy.jpg'),(1000,700))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_music = mixer.Sound('fire.ogg')

font.init()
font = font.SysFont('Arial',35)
score = 0
miss = 0
class Game_Sprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y,size_x,size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(Game_Sprite):
    def control(self):
        buttons = key.get_pressed()
        if buttons[K_a] and self.rect.x>5:
            self.rect.x-= self.speed
        if buttons[K_d] and self.rect.x<920:
            self.rect.x+= self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.x+50,self.rect.y,15,20,15)
        bullets.add(bullet)
class Enemy(Game_Sprite):
    def update(self):
        global miss 
        self.rect.y += self.speed
        global miss
        if self.rect.y > 700:
            miss += 1
            self.rect.y = 0
            self.rect.x = randint(0,920)
class Enemy_1(Game_Sprite):
    def update(self):
        global miss 
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(0,920)
class Bullet(Game_Sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
game = True
finish = False
clock = time.Clock()
Vanechkin = Player('rocket.png',480,580,100,100,10)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy_1('asteroid.png',randint(80,920),0,80,80,randint(1,3))
    asteroids.add(asteroid)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png',randint(0,920),0,80,80,randint(2,7))
    monsters.add(monster)
kol_bullets = 0
r = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if kol_bullets < 10 and r == False:
                    kol_bullets += 1
                    fire_music.play()
                    Vanechkin.fire()
                if kol_bullets >= 10 and r == False:
                    start_t = timer()
                    r = True
    if finish != True:
        window.blit(fon,(0,0))
        score_text = font.render('Счет: '+str(score),True,(255,255,255))
        miss_text = font.render('Пропущено: '+str(miss),True,(255,255,255))
        window.blit(score_text,(10,10))
        window.blit(miss_text,(10,55))
        Vanechkin.reset()
        Vanechkin.control()
        monster.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.draw(window)
        asteroids.update()
        if r == True:
            end_t = timer()
            if end_t-start_t < 2:
                text_r = font.render('Не гони',True,(255,255,255))
                window.blit(text_r,(500,350))
            else:
                r = False
                kol_bullets = 0

        if sprite.spritecollide(Vanechkin,monsters,False) or sprite.spritecollide(Vanechkin,asteroids,False) or miss>=20:
            finish = True
            text_lose = font.render('Емае',True,(255,255,255))
            window.blit(text_lose,(500,350))
        babah = sprite.groupcollide(bullets,monsters,True,True)
        for c in babah:
            score += 1
            monster = Enemy('ufo.png',randint(0,920),0,80,80,randint(2,7))
            monsters.add(monster)
        if score >=10:
            finish = True
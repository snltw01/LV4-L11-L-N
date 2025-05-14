import pygame
import random, time
pygame.init()

sc_w=800
sc_h=600
sc=pygame.display.set_mode((sc_w,sc_h))
pygame.display.set_caption('Plane game')
pygame.mixer.init()
pygame.mixer.music.load('music/bg.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)
gun_sound=pygame.mixer.Sound('music/3zgun.mp3')
explosion_sound=pygame.mixer.Sound('music/explosion.mp3')
 
bg_IMG=pygame.image.load('IMG/bg.png')
bg_IMG=pygame.transform.scale(bg_IMG,(sc_w,sc_h))

win_IMG=pygame.image.load('IMG/win.png')
win_IMG=pygame.transform.scale(win_IMG,(500,500))

lose_IMG=pygame.image.load('IMG/lose.png')
lose_IMG=pygame.transform.scale(lose_IMG,(500,500))

bullet_IMG=pygame.image.load('IMG/bullet.png')
bullet_IMG=pygame.transform.scale(bullet_IMG,(10,51))
bullet_IMG=pygame.transform.rotate(bullet_IMG,-90)

shield_IMG=pygame.image.load('IMG/shield.png')
shield_IMG=pygame.transform.scale(shield_IMG,(62,63))

eny_bullet_IMG=pygame.image.load('IMG/enermy_bullet.png')
eny_bullet_IMG=pygame.transform.scale(eny_bullet_IMG,(50,50))
eny_bullet_IMG=pygame.transform.rotate(eny_bullet_IMG,180)

meteorite_IMG=pygame.image.load('IMG/enermy.png')
meteorite_IMG=pygame.transform.scale(meteorite_IMG,(70,103))
meteorite_IMG=pygame.transform.rotate(meteorite_IMG,90)

enermy_IMG=pygame.image.load('IMG/enermy.png')
enermy_IMG=pygame.transform.scale(enermy_IMG,(70,103))
enermy_IMG=pygame.transform.rotate(enermy_IMG,90)

explosion_IMG=pygame.image.load('IMG/explosion.png')
explosion_IMG=pygame.transform.scale(explosion_IMG,(70,103))

player_IMG=pygame.image.load('IMG/plane.png')
player_IMG=pygame.transform.scale(player_IMG,(50,50))
player_IMG=pygame.transform.rotate(player_IMG,-90)

black=(0,0,0)
white=(255,255,255)
running=True
bullet_ready="ready"
score=0
level=1
timer=0
speed=5

class meteorite(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=meteorite_IMG
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
    def update(self):
        self.rect.y+=10
      
        print(self.rect.bottomleft)
        if self.rect.top>sc_h:
            self.kill()
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=player_IMG
        self.rect=self.image.get_rect()
        
    def update(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x-=5

        if keys[pygame.K_RIGHT]:
            self.rect.x+=5
        
        if self.rect.right>sc_w:
            self.rect.x=sc_w-50

        if self.rect.left<0:
            self.rect.x=0

        if keys[pygame.K_DOWN]:
            self.rect.y+=speed

        if keys[pygame.K_UP]:
            self.rect.y-=speed

        if self.rect.top<0:
            self.rect.y=0

        if self.rect.bottom>sc_h:
            self.rect.y=sc_h-50


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=bullet_IMG
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
    def update(self):
        self.rect.x+=10
        print(self.rect.left)
        if self.rect.left>1000:
            self.kill()

class eny_Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=eny_bullet_IMG
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
    def update(self):
        self.rect.x-=10
        print(self.rect.right)
        if self.rect.left<0:
            self.kill()

class shield(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.image=shield_IMG
        self.rect=self.image.get_rect()
        self.player=player
        self.time_shield=pygame.time.get_ticks()
    def update(self):
        self.rect.center = self.player.rect.center
        now_time = pygame.time.get_ticks()
        if now_time - self.time_shield > 3000:
            self.kill()

class enermy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed=speed
        self.image=enermy_IMG
        self.rect=self.image.get_rect()
        self.rect.x=sc_w
        self.rect.y=random.randint(70,sc_h-70)
    
    def update(self):
        self.rect.x-=self.speed
        if self.rect.right<0:
            self.kill()

class explosion(pygame.sprite.Sprite):
    def __init__(self,center):
        super().__init__()
        self.image=explosion_IMG
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.time_start=pygame.time.get_ticks()

    def update(self):
        now_time=pygame.time.get_ticks()
        if now_time- self.time_start>=300:
            self.kill()
font=pygame.font.Font(None,40)
clock=pygame.time.Clock()
plane=Player()
eny=enermy()
all_gp=pygame.sprite.Group()
all_gp.add(plane)
bullet_gp=pygame.sprite.Group()
enermy_gp=pygame.sprite.Group()
eny_bullet_gp=pygame.sprite.Group()
meteorite_gp=pygame.sprite.Group()
shield_gp = pygame.sprite.Group()

timer=0
bg_x=0
bg_y=0
valocity_x=1
valocity_y=5
shield_active=False
def start_screen():
    title_font=pygame.font.Font(None,80)
    title_text=title_font.render('Plane game',True,white)
    title_rect=title_text.get_rect(center=(sc_w/2,sc_h/2))
    start_font=pygame.font.Font(None,35)
    start_text=start_font.render("Enter to play the game",True,white)
    start_rect=start_text.get_rect(center=(sc_w/2,sc_h/2+100))
    
    
    waiting=True
    while waiting:

        print('bd')
        sc.blit(title_text,title_rect)
        sc.blit(start_text,start_rect)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                waiting=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    waiting=False
        pygame.display.update()
start_screen()

while running:
    
    if score>=20:
        level=3
    
    if score>=0 and score<10:
        level =1
    if score>=10 and score<20:
        level=2
        
    
    if random.random()<0.08:
        bullet_ready="ready"
    


    clock.tick(60)
    sc.blit(bg_IMG,(bg_x,bg_y))
    sc.blit(bg_IMG,(bg_x+800,bg_y))
    


    if timer>30:
        Enermy=enermy()
        all_gp.add(Enermy)
        enermy_gp.add(Enermy)
        timer=00000
    timer+=1
    bg_x-=valocity_x
    if bg_x+600<0:
        bg_x=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if bullet_ready == "ready":
                if event.key == pygame.K_0:
                    gun_sound.play()
                    bullet = Bullet(plane.rect.right, plane.rect.centery)
                    bullet_gp.add(bullet)
                    all_gp.add(bullet)
                    print("bullet")
                    bullet_ready = "reload"
            if event.key == pygame.K_e:
                shield_active = True
                shield_1 = shield(plane)
              
                shield_gp.add(shield_1)  # để vẽ sau cùng
         

    if score==40:
        sc.blit(win_IMG,(sc_w//2-250,sc_h//2-250))
        pygame.display.update()
        continue
    if score<0:
        sc.blit(lose_IMG,(sc_w//2-250,sc_h//2-250))
        pygame.display.update()
        continue
 
    
    if level>=2:
        for Enermy in enermy_gp:
            if random.random()<0.01:
                eny_bullet=eny_Bullet(Enermy.rect.left,Enermy.rect.centery)
                eny_bullet_gp.add(eny_bullet)
                all_gp.add(eny_bullet)

    if level ==3:
        if random.random() < 0.02:
            meteorite_NPC = meteorite(random.randint(0, sc_w - 70), 0)
            meteorite_gp.add(meteorite_NPC)
            all_gp.add(meteorite_NPC)
    if shield_active==False:
        if pygame.sprite.spritecollide(plane,enermy_gp,True):
            explosion_sound.play()
            score-=1

        if pygame.sprite.spritecollide(plane,meteorite_gp,True):
            explosion_sound.play()
            score-=1

        if pygame.sprite.spritecollide(plane,eny_bullet_gp,True):
            explosion_sound.play()
            score-=1
    if shield_active==True:
        if pygame.sprite.spritecollide(plane,enermy_gp,False):
            explosion_sound.play()

        if pygame.sprite.spritecollide(plane,meteorite_gp,False):
            explosion_sound.play()


        if pygame.sprite.spritecollide(plane,eny_bullet_gp,False):
            explosion_sound.play()
 

    if pygame.sprite.groupcollide(bullet_gp,eny_bullet_gp,True,True):
        explosion_sound.play()

    if pygame.sprite.groupcollide(bullet_gp,meteorite_gp,True,True):
        explosion_sound.play()
  
    if pygame.sprite.groupcollide(eny_bullet_gp,meteorite_gp,True,True):
        explosion_sound.play()
    

        
    hits=pygame.sprite.groupcollide(bullet_gp,enermy_gp,True,True)
    for hit in hits:
        Explosion=explosion(hit.rect.center)
        all_gp.add(Explosion)
        explosion_sound.play()
        score+=1
    if shield_active==False:
        now =pygame.time.get_ticks()
        # if now-use>= 6000:
        #     shield_active=True
    # Kiểm tra xem khiên có còn tồn tại không
    if not shield_gp:  # Nếu shield_gp rỗng (không còn sprite khiên)
        shield_active = False

    score_text=font.render("Score: "+str(score),True,black)
    lv_text=font.render("Level: "+str(level),True,black)
    ready_bullet=font.render("Bullet: "+str(bullet_ready),True,black)
    sc.blit(score_text,(10,10))
    sc.blit(lv_text,(150,10))
    sc.blit(ready_bullet,(600,10))
    shield_gp.update()
    shield_gp.draw(sc)
    all_gp.update()
    all_gp.draw(sc)
    
    pygame.display.update()

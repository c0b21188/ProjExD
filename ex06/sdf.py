import pygame as pg
import sys
import random


p_damage = None#プレイヤーがダメージを受けた際のSE
p_shoot = None#プレイヤーのショットSE
e_down = None#敵を倒した際のSE

class Screen:
    def __init__(self, title, wh, image):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)     # Surface
        self.rct = self.sfc.get_rect()         # Rect
        self.bgi_sfc = pg.image.load(image)    # Surface
        self.bgi_rct = self.bgi_sfc.get_rect() # Rect
        self.plane_mini_img = pg.image.load('ex06/png/01.png')
        self.plane_mini_img = pg.transform.scale(self.plane_mini_img,(50,35))
        # self.plane_mini_img.set_colorkey((255,255,255))

        # planeImg2 = pygame.image.load("plane.png").convert()
        # colorkey = planeImg2.get_at((0,0))  # 左上の色を透明色に
        # planeImg2.set_colorkey(colorkey, RLEACCEL)
        
        self.lives = 3
    def draw_lives(self,screen,x,y):
        for i in range(self.lives):
            img_rect = self.plane_mini_img.get_rect()
            img_rect.x = x + 55 * i
            img_rect.y = y
            screen.blit(self.plane_mini_img,img_rect)
        
    
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)
        
class Zanki:
    def __init__(self, image:str,size: float, vxy):
        self.sfc = pg.image.load(image) 
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)
        self.rct = self.sfc.get_rect() # Rect
        self.vx, self.vy = vxy
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
    def update(self, scr: Screen):
        
        # 練習7
         
        # 練習5
        self.blit(scr)


class Bird:
    def __init__(self, image: str, size: float, xy):
        self.sfc = pg.image.load(image)    # Surface
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)  # Surface
        self.rct = self.sfc.get_rect()          # Rect
        self.rct.center = xy

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        key_states = pg.key.get_pressed() # 辞書
        if key_states[pg.K_UP]: 
            self.rct.centery -= 1
        if key_states[pg.K_DOWN]: 
            self.rct.centery += 1
        if key_states[pg.K_LEFT]: 
            self.rct.centerx -= 1
        if key_states[pg.K_RIGHT]: 
            self.rct.centerx += 1
        # # 練習7
        if check_bound(self.rct, scr.rct) != (1, 1): # 領域外だったら
            if key_states[pg.K_UP]: 
                self.rct.centery += 1
            if key_states[pg.K_DOWN]: 
                self.rct.centery -= 1
            if key_states[pg.K_LEFT]: 
                self.rct.centerx += 1
            if key_states[pg.K_RIGHT]: 
                self.rct.centerx -= 1
        self.blit(scr)
        
    


class Bomb:
    def __init__(self, color, size, vxy, scr: Screen):
        self.sfc = pg.Surface((2*size, 2*size)) # Surface
        self.sfc.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.sfc, color, (size, size), size)
        self.rct = self.sfc.get_rect() # Rect
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 練習6

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        # 練習6
        self.rct.move_ip(self.vx, self.vy)
        # 練習7
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate   
        # 練習5
        self.blit(scr)          


def main():
    clock = pg.time.Clock()
    scr = Screen("逃げろ！こうかとん", (1000, 600), "fig/pg_bg.jpg")
    kkt = Bird("fig/6.png", 2.0, (900, 400))
    bkd1 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)
    bkd2 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)
    bkd3 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)


    znk = Zanki('ex06/png/01.png',0.3,(1,1))


    hoge = pg.mixer.Sound("ex06/mp3/mp3_BGM.mp3")
    hoge.play()
    while True:
        scr.blit()
        # 練習2
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        kkt.update(scr)
        bkd1.update(scr)
        bkd2.update(scr)
        bkd3.update(scr)
        znk.update(scr)
        if kkt.rct.colliderect(bkd1.rct):
            hit_music = pg.mixer.Sound("ex06/mp3/hit.mp3")
            hit_music.play()
            return
        if kkt.rct.colliderect(bkd2.rct):
            hit_music = pg.mixer.Sound("ex06/mp3/hit.mp3")
            hit_music.play()
            return
        if kkt.rct.colliderect(bkd3.rct):
            hit_music = pg.mixer.Sound("ex06/mp3/hit.mp3")
            hit_music.play()
            return

        pg.display.update()
        clock.tick(500)


# 練習7
def check_bound(rct, scr_rct):
    '''
    [1] rct: こうかとん or 爆弾のRect
    [2] scr_rct: スクリーンのRect
    '''
    yoko, tate = +1, +1 # 領域内
    if rct.left < scr_rct.left or scr_rct.right  < rct.right : yoko = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom: tate = -1 # 領域外
    return yoko, tate


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

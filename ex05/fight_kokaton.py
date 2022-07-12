import pygame as pg
import sys
import random


class Screen:
    def __init__(self, title, wh, image):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)     # Surface
        self.rct = self.sfc.get_rect()         # Rect
        self.bgi_sfc = pg.image.load(image)    # Surface
        self.bgi_rct = self.bgi_sfc.get_rect() # Rect

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


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

    def attack(self):
        return Shot(self) 


class Bomb:
    colors = [(255, 0, 0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
    def __init__(self, size, vxy, scr: Screen):
        #color = random.choice(Bomb.colors)
        #vx = random.choice([-1, +1])
        #vy = random.choice([-1, +1])
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
        self.rct.move_ip(+1,0)
        if check_bound(self.rct, scr.rct) != (1,1):
            del self 
        self.blit(scr) 


class Shot:
    dire = {
            pg.K_f: [-1, 0,180], #左に発射
            pg.K_j: [+1, 0,0], #右に発射
            pg.K_v: [0, +1,-90], #下に発射
            pg.K_m: [0, -1,+90], #上に発射
    }

    def __init__(self, chr: Bird, key):
        self.sfc = pg.image.load("fig/beam.png")
        self.sfc = pg.transform.rotozoom(self.sfc, Shot.dere[key][2], 0.1)
        self.sfc = self.sfc.get_rect()
        self.rct.midleft = chr.rct.center
        self.vx,self.vy = Shot.dire[key][0],Shot.dire[key][1]

    def blit(self, scr: Screen):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)
                

def main():
    clock = pg.time.Clock()
    scr = Screen("逃げろ！こうかとん", (1600, 900), "fig/pg_bg.jpg")
    kkt = Bird("fig/6.png", 2.0, (900, 400))
    #bkd = Bomb((255,0,0), 10, (+1,+1), scr)

    beams = [] 
    #bombs = [Bomb for _ in range(5)]
        
    bombs = [Bomb((255,0,0), 10, (+1,+1), scr) for _ in range()]

    while True:
        scr.blit()

        # 練習2
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if event.type == pg.KEYDOWN:
                beam = kkt.attack() #スペースキーが押されたらこうかとんがビームを打つ

        kkt.update(scr)
        bkb.update(scr)
        for bkb in beams:
            bkb.update(scr)
        if kkt.rct.colliderect(bkd.rct):
            return

        if len(beams) != 0:
            for beams in beams:
                beams.update(scr)
                for b, bomb in enumerate(bombs):
                    if bombs[b].rct.colliderect(beams.rct):
                        del bombs[b]
       
        pg.display.update()
        clock.tick(1000)


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

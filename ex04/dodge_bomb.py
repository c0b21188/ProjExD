import pygame as pg
import sys
import random

def main():
    clock = pg.time.Clock()
    pg.display.set_caption("逃げろ！こうかとん")
    screen_sfc = pg.display.set_mode((1000,600)) #Surface
    screen_rct = screen_sfc.get_rect() #Rect
    bgimg_sfc = pg.image.load("fig/平原.jpg") #Surface
    bgimg_rct = bgimg_sfc.get_rect() #Rect
    screen_sfc.blit(bgimg_sfc, bgimg_rct)

    #練習3
    kkimg_sfc = pg.image.load("fig/6.png")
    kkimg_sfc = pg.transform.rotozoom(kkimg_sfc, 0, 2.0) #Surface
    kkimg_rct = kkimg_sfc.get_rect() #Rect
    kkimg_rct.center = 900,400
    

    #練習5：爆弾
    bmimg_sfc = pg.Surface((20,20)) #Surface
    bmimg_sfc.set_colorkey((0,0,0))

    pg.draw.circle(bmimg_sfc, (255, 0, 0), (10, 10), 10)
    bmimg_rct = bmimg_sfc.get_rect() #Rect
    bmimg_rct.centerx = random.randint(0, screen_rct.width)
    bmimg_rct.centery = random.randint(0, screen_rct.height)
    vx,vy = +1, +1 #練習6

    bmimg_sfc2 = pg.Surface((20,20)) #Surface
    bmimg_sfc2.set_colorkey((0,0,0))

    pg.draw.circle(bmimg_sfc2, (0, 0, 255), (10, 10), 10)
    bmimg_rct2 = bmimg_sfc2.get_rect() #Rect
    bmimg_rct2.centerx = random.randint(10, screen_rct.width)
    bmimg_rct2.centery = random.randint(200, screen_rct.height)
    vx2,vy2 = +1, +1

    while True:
        screen_sfc.blit(bgimg_sfc, bgimg_rct)
        

        #練習2
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        #練習4
        key_states = pg.key.get_pressed() #辞書
        if key_states[pg.K_UP] == True: kkimg_rct.centery -= 1
        if key_states[pg.K_DOWN] == True: kkimg_rct.centery += 1
        if key_states[pg.K_LEFT] == True: kkimg_rct.centerx -= 1
        if key_states[pg.K_RIGHT] == True: kkimg_rct.centerx += 1
        if check_bound(kkimg_rct, screen_rct) != (1, 1):
            if key_states[pg.K_UP] == True: kkimg_rct.centery += 1
            if key_states[pg.K_DOWN] == True: kkimg_rct.centery -= 1
            if key_states[pg.K_LEFT] == True: kkimg_rct.centerx += 1
            if key_states[pg.K_RIGHT] == True: kkimg_rct.centerx -= 1 
        screen_sfc.blit(kkimg_sfc, kkimg_rct)

        
        #練習6
        bmimg_rct.move_ip(vx,vy)
        bmimg_rct2.move_ip(vx2,vy2)
        #練習5
        screen_sfc.blit(bmimg_sfc, bmimg_rct)
        screen_sfc.blit(bmimg_sfc2,bmimg_rct2)
        #練習7
        yoko, tate = check_bound(bmimg_rct, screen_rct)
        vx *= yoko
        vy *= tate

        yoko, tate = check_bound2(bmimg_rct2, screen_rct)
        vx2 *= yoko
        vy2 *= tate
        
        if kkimg_rct.colliderect(bmimg_rct): 
            print("gameover")
            return #こうかとん目線
        if kkimg_rct.colliderect(bmimg_rct2):
            print("gameover")
            return #こうかとん目線
        #if bmimg_rct.colliderect(kkimg_rct): return #爆弾目線
        pg.display.update()
        clock.tick(300)

def open():
    endFlag = False
    #フォントとテキストの設定
    font1 = pg.font.SysFont(None, 80)
    text1 = font1.render("Jump the Rope", False, (255,255,255))
    font2 = pg.font.SysFont(None, 40)
    text2 = font1.render("Press Any Key to Start", False, (255,255,255))
    screen_sfc3 = pg.display.set_mode((1000,600)) #Surface
    screen_rct3 = screen_sfc3.get_rect()

    while endFlag == False:
        screen_sfc.fill((0,0,0))
        #上で設定したテキストを表示
        screen_sfc.blit(text1,(30,50))
        screen_sfc.blit(text2,(20,150))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:  
                endFlag = True
            elif event.type == pg.KEYDOWN:
                #もしも何かしらのキーが押されたら、メイン関数を呼び出す
                endFlag = True
                main()

#練習7
def check_bound(rct, scr_rct):
    '''
    [1] rct:こうかとんor爆弾のRect
    [2] scr_rct:スクリーンのRect
    '''
    yoko, tate = +1, +1 #領域内
    if rct.left < scr_rct.left or scr_rct.right < rct.right: yoko = -1 #領域外
    if rct.top < scr_rct.top or scr_rct.bottom < rct.bottom: tate = -1 #領域外
    return yoko, tate

def check_bound2(rct2, scr_rct2):
    '''
    [1] rct:こうかとんor爆弾のRect
    [2] scr_rct:スクリーンのRect
    '''
    yoko, tate = +1, +1 #領域内
    if rct2.left < scr_rct2.left or scr_rct2.right < rct2.right: yoko = -1 #領域外
    if rct2.top < scr_rct2.top or scr_rct2.bottom < rct2.bottom: tate = -1 #領域外
    return yoko, tate




if __name__ == "__main__":
    pg.init()
    main() #これから実装するゲームのメイン部分
    pg.quit()
    sys.exit() 
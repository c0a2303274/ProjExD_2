import os
from random import randint as ri
import sys
import pygame as pg


WIDTH, HEIGHT = 900, 600
DXY = {
    pg.K_UP: [0, -5],
    pg.K_DOWN: [0, +5], 
    pg.K_LEFT: [-5, 0],
    pg.K_RIGHT: [+5, 0],
}
# 移動量辞書


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    bb_s = pg.Surface((20, 20))
    bb = pg.draw.circle(bb_s, (255, 0, 0), (10, 10), 10)
    bb_s.set_colorkey((0, 0, 0))
    bb.center = ri(0, WIDTH), ri(0, HEIGHT)
    kk_rct.center = WIDTH / 2, HEIGHT / 2
    clock = pg.time.Clock()
    tmr = 0
    vx = +5
    vy = +5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DXY.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        bb.move_ip(+vx, +vy)
        kk_j = D_Judg(kk_rct)
        if kk_j != [True, True]:
            kk_rct.move_ip((-sum_mv[0], -sum_mv[1]))
        bb_j = D_Judg(bb)
        if not bb_j[0]:
            vx *= -1
        if not bb_j[1]:
            vy *= -1
        
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_s, bb)
        pg.display.update()
        tmr += 1
        clock.tick(50)

def D_Judg(rct:pg.Rect):
    width, hight = True, True
    if rct.left < 0 or rct.right > WIDTH:
        width = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        hight = False
    return [width, hight]

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
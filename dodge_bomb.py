import os
from random import randint as ri
import sys
import pygame as pg


WIDTH, HEIGHT = 900, 600
DXY = {# 移動量辞書
    pg.K_UP: [0, -5],
    pg.K_DOWN: [0, +5], 
    pg.K_LEFT: [-5, 0],
    pg.K_RIGHT: [+5, 0],
}


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_gg = pg.image.load("fig/8.png")
    KKg_rct = kk_gg.get_rect()
    KKg_rct.center = [2 * WIDTH / 7, HEIGHT / 2]
    kkgg_rct = kk_gg.get_rect()
    kkgg_rct.center = [5 * WIDTH / 7, HEIGHT / 2]

    bb_t = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_t.append(bb_img)
    f = 0
    # 接触のフラグ

    kk_l = kk_img
    kk_lu = pg.transform.rotozoom(kk_l, -45.0, 1.0)
    kk_r = pg.transform.flip(kk_img, True, False)
    kk_rd = pg.transform.rotozoom(kk_r, -45.0, 1.0)
    kk_d = pg.transform.rotozoom(kk_r, -90.0, 1.0)
    kk_dl = pg.transform.rotozoom(kk_d, 45.0, 1.0)
    kk_dl = pg.transform.rotozoom(kk_l, 45, 1.0)
    kk_u = pg.transform.rotozoom(kk_img, -90.0, 1.0)
    kk_ur  = pg.transform.rotozoom(kk_r, 45.0, 1.0)
    KK_ZOOM = {# 回転用の辞書
        str([0, -5]): kk_u,
        str([5, -5]): kk_ur,
        str([5, 0]): kk_r,
        str([5, 5]): kk_rd,
        str([0, 5]): kk_d,
        str([-5, 5]): kk_dl,
        str([-5, 0]): kk_l, 
        str([-5, -5]): kk_lu,
    }


    bb_s = pg.Surface((20, 20))
    bb = pg.draw.circle(bb_s, (255, 0, 0), (10, 10), 10)
    bb.center = ri(0, WIDTH), ri(0, HEIGHT)
    kk_rct.center = WIDTH / 2, HEIGHT / 2
    clock = pg.time.Clock()
    vx = +5
    vy = +5
    tmr = 0
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
                if not sum_mv == [0, 0]:
                    kk_img = KK_ZOOM[str(sum_mv)]
        kk_rct.move_ip(sum_mv)
        avx = sp_j(vx, tmr)
        avy = sp_j(vy, tmr)
        bb.move_ip(avx, avy)
        kk_j = D_Judg(kk_rct)
        if kk_j != [True, True]:
            kk_rct.move_ip((-sum_mv[0], -sum_mv[1]))
        bb_j = D_Judg(bb)
        if not bb_j[0]:
            vx *= -1
        if not bb_j[1]:
            vy *= -1
        if kk_rct.colliderect(bb):
            f = 1
        if f == 0:
            screen.blit(kk_img, kk_rct)
            bb_s = bb_t[min(tmr//500, 9)]
            bb_s.set_colorkey((0, 0, 0))
            screen.blit(bb_s, bb)
        elif f == 1:
            bl_s = pg.Surface((WIDTH, HEIGHT))
            bl_rct = pg.draw.rect(bl_s, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
            bl_s.set_alpha(200)
            screen.blit(bl_s, bl_rct)
            gm = pg.font.Font(None, 80)
            txt = gm.render("Game Over",True, (255, 255, 255))
            txt_rct = txt.get_rect()
            txt_rct.center = [WIDTH / 2, HEIGHT / 2]
            screen.blit(txt, txt_rct)
            screen.blit(kk_gg, KKg_rct)
            screen.blit(kk_gg, kkgg_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)

def D_Judg(rct:pg.Rect) -> tuple[bool, bool]:
    """
    上下左右の画面内判定
    画面内の場合True,画面外の場合Falseを返す
    """
    width, hight = True, True
    if rct.left < 0 or rct.right > WIDTH:
        width = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        hight = False
    return [width, hight]

def sp_j(d, tmr):
    accs = [a for a in range(1, 11)]
    return (d * accs[min(tmr//500, 9)])

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
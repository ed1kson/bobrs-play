import cfg
import sys
import random
import pygame as pg
from modules import *

print(cfg.BGM_PATH)

def initGame():
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((cfg.SCREENSIZE))
    pg.display.set_caption('Поймай бобра')
    return screen

def main():
    screen = initGame()
    pg.mixer.music.load(cfg.BGM_PATH)
    pg.mixer.music.play(-1)
    count_down = pg.mixer.Sound(cfg.COUNT_DOWN_SOUND_PATH)
    hammering = pg.mixer.Sound(cfg.HAMMERING_SOUND_PATH)

    font = pg.font.Font(cfg.FONT_PATH, 40)

    background = pg.image.load(cfg.GAME_BG_IMAGEPATH)

    startInterface(screen, cfg.GAME_BEGIN_IMAGEPATHS)
    hole_pos = random.choice(cfg.HOLE_POSITIONS)
    change_hole_event = pg.USEREVENT
    pg.time.set_timer(change_hole_event, 800)

    mole = Mole(cfg.MOLE_IMAGEPATHES, hole_pos)

    hammer = Hammer(cfg.HAMMER_IMAGEPATH, (500, 250))

    clock = pg.time.Clock()

    your_score = 0
    check = False

    init_time = pg.time.get_ticks()

    while True:
        time_remain = round((61000 - (pg.time.get_ticks() - init_time))/1000)
        if time_remain == 40 and not check:
            hole_pos = random.choice(cfg.HOLE_POSITIONS)
            mole.reset()
            mole.setPosition(hole_pos)
            pg.time.set_timer(change_hole_event, 650)
            check = True
        if time_remain == 20 and check:
            hole_pos = random.choice(cfg.HOLE_POSITIONS)
            mole.reset()
            mole.setPosition(hole_pos)
            pg.time.set_timer(change_hole_event, 500)
            check = False
        if time_remain == 10:
            count_down.play()
        if time_remain < 0: break
        count_down_text = font.render('Time: ' + str(time_remain), True, cfg.WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEMOTION:
                hammer.SetPosition(pg.mouse.get_pos())
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    hammer.setHammering()
            elif event.type == change_hole_event:
                hole_pos = random.choice(cfg.HOLE_POSITIONS)
                mole.reset()
                mole.setPosition(hole_pos)
        if hammer.is_hammering and not mole.is_hammering:
            is_hammer = pg.sprite.collide_mask(hammer, mole)
            if is_hammer:
                mole.setBeHammered()
                hammering.play()
                your_score += 10
            
        your_score_text = font.render('Score: ' + str(your_score), True, cfg.BROWN)

        screen.blit(background, (0, 0))
        screen.blit(count_down_text, (875, 8))
        screen.blit(your_score_text, (800, 430))
        mole.draw(screen)
        hammer.draw(screen)
        
        pg.display.flip()

    is_restart = endInterface(screen, cfg.GAME_END_IMAGEPATH, your_score, cfg.FONT_PATH, [cfg.WHITE, cfg.RED], cfg.SCREENSIZE)
    return is_restart

if __name__ == '__main__' :
    while True:
        is_restart = main()
        if not is_restart:
            break
import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
# from bullet import Bullet
import game_functions as gf
from game_stats import GameStats

def run_game():
    #initialize game and create screen object.
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    stats=GameStats(ai_settings)

    #make a ship
    ship=Ship(ai_settings,screen)

    #make a group to store bullets in.
    bullets=Group()
    aliens=Group()
    #create the fleet of aliens
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #make an alien
    alien=Alien(ai_settings,screen)

    #set the background color
    # bg_color=(230,230,230)

    #start the main loop for the game
    while True:
        #watch for keyboard and mouse events
        gf.check_events(ai_settings,screen,ship,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,ship,aliens,bullets)

run_game()

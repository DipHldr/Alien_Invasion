import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
     """check if any alien have reached the bottom of the screen"""
     screen_rect=screen.get_rect()
     for alien in aliens.sprites():
          if alien.rect.bottom >= screen_rect.bottom:
               #treat this the same as ship hit
               ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
               break

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
     """respond to ship being hit by aliens"""
     #decrement ship_left
     if stats.ship_left>0:
         stats.ship_left-=1

         #empty the list of aliens and bullets
         aliens.empty()
         bullets.empty()

         #create a new and center the ship
         create_fleet(ai_settings,screen,ship,aliens)
         ship.center_ship()

         #pause
         sleep(1)
     else:
          stats.game_active=False

def check_fleet_edges(ai_settings,aliens):
     """respond appropriately if any aliens have reached an edge"""
     for alien in aliens.sprites():
          if alien.check_edges():
               change_fleet_direction(ai_settings,aliens)
               break

def change_fleet_direction(ai_settings,aliens):
     """drop the entire fleet and change fleet's direction"""
     for alien in aliens.sprites():
          alien.rect.y+=ai_settings.fleet_drop_speed
     ai_settings.fleet_direction*=-1

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
     """update position of all aliens in the fleet"""
     """check if the fleet is at an edge and
       then update the position of all aliens in the fleet"""
     check_fleet_edges(ai_settings,aliens)
     aliens.update()
     #look for alien ship collision
     check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
     if pygame.sprite.spritecollideany(ship,aliens):
          ship_hit(ai_settings,stats,screen,ship,aliens,bullets)

def get_number_rows(ai_settings,ship_height,alien_height):
     """determine the number of rows of alien that fit on the screen"""
     available_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
     number_rows=int(available_space_y/(2*alien_height))
     return number_rows

def get_number_aliens_x(ai_settings,alien_width):
     available_space_x=ai_settings.screen_width-2*alien_width
     number_aliens_x=int(available_space_x/(2*alien_width))
     return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
 #create an alien and find the number of aliens in a row
     #spacing between each alien is equal to one alien width
     alien=Alien(ai_settings,screen)
     alien_width=alien.rect.width
     alien.x=alien_width+2*alien_width*alien_number
     alien.rect.x=alien.x
     alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
     aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
     """create full fleet of aliens"""
    
     alien=Alien(ai_settings,screen)
     number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
     number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
     #create the first row of aliens
     for row_number in range(number_rows):
         for alien_number in range(number_aliens_x):
              #create an alien and place it in a row
              create_alien(ai_settings,screen,aliens,alien_number,row_number)
          
def check_keydown_events(event,ai_settings,screen,ship,bullets):
     """respond to keypresses"""
     if event.key==pygame.K_RIGHT:
         #move ship to right
         ship.moving_right=True
     elif event.key==pygame.K_LEFT:
        ship.moving_left=True
     elif event.key==pygame.K_SPACE:
          fire_bullet(ai_settings,screen,ship,bullets)
     elif event.key==pygame.K_q:
          sys.exit()          

def fire_bullet(ai_settings,screen,ship,bullets):
      #fire bullet if limited not reached yet
     if len(bullets)<ai_settings.bullets_allowed:
          #create new bullet and add it to the bullets group
          new_bullet=Bullet(ai_settings,screen,ship)
          bullets.add(new_bullet)

def check_keyup_events(event,ship):
     """responds to key releases"""
     if event.key == pygame.K_RIGHT:
        ship.moving_right=False 
     elif event.key==pygame.K_LEFT:
         ship.moving_left=False
     
def check_events(ai_settings,screen,ship,bullets):
    """respond to keypress and mouse events."""
    for event in pygame.event.get():
         if event.type==pygame.QUIT:
            sys.exit()
         elif event.type==pygame.KEYDOWN:
              check_keydown_events(event,ai_settings,screen,ship,bullets)

         elif event.type==pygame.KEYUP:
              check_keyup_events(event,ship)

def update_screen(ai_settings,screen,ship,aliens,bullets):
         #redraw the screen during each pass through the loop
        screen.fill(ai_settings.bg_color)
        #redraw all bullets behind ships and aliens.
        for bullet in bullets.sprites():
             bullet.draw_bullet()

        ship.blitme()
        
        aliens.draw(screen)
        

        #make the most recently drawn screen visible
        pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,bullets):
    #update bullet position
     bullets.update()
     #get rid of bullets that have disappeared
     for bullet in bullets.copy():
          if bullet.rect.bottom <=0:
             bullets.remove(bullet)
          print(len(bullets))
     #check if any bullet have hit the aliens
     check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets)

def check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets):
     collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
     if len(aliens)==0:
          #destroy existing bullets and create new fleet
          bullets.empty()
          create_fleet(ai_settings,screen,ship,aliens)
#!/usr/bin/env python

#
#   Breakout V 0.1 June 2009
#
#   Copyright (C) 2009 John Cheetham    
#
#   web   : http://www.johncheetham.com/projects/breakout
#   email : developer@johncheetham.com
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#    
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, pygame, random

class Breakout():
   
    def main(self):

        xspeed_init = 6 # originally 6
        yspeed_init = 6 # originally 6
        max_lives = 5 # was 5 originally
        bat_speed_init = 5
        bat_speed = bat_speed_init # was 30 originally pixel movement left / right
        #
        wall_speed_init = 4 # was 4
        bottom_edge_init = 50 # just to initialize this parameter
        brick_hesitation_factor_init = 30 # was 30
        #
        score = 0 
        bgcolour = 0x2F, 0x4F, 0x4F  # darkslategrey        
        size = width, height = 640, 480

        pygame.init()            
        screen = pygame.display.set_mode(size)
        #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        bat = pygame.image.load("bat.png").convert()
        batrect = bat.get_rect()
        #
        missile = pygame.image.load("bullet.png").convert()
        missile_rect = missile.get_rect()
        missile_speed_init = wall_speed_init
        missile_speed = missile_speed_init
        can_shoot = True

        alien_missile = pygame.image.load("bullet.png").convert()
        alien_missile_rect = missile.get_rect()
        alien_missile_speed_init = missile_speed_init
        alien_missile_speed = alien_missile_speed_init

        Invader_shoots = True


        pong = pygame.mixer.Sound('Blip_1-Surround-147.wav')
        pong.set_volume(10)        
        
        wall = Wall()
        wall.build_wall(width)

        # Initialise ready for game loop
        batrect = batrect.move((width / 2) - (batrect.right / 2), height - 20)
        brick_hesitation_factor = brick_hesitation_factor_init
        wall_speed = wall_speed_init
        bottom_edge = bottom_edge_init
        direction = 1
        #
  
        lives = max_lives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1,30)  # frequency with which a pressed key is repeated (first is after 1 ms, then every 30 ms after)     
        pygame.mouse.set_visible(0)       # turn off mouse pointer

        control_idx = brick_hesitation_factor
        brick_move = False
        while 1:

            # 60 frames per second -- maximum number of while loops executed per second
            clock.tick(60)
            control_idx += 1
            if control_idx % brick_hesitation_factor == 0:
                control_idx = 1
                brick_move = True
            else:
                brick_move = False
            
            # process key presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
        	            sys.exit()
                    if event.key == pygame.K_LEFT:                        
                        #batrect = batrect.move(-bat_speed, 0)     
                        bat_speed = -bat_speed_init    
                    if event.key == pygame.K_RIGHT:                    
                        #batrect = batrect.move(bat_speed, 0)
                        bat_speed = bat_speed_init
                    if event.key == pygame.K_SPACE:
                        if can_shoot == True:
                            can_shoot = False
                            missile_rect.center = batrect.center             
            
            # Move missile, move bat
            batrect = batrect.move(bat_speed, 0)
            if (batrect.left < 0):                           
                batrect.left = 0  
            if (batrect.right > width):                            
                batrect.right = width
            missile_rect = missile_rect.move(0 , -missile_speed_init)
            if missile_rect.centery < 0:
                can_shoot = True
            #

            # move bricks
            if brick_move:
                current_wall_speed = wall_speed
                wall_parameters = wall.move_wall(wall.brickrect, wall_speed, width)
                wall_speed = wall_parameters[0]
                bottom_edge = wall_parameters[1]
                if wall_speed * current_wall_speed < 0:
                    #brick_hesitation_factor -= 1 # Can be used to speed up wall each time it lowers
                    current_wall_speed = wall_speed

            # invaders (bricks) shoot
            if Invader_shoots == True:
                invader_count = len(wall.brickrect)
                shooter = random.randrange(0, invader_count)
                alien_missile_rect.center = wall.brickrect[shooter].center
                Invader_shoots = False
            alien_missile_rect = alien_missile_rect.move(0, alien_missile_speed)
            if alien_missile_rect.top > height:
                Invader_shoots = True

            


            if bottom_edge > batrect.top: #or ballrect.top > height:
                lives -= 1

            if alien_missile_rect.colliderect(batrect):
                lives -= 1
                alien_missile_rect.center = -50, -50
                Invader_shoots = True

            # if wall completely gone or passes paddle then rebuild wall
            if wall.brickrect == []:
                brick_hesitation_factor = brick_hesitation_factor_init            
                wall.build_wall(width)                
                screen.blit(bat, batrect)   #Redraws bat in new position
                pygame.display.flip()  #Part of the redraw process--updates the entire screen; .update() updates a portion of the screen only


            if lives == 0:                    
                msg = pygame.font.Font(None,70).render("Game Over", True, (0,255,255), bgcolour)
                msgrect = msg.get_rect()
                msgrect = msgrect.move(width / 2 - (msgrect.center[0]), height / 3)
                screen.blit(msg, msgrect)
                pygame.display.flip()
                # process key presses
                #     - ESC to quit
                #     - any other key to restart game
                while 1:
                    restart = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                sys.exit()
                            if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):                                    
                                restart = True      
                    if restart:                   
                        screen.fill(bgcolour)
                        wall.build_wall(width)
                        lives = max_lives
                        score = 0
                        break
            

            
           
            # check if missile has hit wall
            index = missile_rect.collidelist(wall.brickrect)  #check to see if missile has collided with a brick in the wall     
            if index != -1:
                missile_rect.center = -10, -10
                can_shoot = True 
           
                wall.brickrect[index:index + 1] = [] #delete brick that has been hit by ball
                score += 10 #increase score


            screen.fill(bgcolour) #This line may repaint the entire game window so all of the items can be redrawn effectively giving the illusion of movement. Without this line, the wall doesn't visually disappear, but the deleted blocks don't deflect the ball.

            #These next 4 lines update the image for the score
            scoretext = pygame.font.Font(None,30).render("Score: " + str(score), True, (0,255,255), bgcolour) #40=font size, write new score (str(score))
            scoretextrect = scoretext.get_rect() #Gets the bounding rectangle of for the score
            scoretextrect = scoretextrect.move(width - scoretextrect.right, 0) #Right justifies the score box bounding rectangle in the game window
            screen.blit(scoretext, scoretextrect) #draws score on screen

            #
            lifestring = str(lives - 1) + " Lives Remaining"
            lifetext = pygame.font.Font(None,30).render((lifestring), True, (0,255,255), bgcolour) #40=font size, write new score (str(score))
            lifetextrect = lifetext.get_rect() #Gets the bounding rectangle of for the number of lives
            lifetextrect = lifetextrect.move(lifetextrect.left, 0) #Left justifies the lives box bounding rectangle in the game window
            screen.blit(lifetext, lifetextrect) #draws lives on screen
            #

            for i in range(0, len(wall.brickrect)): #This draws all of the active bricks in the wall
                screen.blit(wall.brick, wall.brickrect[i])    

            # if wall completely gone then rebuild it
            if wall.brickrect == []:
                brick_hesitation_factor = 30            
                wall.build_wall(width)                
                batrect.center = width / 2, height - 20
         
            #screen.blit(ball, ballrect) #Redraws ball in new position
            screen.blit(bat, batrect)   #Redraws bat in new position
            screen.blit(missile, missile_rect)
            screen.blit(alien_missile, alien_missile_rect)
            pygame.display.flip()  #Part of the redraw process--updates the entire screen; .update() updates a portion of the screen only

class Wall():

    def __init__(self):
        self.brick = pygame.image.load("brick.png").convert()
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left       
        self.brickheight = brickrect.bottom - brickrect.top             

    def build_wall(self, width):        
        xpos = 50 # was 0
        ypos = 60
        adj = 0
        self.brickrect = []      # This is the array of bricks in the wall
        for i in range (0, 52):  # number of bricks in wall           
            if xpos > width - 50: # was width:     # Each time a new brick would be drawn beyond the window, a new row is started and the Xpos for that row alternates between 0 and -1/2 of it's length
                if adj == 50: # was 0
                    adj = 50 # was self.bricklength / 2
                else:
                    adj = 50 # was 0
                xpos = adj #(was -adj)
                ypos += 1.25 * (self.brickheight) # This controls space between rows of bricks. When the coefficient is 1.0, there's no space between rows 

            #print(xpos, ypos)    
            self.brickrect.append(self.brick.get_rect()) #I think this adds another brick to the wall   
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos) #I think this is where the newly added brick has its position properties defined
            xpos = xpos + 1.25 * (self.bricklength) #This controls the spacing between the bricks: +self.bricklenght means bricks are snug; using a larger number puts space between the bricks
    
    def move_wall(self, bricks, wall_speed, width):
        # New method that I added for moving the bricks and finding the leftmost, rightmost, bottom most edges of the existing wall
        brickCount = len(bricks) # number of moving bricks
        brick_length = bricks[0].right - bricks[0].left
        self.left = bricks[0].left
        self.right = bricks[0].right
        self.bottom = bricks[0].bottom

        for i in range(0, brickCount):  #This draws all of the active bricks in the wall
            bricks[i] = bricks[i].move(wall_speed, 0)

        for i in range(0, brickCount): #find leftmost, rightmost, bottom most edges of the existing wall
            left_edge_temp = bricks[i].left
            right_edge_temp = bricks[i].right
            bottom_edge_temp = bricks[i].bottom
            if left_edge_temp < self.left:
                self.left = left_edge_temp
            if right_edge_temp > self.right:
                self.right = right_edge_temp
            if bottom_edge_temp > self.bottom:
                self.bottom = bottom_edge_temp

        # Is it time for the bricks to change direction and lower?
        if (self.left) < (0) or (self.right) > (width):
            wall_speed = -1.0 * (wall_speed)
            for j in range(0,brickCount):
                bricks[j] = bricks[j].move(wall_speed, 10)
        self.speed = wall_speed
        wall_parameters = [self.speed, self.bottom, self.left, self.right]
        return wall_parameters
  

if __name__ == '__main__':
    br = Breakout()
    br.main()


# Pygame creates a new rect with the size of the image and the x, y coordinates (0, 0). 
# To give the rect other coords during the instantiation you can pass an argument to get_rect.
# To move the rect later, you can change any of these attributes of the rect:
# This means that x,y is a corner of the rectangle and it extends from x,y to x+length and y+height
#
# x,y
# top, left, bottom, right
# topleft, bottomleft, topright, bottomright
# midtop, midleft, midbottom, midright
# center, centerx, centery
# size, width, height
# w,h
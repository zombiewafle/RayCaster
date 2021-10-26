from typing import ForwardRef
import pygame
from pygame.event import pump

from menu import *

from math import cos, sin, pi

from pygame import display

RAY_AMOUNT = 100

wallcolors = {
    '1': pygame.Color('red'),
    '2': pygame.Color('green'),
    '3': pygame.Color('blue'),
    '4': pygame.Color('yellow'),
    '5': pygame.Color('purple')
    }

wallTextures = {
    '1': pygame.image.load('textures/PIPE4.png'),
    '2': pygame.image.load('textures/CEMENT6.png'),
    '3': pygame.image.load('textures/SW2CMT.png'),
    '4': pygame.image.load('textures/BIGDOOR2.png'),
    '5': pygame.image.load('textures/CEMENT2.png'),
    '6': pygame.image.load('textures/CEMPOIS.png')
    }

class GameState():
    def __init__(self):
        self.state = 'intro'
    
    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type ==  pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'


        screen.blit(menuIMG, (0,0))
        drawText('Wolfenstein', font, pygame.Color("white"), screen, 400,100)
        drawText('New Order and the Origin of the Doom', font, pygame.Color("white"), screen, 200,150)
        screen.fill(pygame.Color("black"), (0,0,40,30) )
        screen.blit(updateFPS(), (0,0))
        clock.tick(60)
    
    
        pygame.display.flip()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        
        if self.state == 'main_game':
            self.main_game()

    def main_game(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False

            elif ev.type == pygame.KEYDOWN:
                newX = rCaster.player['x']
                newY = rCaster.player['y']
                forward = rCaster.player['angle'] * pi / 180
                right = (rCaster.player['angle'] + 90) * pi / 180

                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                    pygame.quit()
                    quit()
                elif ev.key == pygame.K_w:
                    newX += cos(forward) * rCaster.stepSize
                    newY += sin(forward) * rCaster.stepSize
                elif ev.key == pygame.K_s:
                    newX -= cos(forward) * rCaster.stepSize
                    newY -= sin(forward) * rCaster.stepSize
                elif ev.key == pygame.K_a:
                    newX -= cos(right) * rCaster.stepSize
                    newY -= sin(right) * rCaster.stepSize
                elif ev.key == pygame.K_d:
                    newX += cos(right) * rCaster.stepSize
                    newY += sin(right) * rCaster.stepSize
                elif ev.key == pygame.K_q:
                    rCaster.player['angle'] -= rCaster.turnSize
                elif ev.key == pygame.K_e:
                    rCaster.player['angle'] += rCaster.turnSize
                elif ev.key == pygame.K_p:
                    pauseGame()


                i = int(newX/rCaster.blocksize)
                j = int(newY/rCaster.blocksize)

                if rCaster.map[j][i] == ' ':
                    rCaster.player['x'] = newX
                    rCaster.player['y'] = newY


        screen.fill(pygame.Color("gray"))
    
        # Techo
        screen.fill(pygame.Color("black"), (int(width / 2), 0,  int(width / 2), int(height / 2)))
    
        # Piso
        screen.fill(pygame.Color("dimgray"), (int(width / 2), int(height / 2),  int(width / 2), int(height / 2)))
    
    
        rCaster.render()
    
        #FPS
        screen.fill(pygame.Color("black"), (0,0,40,30) )
        screen.blit(updateFPS(), (0,0))
        clock.tick(60)
    
    
        pygame.display.flip()
                
        #screen.fill(pygame.Color("black"))
        #drawText('The Origin of the Doom', font, pygame.Color("white"), screen, 300,50)
        #button1.draw()
        #button2.draw()
        
        #pygame.display.update()
        #clock.tick(60)
        #pygame.display.flip()

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.blocksize = 50
        self.wallheight = 50

        self.maxdistance = 300

        self.font_name = '8-BIT WONDER.TTF'

        self.stepSize = 5
        self.turnSize = 5

        self.player = {
           'x' : 100,
           'y' : 175,
           'fov': 60,
           'angle': 180 }

    def load_map(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append( list(line.rstrip()) )

    def drawBlock(self, x, y, id):
        tex = wallTextures[id]
        tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize) )
        rect = tex.get_rect()
        rect = rect.move((x,y))
        self.screen.blit(tex, rect)

    def drawPlayerIcon(self, color):
        if self.player['x'] < self.width / 2:
            rect = (self.player['x'] - 2, self.player['y'] - 2, 5,5)
            self.screen.fill(color, rect )

    def castRay(self, angle):
        rads = angle * pi / 180
        dist = 0
        stepSize = 1
        stepX = stepSize * cos(rads)
        stepY = stepSize * sin(rads)

        playerPos = (self.player['x'],self.player['y'] )

        x = playerPos[0]
        y = playerPos[1]

        while True:
            dist += stepSize      

            x += stepX
            y += stepY

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if j < len(self.map):
                if i < len(self.map[j]):
                    if self.map[j][i] != ' ':

                        hitX = x - i*self.blocksize
                        hitY = y - j*self.blocksize

                        hit = 0

                        if 1 < hitX < self.blocksize-1:
                            if hitY < 1:
                                hit = self.blocksize - hitX
                            elif hitY >= self.blocksize-1:
                                hit = hitX
                        elif 1 < hitY < self.blocksize-1:
                            if hitX < 1:
                                hit = hitY
                            elif hitX >= self.blocksize-1:
                                hit = self.blocksize - hitY

                        tx = hit / self.blocksize

                        pygame.draw.line(self.screen,pygame.Color('white'), playerPos, (x,y))
                        return dist, self.map[j][i], tx

    def render(self):
        halfWidth = int(self.width / 2)
        halfHeight = int(self.height / 2)

        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):

                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if j < len(self.map):
                    if i < len(self.map[j]):
                        if self.map[j][i] != ' ':
                            self.drawBlock(x, y, self.map[j][i])

        self.drawPlayerIcon(pygame.Color('black'))

        for column in range(RAY_AMOUNT):
            angle = self.player['angle'] - (self.player['fov'] / 2) + (self.player['fov'] * column / RAY_AMOUNT)
            dist, id, tx = self.castRay(angle)

            rayWidth = int(( 1 / RAY_AMOUNT) * halfWidth)

            startX = halfWidth + int(( (column / RAY_AMOUNT) * halfWidth))

            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle)) * wallHeight
            h = self.height / (dist * cos( (angle - self.player["angle"]) * pi / 180)) * self.wallheight
            startY = int(halfHeight - h/2)
            endY = int(halfHeight + h/2)

            color_k = (1 - min(1, dist / self.maxdistance)) * 255

            tex = wallTextures[id]
            tex = pygame.transform.scale(tex, (tex.get_width() * rayWidth, int(h)))
            #tex.fill((color_k,color_k,color_k), special_flags=pygame.BLEND_MULT)
            tx = int(tx * tex.get_width())
            self.screen.blit(tex, (startX, startY), (tx,0,rayWidth,tex.get_height()))

        # Columna divisora
        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), pygame.Color('black'))
            self.screen.set_at( (halfWidth+1, i), pygame.Color('black'))
            self.screen.set_at( (halfWidth-1, i), pygame.Color('black'))

class MainButton():
    def __init__(self,text,width,height,pos,elevation):
		#Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        
        # top rectangle
        self.top_rect = pygame.Rect(pos,(width,height)) 
        self.top_color = '#475F77'

		# bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
		#text
        self.text_surf = font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self):
		# elevation logic 
        # 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
        
        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()
        
    def check_click(self):
        isRunning = True
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    print("Clicked")
                    self.pressed = False

        
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'

width = 1000
height = 500

isRunning = True
pressed = True

game_state = GameState()

click = False

img = pygame.image.load("textures/wallpaper.jpg")
menuIMG = pygame.image.load("textures/logo.jpg")

pygame.display.set_caption('The Origin of the Doom')

pygame.init()
screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL )
screen.set_alpha(None)

rCaster = Raycaster(screen)
rCaster.load_map("map3.txt")

clock = pygame.time.Clock()
#font = pygame.font.SysFont("Arial", 25)
font = pygame.font.Font("8-BIT WONDER.TTF", 20)

button1 = Button('Start Game',210,40,(400,200),8)
button2 = Button('Exit',210,40,(400,300),8)
 

def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

def drawText(msg,font, color, surface, x, y):
    msg = font.render(msg, True, color)
    textRect = msg.get_rect()
    #textRect.topleft = (x, y)
    textRect.topleft = (x, y)
    surface.blit(msg, textRect)

def pauseGame ():
    paused = True
    #font = pygame.font.Font(font,20)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        #screen.fill(pygame.Color("black"))
        screen.blit(img, (0,0))
        #message_to_Screen("Paused, press C to continue or M to quit", pygame.Color("black"))
        drawText('Paused press C to continue or Escape to quit', font, pygame.Color("white"), screen, 100,250)

        #message_to_Screen("Press C to continue or Q to quit", pygame.Color("black"))
        pygame.display.update()
        clock.tick(5)

def mainMenu():
    if stageOption == 1:
	    button1.draw()
	    button2.draw()

	    pygame.display.update()
	    clock.tick(60)

    elif stageOption == 2:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False

            elif ev.type == pygame.KEYDOWN:
                newX = rCaster.player['x']
                newY = rCaster.player['y']
                forward = rCaster.player['angle'] * pi / 180
                right = (rCaster.player['angle'] + 90) * pi / 180

                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                elif ev.key == pygame.K_w:
                    newX += cos(forward) * rCaster.stepSize
                    newY += sin(forward) * rCaster.stepSize
                elif ev.key == pygame.K_s:
                    newX -= cos(forward) * rCaster.stepSize
                    newY -= sin(forward) * rCaster.stepSize
                elif ev.key == pygame.K_a:
                    newX -= cos(right) * rCaster.stepSize
                    newY -= sin(right) * rCaster.stepSize
                elif ev.key == pygame.K_d:
                    newX += cos(right) * rCaster.stepSize
                    newY += sin(right) * rCaster.stepSize
                elif ev.key == pygame.K_q:
                    rCaster.player['angle'] -= rCaster.turnSize
                elif ev.key == pygame.K_e:
                    rCaster.player['angle'] += rCaster.turnSize
                elif ev.key == pygame.K_p:
                    pauseGame()


                i = int(newX/rCaster.blocksize)
                j = int(newY/rCaster.blocksize)

                if rCaster.map[j][i] == ' ':
                    rCaster.player['x'] = newX
                    rCaster.player['y'] = newY


    elif stageOption == 3:
        pygame.quit()
        quit()

def updateFPS():
    #font = pygame.font.Font(self.font_name,5)
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

while isRunning:
    game_state.state_manager()

pygame.quit()

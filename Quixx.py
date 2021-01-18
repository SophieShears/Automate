# Program that allows the user to play the game Quixx over a Zoom call

import pygame
import random
import time
from copy import deepcopy

pygame.init()

win = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Quixx')
clock = pygame.time.Clock()

class Main:
    def __init__(self):
        self.players = []

        self.black = (0, 0, 0)
        self.blue = (0, 128, 255)
        self.green = (0, 128, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        self.yellow = (230, 230, 0)

        self.roll = {'w1':'', 'w2':'', 'r':'', 'g':'', 'b':'', 'y':''}
        self.prevRoll = {'w1':'', 'w2':'', 'r':'', 'g':'', 'b':'', 'y':''}

        self.players = {}
        self.displayedPosition = 0
        self.displayedPlayer = ''

        self.numPlayers = int(input("Enter number of players: "))
        for i in range(0, self.numPlayers):
            player = input('Player name: ')
            self.players[i+1] = player

    def textObjects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def drawText(self, msg, text_color, x, y, w, h, fontsize=100):
        smallText = pygame.font.SysFont("freesansbold.ttf", fontsize)
        textSurf, textRect = self.textObjects(msg, smallText, text_color)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        win.blit(textSurf, textRect)

    def button(self, msg, x, y, w, h, text_color, border_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(win, border_color, (x, y, w, h), 3)
            if click[0] == 1 and action != None:
                action()

        smallText = pygame.font.SysFont("freesansbold.ttf", 40)
        textSurf, textRect = self.textObjects(msg, smallText, text_color)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        win.blit(textSurf, textRect)

    def rollEffect(self):
        if self.roll['w1'] != '':
            self.prevRoll = deepcopy(self.roll)
        for die in self.roll:
            self.roll[die] = str(random.randint(1, 6))
        if self.displayedPosition == self.numPlayers:
            self.displayedPosition = 1
            self.displayedPlayer = self.players[self.displayedPosition]
        elif self.displayedPosition != self.numPlayers:
            self.displayedPosition += 1
            self.displayedPlayer = self.players[self.displayedPosition]
        time.sleep(0.5)

    def drawWin(self):
        win.fill(self.white)

        #Die Squares
        pygame.draw.rect(win, self.black, (400, 100, 150, 150), 2)
        pygame.draw.rect(win, self.black, (600, 100, 150, 150), 2)
        pygame.draw.rect(win, self.red, (400, 300, 150, 150))
        pygame.draw.rect(win, self.green, (600, 300, 150, 150))
        pygame.draw.rect(win, self.blue, (400, 500, 150, 150))
        pygame.draw.rect(win, self.yellow, (600, 500, 150, 150))

        #Die values
        self.drawText(self.roll['w1'], self.black, 400, 100, 150, 150)
        self.drawText(self.roll['w2'], self.black, 600, 100, 150, 150)
        self.drawText(self.roll['r'], self.black, 400, 300, 150, 150)
        self.drawText(self.roll['g'], self.black, 600, 300, 150, 150)
        self.drawText(self.roll['b'], self.black, 400, 500, 150, 150)
        self.drawText(self.roll['y'], self.black, 600, 500, 150, 150)

        #left column
        self.drawText(self.displayedPlayer, self.black, 100, 100, 150, 150, fontsize=115)

        y = 200
        for i in self.players:
            self.drawText(self.players[i], self.black, 100, y, 150, 150, fontsize=50)
            y += 50

        #Right column
        self.drawText('Previous Roll', self.black, 900, 100, 150, 150, fontsize=50)

        self.drawText('White : ' + self.prevRoll['w1'], self.black, 900, 150, 150, 150, fontsize=30)
        self.drawText('White : ' + self.prevRoll['w2'], self.black, 900, 175, 150, 150, fontsize=30)
        self.drawText('Red : ' + self.prevRoll['r'], self.red, 900, 200, 150, 150, fontsize=30)
        self.drawText('Green : ' + self.prevRoll['g'], self.green, 900, 225, 150, 150, fontsize=30)
        self.drawText('Blue : ' + self.prevRoll['b'], self.blue, 900, 250, 150, 150, fontsize=30)
        self.drawText('Yellow : ' + self.prevRoll['y'], self.yellow, 900, 275, 150, 150, fontsize=30)

        #button
        self.button('Next Turn', 400, 700, 200, 75, self.black, self.black, self.rollEffect)

    def gameLoop(self):
        while True:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.drawWin()
            pygame.display.update()
            clock.tick(30)


run = Main()
run.gameLoop()
pygame.quit()
quit()

import pygame
from pygame.display import *

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Checkers")

class Button:
	def __init__(self,text,x,y,width,height,color1,color2):
		mPos = pygame.mouse.get_pos()
		mPressed = pygame.mouse.get_pressed()
		self.dct = {'2':'X','1':'x','0':'.','-1':'o','-2':'O','Quit':'Quit', 'Stay':'Stay'}
		self.text = text
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color1 = color1
		self.color2 = color2
		self.status = False
		self.chosen = False
		if self.chosen or (self.x < mPos[0] < self.x+self.width and self.y < mPos[1] < self.y+self.width):
			pygame.draw.rect(screen, self.color2, (self.x,self.y,self.width,self.height))
			if mPressed[0] == 1:
				self.status = True
		else:
			pygame.draw.rect(screen, self.color1, (self.x,self.y,self.width,self.height))
		writing = pygame.font.Font("freesansbold.ttf",16)
		self.startSurface, self.startRect = TextBox(self.dct[self.text], writing)
		self.startRect = ((self.x+(self.width/4)),(self.y+(self.height/2)))
		screen.blit(self.startSurface, self.startRect)
	def update(self):
		mPos = pygame.mouse.get_pos()
		mPressed = pygame.mouse.get_pressed()
		if self.chosen or (self.x < mPos[0] < self.x+self.width and self.y < mPos[1] < self.y+self.width):
			pygame.draw.rect(screen, self.color2, (self.x,self.y,self.width,self.height))
			if mPressed[0] == 1:
				self.status = True
		else:
			pygame.draw.rect(screen, self.color1, (self.x,self.y,self.width,self.height))
		writing = pygame.font.Font("freesansbold.ttf",16)
		self.startSurface, self.startRect = TextBox(self.dct[self.text], writing)
		self.startRect = ((self.x+(self.width/4)),(self.y+(self.height/2)))
		screen.blit(self.startSurface, self.startRect)

def getpygame():
	return pygame

def getScreen():
	return screen

def TextBox(string, font):
	surface = font.render(string, True, (0,0,0))
	return surface, surface.get_rect()

def createButton(text,x,y,width,height,color1,color2):
	return Button(text,x,y,width,height,color1,color2)
	'''mPos = pygame.mouse.get_pos()
	mPressed = pygame.mouse.get_pressed()
	if x < mPos[0] < x+width and y < mPos[1] < y+width:
		pygame.draw.rect(screen, color2, (x,y,width,height))
		if mPressed[0] == 1:
			return True
	else:
		pygame.draw.rect(screen, color1, (x,y,width,height))
	writing = pygame.font.Font("freesansbold.ttf",16)
	startSurface, startRect = TextBox(text, writing)
	startRect = ((x+(width/4)),(y+(height/2)))
	screen.blit(startSurface, startRect)'''

def createFrame(x,y,width,height,color):
	pygame.draw.rect(screen, color, (x,y,width,height))
	writing = pygame.font.Font("freesansbold.ttf",16)
	startSurface, startRect = TextBox("", writing)
	startRect = ((x+(width/4)),(y+(height/2)))
	screen.blit(startSurface, startRect)
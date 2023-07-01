# vim: set noexpandtab:

import sys
import random
import pygame
import math
blackHole0 = pygame.image.load("blackhole0.png")
blackHole1 = pygame.image.load("blackhole1.png")
blackHole2 = pygame.image.load("blackhole2.png")
blackHole3 = pygame.image.load("blackhole3.png")

earth = pygame.image.load("Earth.png")

player_1_image1 = pygame.image.load("HORSE_1.png")
player_1_image2 = pygame.image.load("HORSE_2.png")
player_1_images = {"right":[player_1_image1, player_1_image2],
									"up":[pygame.transform.rotate(player_1_image1, 90),
													pygame.transform.rotate(player_1_image2, 90)],
									"left":[pygame.transform.rotate(player_1_image1, 180),
													pygame.transform.rotate(player_1_image2, 180)],
									"down":[pygame.transform.rotate(player_1_image1, 270),
													pygame.transform.rotate(player_1_image2, 270)]}

#player 2
player_2_image1 = pygame.image.load("HORSE_B_1.png")
player_2_image2 = pygame.image.load("HORSE_B_2.png")
player_2_images = {"right":[player_2_image1, player_2_image2],
									"up":[pygame.transform.rotate(player_2_image1, 90),
													pygame.transform.rotate(player_2_image2, 90)],
									"left":[pygame.transform.rotate(player_2_image1, 180),
													pygame.transform.rotate(player_2_image2, 180)],
									"down":[pygame.transform.rotate(player_2_image1, 270),
													pygame.transform.rotate(player_2_image2, 270)]}

#FUNCTION FOR SHUTTING DOWN######################
def quitGame():
	print("Shutting down succesfully")
	pygame.quit()
	sys.exit()


class Earth(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Earth.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = screenWidth/2
		self.rect.centery = screenHeight/2
		self.radius = 24
		self.xDelta = 0
		self.yDelta = 0

	def update(self):
		self.rect.x += self.xDelta
		self.rect.y += self.yDelta

		if self.rect.centerx < 0:
			self.rect.centerx = 0
			self.xDelta *= -1
		elif self.rect.centerx > screenWidth:
			self.rect.centerx = screenWidth
			self.xDelta *= -1

		if self.rect.centery < 0:
			self.rect.centery = 0
			self.yDelta *= -1
		elif self.rect.centery > screenHeight:
			self.rect.centery = screenHeight
			self.yDelta *= -1


class Wormhole(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("blackHole3.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = random.randint(0,screenWidth)
		self.rect.centery = random.randint(0,screenHeight)
		self.radius = 16
		self.xDelta = 0
		self.yDelta = 0

	def update(self):
		self.rect.x += self.xDelta
		self.rect.y += self.yDelta

		if self.rect.centerx < 0:
			self.rect.centerx = 0
			self.xDelta *= -1
		elif self.rect.centerx > screenWidth:
			self.rect.centerx = screenWidth
			self.xDelta *= -1

		if self.rect.centery < 0:
			self.rect.centery = 0
			self.yDelta *= -1
		elif self.rect.centery > screenHeight:
			self.rect.centery = screenHeight
			self.yDelta *= -1


class Asteroid(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Asteroid.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = random.randint(0,screenWidth)
		self.rect.centery = random.randint(0,screenHeight)
		self.xDelta = 0
		self.yDelta = 0
		self.radius=70
		self.mass=10

	def update(self):
		g = 30
		for earth in earths:
			xDist = self.rect.centerx - earth.rect.centerx
			yDist = self.rect.centery - earth.rect.centery
			dist = math.sqrt(xDist**2+yDist**2)

			angle = math.atan2(yDist, xDist)
			self.xDelta -= math.cos(angle) * g/dist
			self.yDelta -= math.sin(angle) * g/dist

	
		self.rect.x += self.xDelta
		self.rect.y += self.yDelta

"""
		if self.rect.centerx < 0:
			self.rect.centerx = 0
			self.xDelta *= -0.5
		elif self.rect.centerx > screenWidth:
			self.rect.centerx = screenWidth
			self.xDelta *= -0.5

		if self.rect.centery < 0:
			self.rect.centery = 0
			self.yDelta *= -0.5
		elif self.rect.centery > screenHeight:
			self.rect.centery = screenHeight
			self.yDelta *= -0.5
"""

class Player(pygame.sprite.Sprite):
	def __init__(self,playerNumber):
		pygame.sprite.Sprite.__init__(self)
		self.playerNumber = playerNumber
		if self.playerNumber == 1:
			self.images = player_1_images["left"]
			self.image = self.images[0]
			self.rect = self.image.get_rect()
			self.rect.centerx = screenWidth/2 + 300
			self.yDelta = 6
		elif self.playerNumber == 2:
			self.images = player_2_images["right"]
			self.image = self.images[0]
			self.rect = self.image.get_rect()
			self.rect.centerx = screenWidth/2 - 300
			self.yDelta = -6

		self.rect.centery = screenHeight/2
		self.xDelta = 0
		self.accForce = 1.5
		self.thrust = "None"
		self.radius = 30
		self.mass = 3
	
	def accelerateRight(self):
		self.xDelta += self.accForce
		if self.playerNumber == 1:
			self.images = player_1_images["right"]
		elif self.playerNumber == 2:
			self.images = player_2_images["right"]
			
		self.image = self.images[1]
	def accelerateLeft(self):
		self.xDelta -= self.accForce
		if self.playerNumber == 1:
			self.images = player_1_images["left"]
		elif self.playerNumber == 2:
			self.images = player_2_images["left"]
			
		self.image = self.images[1]
	def accelerateUp(self):
		self.yDelta -= self.accForce
		if self.playerNumber == 1:
			self.images = player_1_images["up"]
		elif self.playerNumber == 2:
			self.images = player_2_images["up"]
			
		self.image = self.images[1]

	def accelerateDown(self):
		self.yDelta += self.accForce
		if self.playerNumber == 1:
			self.images = player_1_images["down"]
		elif self.playerNumber == 2:
			self.images = player_2_images["down"]
		self.image = self.images[1]

	def update(self):
		g = 40
		for earth in earths:
			xDist = self.rect.centerx - earth.rect.centerx
			yDist = self.rect.centery - earth.rect.centery
			dist = math.sqrt(xDist**2+yDist**2)

			angle = math.atan2(yDist, xDist)
			self.xDelta -= math.cos(angle) * g/dist
			self.yDelta -= math.sin(angle) * g/dist

	
		self.rect.x += self.xDelta
		self.rect.y += self.yDelta

		if self.rect.centerx < 0:
			self.rect.centerx = 0
			self.xDelta *= -0.5
		elif self.rect.centerx > screenWidth:
			self.rect.centerx = screenWidth
			self.xDelta *= -0.5

		if self.rect.centery < 0:
			self.rect.centery = 0
			self.yDelta *= -0.5
		elif self.rect.centery > screenHeight:
			self.rect.centery = screenHeight
			self.yDelta *= -0.5



#startup stuff###################################
pygame.init()
screenWidth = 2560
screenHeight = 1440
screen = pygame.display.set_mode((screenWidth,screenHeight),flags=pygame.NOFRAME)
clock = pygame.time.Clock()
frameCount = 0
players = pygame.sprite.Group()

earths = pygame.sprite.Group()
earth = Earth()
earths.add(earth)

wormholes = pygame.sprite.Group()

player1 = Player(1)
player2 = Player(2)
players.add(player1,player2)

asteroids = pygame.sprite.Group()

background = pygame.Surface((screenWidth,screenHeight))
backgroundRect = background.get_rect()
pygame.draw.rect(background, (10,10,10), backgroundRect) 
for i in range(300):
	x = random.randint(0,screenWidth)
	y = random.randint(0,screenHeight)
	s = random.randint(1,4)
	starRect = pygame.rect.Rect(x,y,s,s)
	pygame.draw.rect(background, (255,255,255), starRect)



#THE GAME LOOP####################################
while True:

	#input handling
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			#Player 1 movement
			if event.key == pygame.K_DOWN:
				player1.accelerateDown()
			elif event.key == pygame.K_UP:
				player1.accelerateUp()
			elif event.key == pygame.K_RIGHT:
				player1.accelerateRight()
			elif event.key == pygame.K_LEFT:
				player1.accelerateLeft()

			#Player 2 movement
			elif event.key == pygame.K_s:
				player2.accelerateDown()
			elif event.key == pygame.K_w:
				player2.accelerateUp()
			elif event.key == pygame.K_d:
				player2.accelerateRight()
			elif event.key == pygame.K_a:
				player2.accelerateLeft()

			#Quit with escape key
			elif event.key == pygame.K_ESCAPE:
				quitGame()
		elif event.type == pygame.QUIT:
			quitGame()

	#update stuff
	earths.update()
	players.update()
	asteroids.update()

	#Collision management
	if pygame.sprite.collide_circle(player1,player2):
		xDP1=player2.xDelta
		xDP2=player1.xDelta
		yDP1=player2.yDelta
		yDP2=player1.yDelta

		player1.xDelta=xDP1
		player2.xDelta=xDP2
		player1.yDelta=yDP1
		player2.yDelta=yDP2
		
	for asteroid in asteroids:
		if pygame.sprite.collide_circle(earth,asteroid):
			quitGame()	

		for player in players:
			if pygame.sprite.collide_circle(player,asteroid):
				xDA=player.xDelta
				xDP=asteroid.xDelta
				yDA=player.yDelta
				yDP=asteroid.yDelta

				asteroid.xDelta=xDA
				player.xDelta=xDP
				asteroid.yDelta=yDA
				player.yDelta=yDP

	for wormhole in wormholes:
		for asteroid in asteroids:
			if pygame.sprite.collide_circle(asteroid,wormhole):
				asteroid.kill()



		
	#draw stuff
	screen.blit(background,(0,0))
	
	if (frameCount % 600 == 0):
		asteroid = Asteroid()
		asteroids.add(asteroid)

		wormholes.empty()
		wormhole = Wormhole()
		wormholes.add(wormhole)

	asteroids.draw(screen)
	#screen.blit(earth,(screenWidth/2-36,screenHeight/2-36))
	earths.draw(screen)
	wormholes.draw(screen)
	players.draw(screen)


	player1.image = player1.images[0]
	player2.image = player2.images[0]
	pygame.display.flip()

	#update frame counter
	frameCount += 1

#CLOCK MUST BE LAST##############################
	clock.tick(60)


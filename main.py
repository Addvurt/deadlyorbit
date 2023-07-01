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

class ForeignObject(pygame.sprite.Sprite):
	def __init__(self,number):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Asteroid.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.centerx = 100
		self.rect.centery = 100
		self.xDelta = 0
		self.yDelta = 0

	def update(self):
		g = 30
		xDist = self.rect.centerx - screenWidth/2
		yDist = self.rect.centery - screenHeight/2
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
		xDist = self.rect.centerx - screenWidth/2
		yDist = self.rect.centery - screenHeight/2
		dist = math.sqrt(xDist**2+yDist**2)

		angle = math.atan2(yDist, xDist)
		self.xDelta -= math.cos(angle) * g/dist
		self.yDelta -= math.sin(angle) * g/dist

	
		self.rect.x += self.xDelta
		self.rect.y += self.yDelta

		bounce = random.randrange(-2,2)
		if self.rect.centerx < 0:
			self.rect.centerx = 0
			self.xDelta *= bounce
		elif self.rect.centerx > screenWidth:
			self.rect.centerx = screenWidth
			self.xDelta *= bounce

		if self.rect.centery < 0:
			self.rect.centery = 0
			self.yDelta *= bounce
		elif self.rect.centery > screenHeight:
			self.rect.centery = screenHeight
			self.yDelta *= bounce


		if self.rect.centerx > screenWidth/2+100 or self.rect.centerx < screenWidth/2-100:
			if self in behindEarth:
				behindEarth.remove(self)
				infrontOfEarth.add(self)
			else:
				infrontOfEarth.remove(self)
				behindEarth.add(self)

#startup stuff###################################
pygame.init()
screenWidth = 2560
screenHeight = 1440
screen = pygame.display.set_mode((screenWidth,screenHeight),flags=pygame.NOFRAME)
clock = pygame.time.Clock()
frameCount = 0
players = pygame.sprite.Group()
behindEarth = pygame.sprite.Group()
infrontOfEarth = pygame.sprite.Group()
player1 = Player(1)
player2 = Player(2)
players.add(player1,player2)

foreignObjects = pygame.sprite.Group()
asteroid = ForeignObject(1)
foreignObjects.add(asteroid)

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
	players.update()
	foreignObjects.update()


	#draw stuff
	screen.blit(background,(0,0))
	
	if (frameCount % 600 == 0):
		blackHolePos = (random.randint(0,screenWidth*1),random.randint(0,screenHeight))
	if (frameCount % 600 < 100):
		screen.blit(blackHole0,(blackHolePos))
	elif (frameCount % 600 < 100):
		screen.blit(blackHole3,(blackHolePos))
	elif (frameCount % 600 < 200):
		screen.blit(blackHole2,(blackHolePos))
	elif (frameCount % 600 < 300):
		screen.blit(blackHole3,(blackHolePos))
	elif (frameCount % 600 < 400):
		screen.blit(blackHole2,(blackHolePos))
	elif (frameCount % 600 < 500):
		screen.blit(blackHole3,(blackHolePos))
	elif (frameCount % 600 < 600):
		screen.blit(blackHole3,(blackHolePos))
		
	#players.draw(screen)
	foreignObjects.draw(screen)
	behindEarth.draw(screen)
	screen.blit(earth,(screenWidth/2-36,screenHeight/2-36))
	infrontOfEarth.draw(screen)

	player1.image = player1.images[0]
	player2.image = player2.images[0]
	pygame.display.flip()

	#update frame counter
	frameCount += 1

#CLOCK MUST BE LAST###############################
	clock.tick(60)

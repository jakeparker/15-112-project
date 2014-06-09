import pygame
import numpy
from samus import *
from samus_weapons import *
from nettori import *
from background import *
from atlas import *
from interaction import *
import sys


# main_dir = os.path.split(os.path.abspath(__file__))[0]
# imagename = os.path.join(main_dir, 'data', 'arraydemo.bmp')
# imgsurface = pygame.image.load(imagename)

class Camera(object):
	def __init__(self, main):
		self.player = main.player
		self.rect = Rect(0,0,240*2,160*2)
		self.view = Rect(0,0,main.width,main.height)
		self.rect.center = self.player.rect.center

	def update(self):
		if self.player.rect.centerx > self.rect.centerx+16:
			self.rect.centerx = self.player.rect.centerx-16
		if self.player.rect.centerx < self.rect.centerx-16:
			self.rect.centerx = self.player.rect.centerx+16
		if self.player.rect.centery > self.rect.centery+16:
			self.rect.centery = self.player.rect.centery-16
		if self.player.rect.centery < self.rect.centery-16:
			self.rect.centery = self.player.rect.centery+16

		self.rect.clamp_ip(self.view)

class Game(object):
	def __init__(self):
		self.name = 'Main'

	def load_map(self):
		pathway = 'maps/map0/'
		self.map0 = load_image('map0', pathway)
		self.map0_clear = load_image('map0', pathway)
		self.map0_rect = self.map0.get_rect()
		map0_mask = load_image('map0_mask', pathway)
		self.map0_mask = pygame.surfarray.pixels3d(map0_mask)
		self.blank = load_image("blank", pathway)

	#def load_camera(self):
	#	self.x = 1411
	#	self.y = 132
	#	self.cameraX = self.x - self.width/2
	#	self.cameraY = self.y - self.height/2

	#def update_camera(self):

		# camera centered at player if wall out of view
		# if wall in view, camera is still, player moves
		
	#	rect = self.player.rect
	#	if (rect.left < self.cameraX) or (rect.right > self.cameraX+self.width):
	#		self.cameraX = rect.left - self.width/2
	#	if (rect.top < self.cameraY) or (rect.bottom > self.cameraY+self.height):
	#		self.cameraY = rect.top - self.height/2

	def load_colorKey(self):
		black = (0,0,0)         # out of bounds
		green = (0,249,0)       # wall segmen
		cyan = (0,253,255)      # playable area
		blue = (4,51,255)       # overlay
		magenta = (255,64,255)  # doorspore
		purple = (148,33,146)   # hatch
		orange = (255,147,0)    # elevator
		self.colorKey = [cyan, green, black, blue, magenta, purple, orange]

	def load_attributes(self):
		self.player = Samus(self, 250, 1411, 132)
		makeAtlas(self)
		makeBossAtlas(self)
		load_background(self)
		self.interaction = Interaction(self)

	def load_spriteGroups(self):
		self.LayeredUpdate = pygame.sprite.LayeredUpdates()
		self.enemyGroup = pygame.sprite.Group()
		self.enemyProjectiles = pygame.sprite.Group()
		self.playerProjectiles = pygame.sprite.Group()
		self.elevators = list() # list of classes, not sprites

	def keyEvent(self, event):
		if (event.key == pygame.K_y):
			self.running = not(self.running)
		elif (event.key == pygame.K_n):
			pygame.quit()
			sys.exit(0)

	def update(self):
		self.interaction.update()
		self.updateGroups()
		#self.update_camera()
		self.camera.update()

	def updateGroups(self):
		self.LayeredUpdate.update(pygame.time.get_ticks())

	def scaleImage(self, view_array, n):
		# numpy array scaling method based on:
		# http://osdir.com/ml/python.pygame/2001-12/msg00000.html
		if (view_array.shape[0] >= view_array.shape[1]):
			scaled =  numpy.repeat(numpy.repeat(view_array,n,1), n,0)
		else:
			scaled = numpy.repeat(numpy.repeat(view_array, n,0), n,1)
		return scaled

	def update_display(self):
		self.view.fill((0,0,0))
		#self.view.blit(self.map0, (0,0), (self.cameraX, self.cameraY, self.width, self.height))
		self.view.blit(self.map0, (0,0), (self.player.rect.centerx-self.camera.rect.centerx, self.player.rect.centery - self.camera.rect.centery, self.camera.rect.w, self.camera.rect.h))
		view_array = pygame.surfarray.array2d(self.view)
		scaled = self.scaleImage(view_array, self.scaleBy)
		pygame.surfarray.blit_array(self.screen, scaled)

	def run(self, width, height, scaleBy):
		self.running = True
		self.paused = False
		self.scaleBy = scaleBy
		self.width = width
		self.height = height
		#pygame.init()
		self.load_map()
		self.size = (self.width*self.scaleBy, self.height*self.scaleBy)
		self.screen = pygame.display.set_mode(self.size)
		self.view = pygame.Surface((self.width, self.height))
		pygame.display.set_caption("Metroid Fusion")
		#self.load_camera()
		self.load_colorKey()
		self.load_spriteGroups()
		self.load_attributes()
		self.camera = Camera(self)

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if (self.running == True) and (self.paused == False):
						self.player.keyEvent(event)
					else:
						self.keyEvent(event)
			if (self.running == True) and (self.paused ==False):
				self.update()
				self.LayeredUpdate.clear(self.map0, self.map0_clear)
				self.LayeredUpdate.draw(self.map0)
				self.update_display()
			else:
				self.game_over = pygame.surfarray.array2d(load_image("game_over", "sprites/bg/"))
				game_over = self.scaleImage(self.game_over, self.scaleBy)
				pygame.surfarray.blit_array(self.screen, game_over)

			pygame.display.update()



if __name__ == '__main__':
	game = Game()
	game.run(240*2, 160*2, 2)


import pygame, sys, pytmx, pyscroll
import pyscroll.data
from pygame.locals import *
from pytmx.tmxloader import load_pygame
from pyscroll.util import PyscrollGroup
from pygame.locals import *
import collections
import logging

from Music import Music
from IO import *

SCROLL_SPEED = 700

class Level(object):
	def __init__(self, game):
		screen = game.screen
		(w,h) = (screen.get_width(), screen.get_height())

		tmx_data = load_pygame(getFilePath(game.levelName))
		map_data = pyscroll.data.TiledMapData(tmx_data)

		self.map_layer = pyscroll.BufferedRenderer(map_data, (w,h), padding=1, clamp_camera=True)
		self.group = PyscrollGroup(map_layer=self.map_layer)

		self.center = [self.map_layer.rect.width/2, self.map_layer.rect.height/2]

		self.camera_acc = [0, 0, 0]
		self.camera_vel = [0, 0, 0]
		self.last_update = 0

		self.screen = screen

	def keyEvent(self):
		pressed = pygame.key.get_pressed()
		if pressed[K_UP]:
			self.camera_acc[1] = -SCROLL_SPEED * self.last_update
		elif pressed[K_DOWN]:
			self.camera_acc[1] = SCROLL_SPEED * self.last_update
		else:
			self.camera_acc[1] = 0

		if pressed[K_LEFT]:
			self.camera_acc[0] = -SCROLL_SPEED * self.last_update
		elif pressed[K_RIGHT]:
			self.camera_acc[0] = SCROLL_SPEED * self.last_update
		else:
			self.camera_acc[0] = 0


	def update(self, dt):
		self.map_layer.update()

		self.last_update = dt


		friction = pow(.0001, dt)

		self.camera_vel[0] += (self.camera_acc[0] * dt)
		self.camera_vel[1] += (self.camera_acc[1] * dt)

		self.camera_vel[0] *= friction
		self.camera_vel[1] *= friction

		if self.center[0] < 0:
			self.center[0] -= self.camera_vel[0]
			self.camera_acc[0] = 0
			self.camera_vel[0] = 0
		if self.center[0] >= self.map_layer.rect.width:
			self.center[0] -= self.map_layer.rect.width
			self.camera_acc[0] = 0
			self.camera_vel[0] = 0

		if self.center[1] < 0:
			self.center[1] -= self.camera_vel[1]
			self.camera_acc[1] = 0
			self.camera_vel[1] = 0
		if self.center[1] >= self.map_layer.rect.height:
			self.center[1] -= self.camera_vel[1]
			self.camera_acc[1] = 0
			self.camera_vel[1] = 0

		self.center[0] += self.camera_vel[0]
		self.center[1] += self.camera_vel[1]

		self.map_layer.center(self.center)


		




logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


class Game(object):
	def __init__(self, window):
		self.running = True
		self.paused = False
		self.window = window
		self.windowWidth = window.get_width()
		self.windowHeight = window.get_height()
		self.screen = pygame.Surface((240, 160))
		self.init_attributes()

	def init_attributes(self):
		self.levelName = 'Main_Deck.tmx'
		self.level = Level(self)


	def keyEvent(self, event):
		pass

	def update(self, dt):
		#self.screen.fill((0,0,0))
		#self.window.fill((0,0,0))
		self.level.update(dt)
		self.level.map_layer.draw(self.screen, self.screen.get_rect())

		
	def update_display(self):
		self.window.blit(pygame.transform.scale(self.screen, (self.windowWidth, self.windowHeight)), (0,0))
		pygame.display.flip()

	def run(self):
		clock = pygame.time.Clock()
		fps = 60
		fps_log = collections.deque(maxlen=20)
		while True:
			clock.tick(fps*2)
			try:
				fps_log.append(clock.get_fps())
				fps= sum(fps_log)/len(fps_log)
				dt = 1/fps
			except ZeroDivisionError: continue

			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					pygame.quit()
					sys.exit(0)
				elif (event.type == pygame.KEYDOWN):
						self.keyEvent(event)
				elif (event.type == VIDEORESIZE):
					pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					self.level.map_layer.set_size((event.w, event.h))
			self.level.keyEvent()
			self.update(dt)
			self.update_display()

if __name__ == '__main__':
	(width, height) = (640, 480)
	os.environ["SDL_VIDEO_CENTERED"] = "1"
	pygame.mixer.pre_init(44100, -16, 2, 512)
	pygame.init()
	pygame.display.set_mode((width, height), pygame.RESIZABLE)
	pygame.display.set_caption("Metroid Fusion")
	pygame.display.set_icon(load_image("mf_icon.png"))
	#pygame.mouse.set_visible(0)


	window = pygame.display.get_surface()
	game = Game(window)
	game.run()


import pygame, sys
from collections import defaultdict
from pygame.locals import *
from Music import Music
from IO import *
import Game


class Title(object):
	def __init__(self, window, width, height):
		(self.width, self.height) = (width, height)
		self.window = window
		self.windowWidth = self.window.get_width()
		self.windowHeight = self.window.get_height()
		self.title = pygame.Surface((240, 160))
		self.clock = pygame.time.Clock()
		self.init_title()
		self.update_title()

	def init_title(self):
		self.music = Music("mf02.ogg")
		self.image = load_image("intro.png")
		self.logo = load_image("mf_icon.png")
		#self.raw_text = "Press Any Key to Start"
		#self.font = pygame.font.Font(getFilePath("mf_font.ttf"), 16)
		#self.text = self.font.render(self.raw_text, 1, (210, 140, 31))

	def update_title(self):
		self.title.blit(self.image, (0,0))
		self.title.blit(self.logo, (0,0))
		#self.title.blit(self.text, (0,0))

	def update_display(self, surface):
		self.window.blit(pygame.transform.scale(surface, (self.windowWidth, self.windowHeight)), (0,0))
		pygame.display.flip()

##############################################

class Menu(Title):
	def __init__(self, window, width, height):
		super(Menu, self).__init__(window, width, height)
		self.running = True
		self.menu = pygame.Surface((240, 160))
		self.surface = self.title
		self.init_attributes()
		self.init_menu()
		self.update_menu()

	def init_attributes(self):
		self.selection = 0
		self.increment = 1
		self.slots = [ [1, None], [0, None], [0, None] ]
		self.spacerSpacing = (24, 46, 16)
		self.letterSpacing = (+8, -8)
		self.captionPos = (80, 4)

	def init_menu(self):
		background = ["menu"]
		caption = ["samus_data"]
		input_box = ["input"]
		spacers = ["spacer"]
		letters = ["A", "B", "C"]
		self.frames = defaultdict(int)
		self.frames.update({"A":1, "B":1, "C":1, "spacer":1, "menu":0, "samus_data":0, "input":0})
		images = [background, caption, input_box, spacers, letters]
		self.load_images(images)

	def load_images(self, images):
		self.images = dict()
		for imageList in images:
			for imageName in imageList:
				frames = self.frames[imageName]
				if (frames):
					for frame in xrange(frames+1):
						fileName = "%s_%d" % (imageName, frame)
						current_image = load_image(fileName+".png")
						self.images[fileName] = current_image
				else:
					fileName = imageName
					current_image = load_image(fileName+".png")
					self.images[fileName] = current_image

	def update_menu(self):
		self.menu.blit(self.images["menu"], (0,0))
		self.menu.blit(self.images["samus_data"], self.captionPos)
		spacerX = self.spacerSpacing[0]
		spacerY = self.spacerSpacing[1]
		spacerYAdj = self.spacerSpacing[2]
		letterXAdj = self.letterSpacing[0]
		letterYAdj = self.letterSpacing[1]

		for slot in xrange(len(self.slots)):
			highlight = self.slots[slot][0]
			letter = chr(ord("A")+slot) + "_%d"%(highlight)
			spacer = "spacer_%d"%(highlight)
			spacerPos = (spacerX, spacerY+spacerYAdj*slot)
			letterPos = (spacerPos[0]+letterXAdj, spacerPos[1]+letterYAdj)
			self.menu.blit(self.images[letter], letterPos)
			self.menu.blit(self.images[spacer], spacerPos)
		
	def highlightSelection(self):
		self.slots[self.selection][0] = 0

		self.selection += self.increment
		self.selection %= len(self.slots)

		self.slots[self.selection][0] = 1


	def keyEvent(self, event):
		if (event.key == K_UP) or (event.key == K_w):
			self.increment = -1
			self.highlightSelection()
			self.update_menu()
		elif (event.key == K_DOWN) or (event.key == K_s):
			self.increment = +1
			self.highlightSelection()
			self.update_menu()
		elif (event.key == K_RETURN):
			self.newGame()

	def newGame(self):
		self.running = False
		####################################
		print "ADD SAVE/LOAD GAME FEATURE"
		####################################
		game = Game.Game(self.window)
		game.run()


	def run(self):
		while self.running:
			self.clock.tick(30)
			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					pygame.quit()
					sys.exit(0)
				elif (event.type == pygame.KEYDOWN):
					if (self.surface != self.menu):
						self.surface = self.menu
						self.music = Music("mf01.ogg")

					else:
						self.keyEvent(event)


			self.update_display(self.surface)




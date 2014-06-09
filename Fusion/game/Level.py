import pygame, math
from pygame.locals import *
from itertools import chain, product, islice
from tmx import *




class Level(tmxMap):
	def __init__(self, levelName):
		super(Level, self).__init__(levelName)
		self.layers[0][1] = TileBuffer
		self.layers[1][1] = ImageBuffer
		self.parse(self.layers)
		for layer in self.layerlist:
			if isinstance(layer, TileLayer):
				for t in layer.tiles:
					if t.image == None:
						layer.tiles.remove(t)


class TileBuffer(TileLayer):
	def __init__(self, parent, node):
		super(TileBuffer, self).__init__(parent, node)
		self.screen = screen
		self.size = screen.get_size()
		self.name = levelName
		self.padding = padding
		self.clamp_camera = clamp_camera

		self.idle = False
		self.blank = True
		self.half_width = self.size[0]/2
		self.half_height = self.size[1]/2
		self.xoffset = 0
		self.yoffset = 0
		self.old_x = 0
		self.old_y = 0

		tw = self.tilewidth
		th = self.tileheight
		bw = self.size[0] + tw * self.padding
		bh = self.size[1] + th * self.padding
		pw = self.width * tw
		ph = self.height * th

		self.buffer = pygame.Surface((bw, bh))
		self.view = Rect(0,0, math.ceil(bw/tw), math.ceil(bh/th))
		self.rect = Rect(0,0, pw, ph)



		self.queue = iter([])

class ImageBuffer(ImageLayer):
	def __init__(self, parent, node):
		super(ImageBuffer, self).__init__(parent, node)

level = Level('Main_Deck.tmx')
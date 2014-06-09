from collections import defaultdict
from itertools import chain, product
import xml.etree.cElementTree as ET
from IO import *
import os


HorizontallyFlippedFlag = 0x80000000 # 1<<31
VerticallyFlippedFlag = 0x40000000 # 1<<30
AntiDiagonallyFlippedFlag = 0x20000000 # 1<<29
clearFlags = (HorizontallyFlippedFlag | VerticallyFlippedFlag | AntiDiagonallyFlippedFlag)


def decode_gid(gid):
	flags = 0
	if (gid & HorizontallyFlippedFlag):
		flags += 1
	if (gid & VerticallyFlippedFlag):
		flags += 2
	if (gid & AntiDiagonallyFlippedFlag):
		flags += 4
	# clear flags from gid
	gid &= ~(clearFlags)
	return gid, flags


tags = defaultdict(lambda: str)
tags.update({
	"version": float,
	"encoding": str,
	"compression": str,
	"width": int,
	"height": int,
	"tilewidth": int,
	"tileheight": int,
	"source": str,
	"id": int,
	"name": str,
	"value": str,
	"firstgid": int,
	"gid": int,
	"visible": lambda x: bool(eval(x)),
	"opacity": float,
	"type": str,
	"x": int,
	"y": int,
	})


def set_attributes(self, node):
	[setattr(self, key, tags[str(key)](val)) for (key, val) in node.items()]


class tmxMap(object):
	def __init__(self, levelName):
		self.name = levelName
		self.node = ET.parse(getFilePath(levelName)).getroot()
		self.layerlist = list()
		self.layerdict = dict()
		self.tilesets = list()
		self.gidmap = defaultdict(list)

		set_attributes(self, self.node)

		self.layers = [
		           ['layer', TileLayer], 
		           ['imagelayer', ImageLayer], 
		           ['objectgroup', ObjectLayer], 
		           ['tileset',  TileSet]
		              ]
 
	def parse(self, key, filename=None):
		if (filename):
			node = ET.parse(getFilePath(filename)).getroot()
		else:
			node = self.node

		for layer, instance in key:
			for subnode in node.findall(layer):
				instance(self, subnode)

	def __iter__(self): return chain([layer for layer in self.layerlist], 
									 [tileset for tileset in self.tilesets])
	def __repr__(self): return "tmxMap, %s" % self.name


class TileLayer(object):
	def __init__(self, parent, node):
		self.tiles = list()

		self.parent = parent
		self.name = None
		self.opacity = 1.0
		self.visible = True

		set_attributes(self, node)

		for (i,v) in enumerate(node.getiterator('tile')):
			row = i / self.width
			col = i % self.height
			raw_gid = int(v.items()[0][1])
			tile = Tile(self, row, col, raw_gid)

		if (self.name):
			self.parent.layerdict[self.name] = self
		self.parent.layerlist.append(self)

	def __iter__(self): raise NotImplementedError

	def __repr__(self): return "TileLayer, %s" % self.name


class ImageLayer(object):
	def __init__(self, parent, node):
		self.parent = parent
		self.name = None
		self.opacity = 1.0
		self.trans = None
		self.visible = True

		set_attributes(self, node)
		set_attributes(self, node.find('image'))
		
		try:
			self.image = load_image(self.source)
		except:
			self.image = None

		if (self.name):
			self.parent.layerdict[self.name] = self
		self.parent.layerlist.append(self)

	def __iter__(self): raise NotImplementedError

	def __repr__(self): return "ImageLayer, %s" % self.name


class ObjectLayer(object):
	def __init__(self, parent, node):
		self.objects = list()

		self.parent = parent
		self.name = None
		self.opacity = 1.0
		self.visible = True
		self.color = None

		set_attributes(self, node)

		for child in node.getiterator('object'):
			obj = Object(self, child)

		if (self.name):
			self.parent.layerdict[self.name] = self
		self.parent.layerlist.append(self)

	def __iter__(self): raise NotImplementedError

	def __repr__(self): return "ObjectLayer, %s" % self.name

class TileSet(object):
	def __init__(self, parent, node):
		self.parent = parent
		self.name = None
		self.margin = 0
		self.spacing = 0
		self.trans = None

		set_attributes(self, node)
		set_attributes(self, node.find('image'))

		for child in node.getiterator('tile'):
			(tiled_gid, flags) = decode_gid(int(child.get('id')))
			tiles = self.parent.gidmap[tiled_gid]
			for subnode in child.getiterator('property'):
				name = subnode.attrib['name']
				value = subnode.attrib['value']
				value = tags[str(name)](value)
				for tile in tiles:
					setattr(tile, name, value)
			
		ts_image = load_image(self.source)
		(w,h) = ts_image.get_size()
		m = self.margin
		sp = self.spacing
		tw = self.tilewidth
		th = self.tileheight
		stw = tw + sp
		sth = th + sp
		t_size = (tw, th)

		width = int((((w - m*2 + sp) / stw) * stw)-sp)
		height = int((((h - m*2 + sp) / stw) * stw)-sp)

		p = product(range(m, h+m, sth), range(m, w+m, stw))

		gidmap = self.parent.gidmap
		for tiled_gid, (row, col) in enumerate(p, self.firstgid):
			if col + tw-sp > width:
				continue
			tiles = gidmap[tiled_gid]
			t_image = ts_image.subsurface(((col, row), t_size))
			for tile in tiles:
				tile.image = t_image


		self.parent.tilesets.append(self)

	def __iter__(self): raise NotImplementedError

	def __repr__(self): return "TileSet, %s" % self.name

class Tile(object):
	def __init__(self, parent, row, col, raw_gid):
		self.parent = parent
		self.row = row
		self.col = col
		self.gid, self.flags = decode_gid(raw_gid)
		gidmap = self.parent.parent.gidmap
		gidmap[self.gid].append(self)

		self.name = None
		self.type = None
		self.image = None
		self.visible = True

		self.parent.tiles.append(self)

	def __iter__(self): raise NotImplementedError

	def __repr__(self): return "Tile, %s" % self.name


class Object(object):
	def __init__(self, parent, node):
		self.parent = parent

		self.name = None
		self.type = None
		self.width = 0
		self.height = 0
		self.gid = None
		self.visible = True

		self.parent.objects.append(self)

	def __iter__(self): raise NotImplementedError

	def __repr__(self): return "Object, %s" % self.name






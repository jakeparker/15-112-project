from collections import defaultdict
import xml.etree.cElementTree as ET
from IO import *


class Commands(object):
	def __init__(self):
		pass

	def getConfig(self):
		controls = defaultdict(int)
		controls.update(
			{
			119:'self.up',
			115:'self.down',
			97: 'self.left',
			100: 'self.right',
			113: 'self.slant',
			44: 'self.fire',
			46: 'self.mode',
			47: 'self.jump',
			} )


		etree = ET.ElementTree(file=getFilePath("config.xml"))
		for elem in etree.iter():
			print elem.tag, elem.attrib

# Config {}
# Controls {}
# down {'value': '115'}
# jump {'value': '47'}
# toggle {'value': '46'}
# right {'value': '100'}
# fire {'value': '44'}
# slant {'value': '113'}
# up {'value': '119'}
# left {'value': '97'}
# Settings {}

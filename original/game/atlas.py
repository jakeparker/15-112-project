import pygame
from pygame.locals import *

(w, h) = (240, 160)
rm0 = [1295+w*0, 0, w, h]

rm1 = [1295+w*1, 0, w, h]

rm2a = [1295+w*2, 0, w, h]   # a b
rm2b = [1295+w*3, 0, w, h]   # c d
rm2c = [1295+w*2, h*1, w, h] # e f
rm2d = [1295+w*3, h*1, w, h]
rm2e = [1295+w*2, h*2, w, h]
rm2f = [1295+w*3, h*2, w, h]

rm3 = [1295+w*1, h*1, w, h]

rm4a = [1295+w*4, h*2, w, h]
rm4b = [1295+w*5, h*2, w, h]

rm5a = [1295+w*6, h*2, w, h]
rm5b = [1295+w*7, h*2, w, h]

rm6c = [1295+w*1, h*2, w, h]
rm6b = [1295+w*0, h*2, w, h]
rm6a = [1295-w*1, h*2, w, h]

rm7a = [1295-w*1, h*3, w, h]
rm7b = [1295-w*1, h*4, w, h]
rm7c = [1295-w*1, h*5, w, h]


rm8e = [1295-w*1, h*6, w, h]
rm8f = [1295+w*0, h*6, w, h]
rm8g = [1295+w*1, h*6, w, h]
rm8h = [1295+w+2, h*6, w, h]
rm8i = [1295+w+3, h*6, w, h]

rm8a = [1295-w*5, h*6, w, h]
rm8aa = [1295-w*5, h*7, w, h]
rm8ab = [1295-w*5, h*8, w, h]

rm8b = [1295-w*4, h*6, w, h]
rm8ba = [1295-w*4, h*7, w, h]
rm8bb = [1295-w*4, h*8, w, h]
rm8bc = [1295-w*4, h*9, w, h]

rm8c = [1295-w*3, h*6, w, h]
rm8ca = [1295-w*3, h*7, w, h]
rm8cb = [1295-w*3, h*8, w, h]
rm8cc = [1295-w*3, h*9, w, h]

rm8d = [1295-w*2, h*6, w, h]

rm9 = [574, 1600, w, h]
rm10 = [814, 1632, 481, 319] # a,b,c,d combined
rm10a = [1295-w*2, h*10, w, h]
rm10b = [1295-w*1, h*10, w, h]
rm10c = [1295-w*2, h*11, w, h]
rm10d = [1295-w*1, h*11, w, h]

rm11 = [1295-w*4, h*10, w, h]

rm12a = [0, h*10, 96, 160]
rm12b = [1295-w*5, h*10, w, h]
rm12c = [0, h*11, 96, 160]
rm12d = [1295-w*5, h*11, w, h]

#from rm2d
rm13 = [2253, 201, 140, 219]

rm14 = [2395, 81, 291, 194] ### BOSS ROOM ###

#############################################


# hatch width = 7, height = 64

# room1
overlay4 = [1535+16, 80, 16, 64]
overlay0 = [1535, 80, 16, 64]
overlay1 = [1599, 80, 16, 64]
overlay2 = [1647, 80, 16, 64]
overlay3 = [1694, 80, 16, 64]

hatch0a = [1744, 80, 7, 64]

door0 = [1751, 80 , 48, 64]

# room2a
hatch0b = [1797, 80, 7, 64]

# room2c
hatch1b = [1821, 208, 7, 64]
door1 = [1295+w*2, 208, 23, 64]  # half door frame
hatch1a = [1295+w*2-7, 208, 7, 64]

# room2e
hatch2b = [1295+w*2+23, h*2+48, 7, 64]
door2 = [1295+w*2-24, h*2+48, 48, 64]
hatch2a = [1295+w*2-24-7, h*2+48, 7, 64] # room6c

# room2f
hatch3a = [2223, 369, 7, 64]
door3 = [2230, 369, 48, 64]
hatch3b = [2277, 369, 7, 64] # room5a

# room4b
hatch4a = [2704, 401, 7, 64]
door4 = [2711, 401, 48, 64]
hatch4b = [2758, 401, 7, 64]# room6a

### BOSS ROOM SKIPPED ###

# room6b
brokenDoor0 = [1263, 369, 64, 64]
overlay47 = [0,0,1,1] # place holder

# room6a
elevator0a = [1159, 433, 32, 8]
#overlay4. = [1151, 417, 48, 16]
overlay5 = [1159, 440, 32, 11]

# room7a
overlay6 = [1158, 485, 32, 14]
overlay7 = [1158, 533, 32, 14]
overlay8 = [1158, 581, 32, 14]
overlay9 = [1158, 629, 32, 14]

# room7b
overlay10 = [1158, 629+32, 32, 14]
overlay11 = [1158, 685, 32, 14]
overlay12 = [1158, 733, 32, 14]
overlay13 = [1158, 781, 32, 14]

# room7c
overlay14 = [1158, 806, 32, 14]
overlay15 = [1158, 853, 32, 14]
overlay16 = [1158, 902, 32, 14]
overlay17 = [1158, 949, 32, 14]

# room8e
overlay18 = [1151, 993, 48, 16]
elevator0b = [1158, 1073, 32, 8]
overlay19 = [1150, 1057, 48, 16]

# room8f
hatch5a = [2*1295+w-24-7, h*6+64, 7, 64] # locked
door5 = [2*1295+w-24, h*6+64, 48, 64] # closed
hatch5b = [2*1295+w+23, h*6+64, 7, 64] # locked

# room8d
hatch6b = [1295-w*2+23, h*6+64, 7, 64]
door6 = [1295-w*2-24, h*6+64, 48, 64]
hatch6a = [1295-w*2-24-7, h*6+64, 7, 64] # room8c

# room8c
elevator1b = [679, 1089, 32, 8]
overlay20 = [670, 1072, 48, 16]
overlay21 = [679, 1092, 32, 11]

# room8ca
overlay22 = [679, 1142, 32, 14]
overlay23 = [679, 1189, 32, 14]
overlay24 = [679, 1237, 32, 14]

# room8cb
overlay25 = [679, 1302, 32, 14]
overlay26 = [679, 1350, 32, 14]
overlay27 = [679, 1398, 32, 14]

# room8cc

overlay28 = [679, 1462, 32, 14]
overlay29 = [679, 1510, 32, 14]
overlay30 = [679, 1557, 32, 14]

# room9
overlay31 = [671, 1601, 48, 15]
elevator1a = [678, 1665, 32, 5]

hatch7a = [784, 1648, 7, 64]
door7 = [784+7, 1648, 48, 64]
hatch7b = [784+7+47, 1648, 7, 64] # room10a

# room10
overlay44 = [814, 1919, 48, 32] # water
overlay45 = [894, 1919, 48, 32] # water
overlay46 = [974, 1919, 48, 32] # water

####### BOSS ROOM SKIPPED #######

# room8a
hatch8a = [544, 1025, 7, 64]
door8 = [551, 1025, 48, 64]
hatch8b = [598, 1025, 7, 64]

# room8b
elevator2b = [439, 1089, 32, 8]
overlay32 = [430, 1073, 48, 16]
overlay33 = [439, 1096, 32, 14]

hatch9b = [311+47, 1025, 7, 64] # locked
door9 = [311, 1025, 48, 64]
hatch9a = [311-7, 1025, 7, 64] # room8a

# room8ba
overlay34 = [439, 1141, 32, 14]
overlay35 = [439, 1190, 32, 14]
overlay36 = [439, 1237, 32, 14]

# room8bb
overlay37 = [439, 1301, 32, 14]
overlay38 = [439, 1350, 32, 14]
overlay39 = [439, 1398, 32, 14]

# room8bc
overlay40 = [439, 1461, 32, 14]
overlay41 = [439, 1509, 32, 14]
overlay42 = [439, 1558, 32, 14]

# room11
elevator2a = [439, 1663, 32, 8]
overlay43 = [430, 1600, 48, 16]

hatch10b = [357, 1648, 7, 64]
door10 = [358-48, 1648, 48, 64]
hatch10a = [358-48-7, 1648, 7, 64]

####################################

def makeBossAtlas(main):

	brm0 = ['sa_x', [1852, 48, 321, 286] ]
	brm1 = ['mecha_ridley', [2419, 116,  224, 161] ]
	brm2 = ['omega_metroid', [2978, 320, 236, 160] ]
	brm3 = ['nettori', [813, 1791, 255, 160] ]
	brm4 = ['neo_ridley', [97, 1647, 237, 263] ]
	brms = [eval('brm%d'%num) for num in xrange(5)]
	
	spawn0 = [ 'SA_X', False, [1566, 80, 184, 66] ]
	spawn1 = [ 'Mecha_Ridley', False, [2174, 202, 221, 71] ]
	spawn2 = [ 'Omega_Metroid', False, [2467, 321, 267, 161] ]
	spawn3 = [ 'Nettori', False, [576, 1600, 237, 159] ]
	spawn4 = [ 'Neo_Ridley', False, [335, 1600, 239, 157] ]
	spawns = [ eval('spawn%s'%num) for num in xrange(5)]

	main.bossList = []
	main.bossSpawns = []
	main.bossRooms = dict()
	for brm in brms:
		boss = brm[0]
		bossRoom = Rect(brm[1])
		main.bossList.append(boss)
		main.bossRooms[boss] = bossRoom
	for spawn in spawns:
		bossClass = spawn[0] + "(self.main)"
		isSpawned = spawn[1]
		spawnRoom = Rect(spawn[2])
		main.bossSpawns.append([spawnRoom,isSpawned, bossClass])

def storeAtlas():
	rooms = [ 
	          rm0,rm1,rm2a,rm2b,rm2c,rm2d,rm2e,rm2f,rm3,rm4a,rm4b,rm5a,rm5b,
	          rm6c,rm6b,rm6a,rm7a,rm7b,rm7c,rm8e,rm8f,rm8g,rm8h,rm8i,rm8a,
	          rm8aa,rm8ab,rm8b,rm8ba,rm8bb,rm8bc,rm8c,rm8ca,rm8cb,rm8cc,rm8d,
	          rm9,rm10, rm10a,rm10b,rm10c,rm10d,rm11,rm12a,rm12b,rm12c,rm12d, rm13, rm14,
	        ]
	overlays = [eval('Rect(overlay%d)' % num) for num in xrange(48)]
	elevators = [ elevator0a, elevator0b, elevator1a,
	              elevator1b, elevator2a, elevator2b ]
	hatch_left = [eval('Rect(hatch%da)'%num) for num in xrange(11)]
	hatch_right = [eval('Rect(hatch%db)'%num) for num in xrange(11)]

	doors = [eval('Rect(door%d)'%num) for num in xrange(11)]

	brokenDoors = [eval('Rect(brokenDoor%d)'%num) for num in xrange(1)]

	for room in rooms:
		room = Rect(room)
	for elevator in elevators:
		elevator = Rect(elevator)
	return (rooms, overlays, elevators,
	 hatch_left, hatch_right, doors, brokenDoors)

def makeAtlas(self):
	(rms, ovrly, elvs, lh, rh,drs, brks) = storeAtlas()
	self.rooms = rms
	self.overlays = ovrly
	self.elevators = elvs
	self.left_hatches = lh
	self.right_hatches = rh
	self.doors = drs
	self.brokenDoors = brks
	return None










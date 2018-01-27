from __future__ import division
	
class Grid:
	arr = []	
	rows = 0
	cols = 0
	
	def __init__(self,r,c):
		self.arr = [[0 for j in range(c)] for i in range(r)]
		self.rows = r
		self.cols = c
	
	def cube_to_offset(self,cube):
		col = cube[0]
		row = cube[2] + (cube[0] - (cube[0]&1)) // 2
		return tuple([col, row])

	def offset_to_cube(self,hex):
		x = hex[0]
		z = hex[1] - (hex[0] - (hex[0]&1)) // 2
		y = -x-z
		return tuple([x, y, z])
	
	
	oddq_directions = [
	   [ tuple([+1,  0]), tuple([+1, -1]), tuple([ 0, -1]),
		 tuple([-1, -1]), tuple([-1,  0]), tuple([ 0, +1]) ],
	   [ tuple([+1, +1]), tuple([+1,  0]), tuple([ 0, -1]),
		 tuple([-1,  0]), tuple([-1, +1]), tuple([ 0, +1]) ]
	]

	def oddq_offset_neighbor(self,hex, direction):
		parity = hex[0] & 1
		dir = self.oddq_directions[parity][direction]
		return tuple([hex[0] + dir[0], hex[1] + dir[1]])
	
	def cube_distance(self,a, b):
		return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))	
	
	def offset_distance(self,a, b):
		ac = self.offset_to_cube(a)
		bc = self.offset_to_cube(b)
		return self.cube_distance(ac, bc)
		
	def cells_within_distance(self,hex,delta):
		center = self.offset_to_cube(hex)
		
		results = []
		for dx in range(-delta,delta+1):
			for dy in range(max(-delta, -dx-delta),min(delta, -dx+delta)+1):
				dz = -dx-dy
				results.append(tuple([center[0] + dx,center[1]+dy,center[2]+dz]))
				
		results = [self.cube_to_offset(it) for it in results]
		
		ret = []
		
		for it in results:
			if 0 <= it[0] < self.cols and 0 <= it[1] < self.rows:
				ret.append(it)
				
		return ret
		
	def getDirection(self,hex1,hex2):
		if hex1 == hex2: return -1
		cube1 = self.offset_to_cube(hex1)
		cube2 = self.offset_to_cube(hex2)
		temp = []
		temp.append(tuple([abs(cube1[0]-cube2[0]),2]))
		temp.append(tuple([abs(cube1[1]-cube2[1]),1]))
		temp.append(tuple([abs(cube1[2]-cube2[2]),0]))
		temp.sort(reverse = True)
		
		dx = cube2[0] - cube1[0]
		dy = cube2[1] - cube1[1]
		dz = cube2[2] - cube1[2]
		
		if temp[0][1] == 2:
			if temp[1][1] == 1:
				#(x,y)
				if dx > 0:
					if dy >= 0: return 1
					else: return 0
				else:
					if dy <= 0: return 4
					else: return 3
			else:
				#(x,z)
				
				if dx > 0:
					if dz >= 0: return 0
					else: return 1
				elif dx < 0:
					if dz <= 0: return 3
					else: return 4
				
		elif temp[0][1] == 1:
			if temp[1][1] == 2:
				#(y,x)
				
				if dy > 0:
					if dx >= 0: return 2
					else: return 3
				else:
					if dx <= 0: return 5
					else: return 0
				
			else:
				#(y,z)
				
				if dy > 0:
					if dz >= 0: return 3
					else: return 2
				else:
					if dz <= 0: return 0
					else: return 5
				
		else:	
			if temp[1][1] == 2:
				#(z,x)
				
				if dz > 0:
					if dx >= 0: return 5
					else: return 4
				else:
					if dx <= 0: return 2
					else: return 1
			else:
				#(z,y)
				
				if dz > 0:
					if dy >= 0: return 4
					else: return 5
				else:
					if dy <= 0: return 1
					else: return 2
"""				
g = Grid(10,10)
cell = tuple([1,2])
cell2 = tuple([1,0])

arr = g.cells_within_distance(cell,2)

for it in arr:
	#print(g.offset_distance(cell,it))
	print(it,g.offset_distance(cell,it))
	
print(g.oddq_offset_neighbor(cell,0))

print(g.getDirection(cell,cell2))
"""

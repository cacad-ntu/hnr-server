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
		x1 = hex1[0]
		y1 = hex1[1]
		x2 = hex2[0]
		y2 = hex2[1]
		 
	
# g = Grid(10,10)
# cell = tuple([1,2])

# arr = g.cells_within_distance(cell,2)

# for it in arr:
# 	#print(g.offset_distance(cell,it))
# 	print(it,g.offset_distance(cell,it))
	
# print(g.oddq_offset_neighbor(cell,0))

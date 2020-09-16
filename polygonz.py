from pygame import Vector2
import math
from ezgame import Game

class Polygon:
	vertices = []
	vertexNormals = []
	edgeNormals = []
	a = 0
	b = 0
	c = 0

	def __init__(self, vertices):
		self.vertices = vertices
	
	def render(self, game, renderVertices = True, renderNormals = True, normalLength = 1):
		if renderNormals and len(self.vertices) != len(self.vertexNormals):
			self.calculateNormals()

		game.setColor(255,255,255)
		if len(self.vertices) >= 3:
			game.polygon(self.vertices)
		if renderVertices:
			game.setColor(255,0,0)
			for v in self.vertices:
				game.circle(v, 1)
		if renderNormals:
			game.setColor(0,255,0)
			game.strokeWeight(1)
			if len(self.vertices) >= 3:
				for i in range(len(self.vertices)):
					game.line(self.vertices[i], self.vertices[i] + normalLength * self.vertexNormals[i])
					mid = (self.vertices[i-1] + self.vertices[i])*0.5
					game.line(mid, mid + normalLength * self.edgeNormals[i])

	def getSignedArea(self):
		area = 0
		for i in range(len(self.vertices)):
			area += self.vertices[i-1].cross(self.vertices[i])
		return area/2

	def calculateNormals(self):
		self.vertexNormals.clear()
		self.edgeNormals.clear()
		for i in range(len(self.vertices)):
			ab = (self.vertices[i] - self.vertices[i-1]).normalize()
			bc = (self.vertices[(i + 1) % len(self.vertices)] - self.vertices[i]).normalize()
			self.edgeNormals.append(Vector2(ab.y, - ab.x))
			xSum = ab.x + bc.x
			ySum = ab.y + bc.y
			if xSum == 0 and ySum == 0:
				self.vertexNormals.append(ab)
			else:
				self.vertexNormals.append(Vector2(ySum, -xSum).normalize())
			#self.vertexNormals.append(Vector2(ab.y + bc.y, -(ab.x + bc.x)).normalize())
	
	def expand(self, amount):
		if len(self.vertices) != len(self.vertexNormals):
			self.calculateNormals()
		
		for i in range(len(self.vertices)):
			self.vertices[i] += self.vertexNormals[i]*amount

	def calculateFactors(self):
		if len(self.vertices) != len(self.vertexNormals):
			self.calculateNormals()
		
		self.a = 0
		self.b = 0
		self.c = 0

		for i in range(len(self.vertices)):
			### Sum A ###
			vertexNormalAngle = calcAngle(self.vertexNormals[i-1], self.vertexNormals[i])
			if(self.vertexNormals[i-1].cross(self.vertexNormals[i]) < 0):
				vertexNormalAngle *= -1
			a = math.sin(vertexNormalAngle/2)*math.cos(vertexNormalAngle/2)
			self.a += a

			### Sum B ###
			alpha = math.pi/2 - calcAngle(self.vertexNormals[i-1], self.edgeNormals[i])
			beta  = math.pi/2 - calcAngle(self.vertexNormals[i], self.edgeNormals[i])
			if self.edgeNormals[i].cross(self.vertexNormals[i]) < 0:
				beta = math.pi - beta
			if self.vertexNormals[i-1].cross(self.edgeNormals[i]) < 0:
				alpha = math.pi - alpha
			if a == 0:
				self.b += (self.vertices[i] - self.vertices[i-1]).magnitude() * math.cos(calcAngle(self.vertexNormals[i], self.edgeNormals[i]))
			else:
				sinConstant = (self.vertices[i] - self.vertices[i-1]).magnitude() / math.sin(math.pi - alpha - beta)
				self.b += (sinConstant*math.sin(alpha) + sinConstant*math.sin(beta)) * a

			### Sum C ###
			self.c += self.vertices[i-1].cross(self.vertices[i])/2

	def setArea(self, value):
		self.calculateNormals()
		self.calculateFactors()
		self.expand((math.sqrt(abs(4*self.a*(value-self.c)+self.b*self.b))-self.b)/(2*self.a))

def clamp(a, b, c):
	return b if a < b else c if a > c else a

def calcAngle(a, b):
	return math.acos(clamp((a*b)/(a.magnitude()*b.magnitude()), -1, 1))

def setArea(vertices, area):
	vertexNormals = []
	edgeNormals = []
	for i in range(len(vertices)):
		ab = (vertices[i] - vertices[i-1]).normalize()
		bc = (vertices[(i + 1) % len(vertices)] - vertices[i]).normalize()
		edgeNormals.append(Vector2(ab.y, - ab.x))
		xSum = ab.x + bc.x
		ySum = ab.y + bc.y
		if xSum == 0 and ySum == 0:
			vertexNormals.append(ab)
		else:
			vertexNormals.append(Vector2(ySum, -xSum).normalize())
	
	a = 0
	b = 0
	c = 0

	for i in range(len(vertices)):
		### Sum A ###
		vertexNormalAngle = calcAngle(vertexNormals[i-1], vertexNormals[i])
		if(vertexNormals[i-1].cross(vertexNormals[i]) < 0):
			vertexNormalAngle *= -1
		currentA = math.sin(vertexNormalAngle/2)*math.cos(vertexNormalAngle/2)
		a += currentA

		### Sum B ###
		alpha = math.pi/2 - calcAngle(vertexNormals[i-1], edgeNormals[i])
		beta  = math.pi/2 - calcAngle(vertexNormals[i], edgeNormals[i])
		if edgeNormals[i].cross(vertexNormals[i]) < 0:
			beta = math.pi - beta
		if vertexNormals[i-1].cross(edgeNormals[i]) < 0:
			alpha = math.pi - alpha
		if math.pi - alpha - beta == 0:
			b += (vertices[i] - vertices[i-1]).magnitude() * math.cos(calcAngle(vertexNormals[i], edgeNormals[i]))
		else:
			sinConstant = (vertices[i] - vertices[i-1]).magnitude() / math.sin(math.pi - alpha - beta)
			b += (sinConstant*math.sin(alpha) + sinConstant*math.sin(beta)) * currentA

		### Sum C ###
		c += vertices[i-1].cross(vertices[i])/2
	
	expansion = (math.sqrt(abs(4*a*(area-c)+b*b))-b)/(2*a)

	for i in range(len(vertices)):
			vertices[i] += vertexNormals[i] * expansion
	pass
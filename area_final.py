import pygame
import math
#import polygonz as poly

PI = 3.141592653589793238462643383279
TWO_PI = PI*2

#Initialize pygame
pygame.init()

screenWidth = 800
screenHeight = 600

unitsize = 10
width = screenWidth / unitsize
height = screenHeight / unitsize

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Area Test")

clock = pygame.time.Clock()

running = True

black = (  0,   0,   0)
white = (255, 255, 255)
red   = (255,   0,   0)
green = (  0, 255,   0)
blue  = (  0,   0, 255)

currentColor = (0, 0, 0)
currentStrokeWeight = 5
mousePos = (0, 0)

target = 500

vertices = []
vertexNormals  = []
edgeNormals = []

def background(color):
	screen.fill(color)

#def setColor(r, g, b):
#	global currentColor
#	currentColor = (r, g, b)

def setColor(color):
	global currentColor
	currentColor = color

def strokeWeight(weight):
	global currentStrokeWeight
	currentStrokeWeight = weight

def circle(x, y, radius):
	pygame.draw.circle(screen, currentColor, worldToScreen((x, y)), radius)

#def line(x1, y1, x2, y2):
#	pygame.draw.line(screen, currentColor, worldToScreen((x1, y1)), worldToScreen(pygame.Vector2(x2, y2)), currentStrokeWeight)

def line(a, b):
	pygame.draw.line(screen, currentColor, worldToScreen(a), worldToScreen(b), currentStrokeWeight)

def polygon(points, filled=True):
	temp = []
	for p in points:
		temp.append(worldToScreen(p))
	pygame.draw.polygon(screen, currentColor, temp, 0 if filled else currentStrokeWeight)

def degToRad(degrees):
	return degrees * TWO_PI / 360

def calcAngle(a, b):
	return math.acos((a*b)/(a.magnitude()*b.magnitude()))	

def worldToScreen(point):
	return (int(point[0] * unitsize + screenWidth / 2), int(-point[1] * unitsize + screenHeight / 2))

def screenToWorld(point):
	return pygame.Vector2((point[0] - screenWidth / 2) / unitsize, -(point[1] - screenHeight / 2) / unitsize)

def expand(amount = 1):
	for i in range(len(vertices)):
		vertices[i] += vertexNormals[i] * amount

def calcNormals():
	vertexNormals.clear()
	edgeNormals.clear()
	for i in range(len(vertices)):
		ab = (vertices[i] - vertices[i-1]).normalize()
		bc = (vertices[(i + 1) % len(vertices)] - vertices[i]).normalize()
		edgeNormals.append(pygame.Vector2(ab.y, - ab.x))
		vertexNormals.append(pygame.Vector2(ab.y + bc.y, -(ab.x + bc.x)).normalize())

def calcArea():
	area = 0
	for i in range(len(vertices)):
		area += vertices[i-1].cross(vertices[i])
	return area/2

def calcFactors():
	sumA = 0
	sumB = 0
	sumC = 0

	for i in range(len(vertices)):
		### Sum A ###
		vertexNormalAngle = calcAngle(vertexNormals[i-1], vertexNormals[i])
		if(vertexNormals[i-1].cross(vertexNormals[i]) < 0):
			vertexNormalAngle *= -1
		a = math.sin(vertexNormalAngle/2)*math.cos(vertexNormalAngle/2)
		sumA += a

		### Sum B ###
		alpha = PI/2 - calcAngle(vertexNormals[i-1], edgeNormals[i])
		beta  = PI/2 - calcAngle(vertexNormals[i], edgeNormals[i])
		if edgeNormals[i].cross(vertexNormals[i]) < 0:
			beta = PI - beta
		if vertexNormals[i-1].cross(edgeNormals[i]) < 0:
			alpha = PI - alpha
		if a == 0:
			sumB += (vertices[i] - vertices[i-1]).magnitude() * math.cos(calcAngle(vertexNormals[i], edgeNormals[i]))
		else:
			sinConstant = (vertices[i] - vertices[i-1]).magnitude() / math.sin(PI - alpha - beta)
			sumB += (sinConstant*math.sin(alpha) + sinConstant*math.sin(beta)) * a

		### Sum C ###
		sumC += vertices[i-1].cross(vertices[i])/2

	return (sumA,sumB,sumC)

def fitToTarget():
	f = calcFactors()
	expansion = (math.sqrt(abs(4*f[0]*(target-f[2])+f[1]*f[1]))-f[1])/(2*f[0])
	expand(expansion)
	print(calcArea())
	return

"""
def fitToTarget():
	expansion = poly.getExpansion(vertices, target)
	expand(expansion)
	print(calcArea())
	return
"""
def loop():
	background(black)
	setColor(white)
	if len(vertices) >= 3:
		polygon(vertices)
	setColor(red)
	for v in vertices:
		circle(v.x, v.y, 4)
	setColor(green)
	strokeWeight(1)
	if len(vertices) >= 3:
		for i in range(len(vertices)):
			line(vertices[i], vertices[i] + 20 / unitsize * vertexNormals[i])
			mid = (vertices[i-1]+vertices[i])*0.5
			line(mid, mid + 20 / unitsize * edgeNormals[i])
	return

def keyPressed(key):
	global running
	if key == 'f':
		running = False
	elif key == 'c':
		vertices.clear()
		vertexNormals.clear()
	elif key == ' ':
		fitToTarget()
def keyReleased(key):
	return

def mousePressed(position, button):
	print(screenToWorld(position))
	vertices.append(screenToWorld(pygame.Vector2(position[0], position[1])))

	if len(vertices) >= 3:
		print(calcArea())
		calcNormals()
	return

def mouseReleased(position, button):
	return

vertices.append(pygame.Vector2( 5,  5))
vertices.append(pygame.Vector2(-5,  5))
vertices.append(pygame.Vector2(-5, -5))
vertices.append(pygame.Vector2( 0, -5))
vertices.append(pygame.Vector2( 0,  0))
vertices.append(pygame.Vector2( 5,  0))

calcNormals()

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			keyPressed(chr(event.key))
		elif event.type == pygame.KEYUP:
			keyReleased(chr(event.key))
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mousePressed(event.pos, event.button)
		elif event.type == pygame.MOUSEBUTTONUP:
			mouseReleased(event.pos, event.button)
		#print(event)
	mousePos = pygame.mouse.get_pos()
	loop()

	pygame.display.update() #update screen
	clock.tick(60)
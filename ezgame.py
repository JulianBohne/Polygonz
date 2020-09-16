import pygame

class Game:
    translation = pygame.Vector2(0, 0)
    scale = (1,1)

    def __init__(self, width, height, caption="Game Window", frameRate=60):
        self.width = width
        self.height = height
        self.running = True

        pygame.init()
        self.clock = pygame.time.Clock()

        self.canvas = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

        self.frameRate = frameRate
        self.currentColor = (0, 0, 0)
        self.currentStrokeWeight = 5
        self.mousePos = (0, 0)
    
    def addUpdate(self, updateFunction):
        self.updateFunction = updateFunction
    
    def addKeyPressed(self, keyPressedFunction):
        self.keyPressedFunction = keyPressedFunction

    def addKeyReleased(self, keyReleasedFunction):
        self.keyReleasedFunction = keyReleasedFunction

    def addMousePressed(self, mousePressedFunction):
        self.mousePressedFunction = mousePressedFunction

    def addMouseReleased(self, mouseReleasedFunction):
        self.mouseReleasedFunction = mouseReleasedFunction

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if hasattr(self, 'keyPressedFunction'):
                        self.keyPressedFunction(chr(event.key))
                elif event.type == pygame.KEYUP:
                    if hasattr(self, 'keyReleasedFunction'):
                        self.keyReleasedFunction(chr(event.key))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(self, 'mousePressedFunction'):
                        self.mousePressedFunction(event.pos, event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if hasattr(self, 'mouseReleasedFunction'):
                        self.mouseReleasedFunction(event.pos, event.button)
            #print(event)
            self.mousePos = pygame.mouse.get_pos()
            self.updateFunction()

            pygame.display.update() #update screen
            self.clock.tick(self.frameRate)

    def quit(self):
        self.running = False

    def translate(self, x):
        self.translation += pygame.Vector2(x[0], x[1])
    
    def scaleBy(self, scale):
        self.scale = (self.scale[0] * scale[0], self.scale[1] * scale[1])

    def background(self, color):
        self.canvas.fill(color)
    
    def setColor(self, r, g, b):
        self.currentColor = (r, g, b)
    
    def strokeWeight(self, weight):
        self.currentStrokeWeight = weight
    
    def circle(self, center, radius):
        pygame.draw.circle(self.canvas, self.currentColor, (int(center[0] * self.scale[0] + self.translation.x), int(center[1] * self.scale[1] + self.translation.y)), radius)
    
    def line(self, a, b):
        pygame.draw.line(self.canvas, self.currentColor, (pygame.Vector2(a[0] * self.scale[0], a[1] * self.scale[1])) + self.translation, (pygame.Vector2(b[0] * self.scale[0], b[1] * self.scale[1])) + self.translation, self.currentStrokeWeight)

    def polygon(self, points, filled=True):
        pygame.draw.polygon(self.canvas, self.currentColor, [((pygame.Vector2(p.x * self.scale[0], p.y * self.scale[1])) + self.translation) for p in points], 0 if filled else self.currentStrokeWeight)
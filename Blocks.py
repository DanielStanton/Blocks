import pygame
from random import randint
import math

class Entity():
    entities = []
    def __init__(self, size, location, colour, velocity=(0, 0)):
        Entity.entities.append(self)
        self.size = size
        self.surface = pygame.Surface(self.size)
        self.colour = colour
        self.surface.fill(self.colour)
        self.location = location
        self.velocity = velocity

    def update(self):
        newX = self.location[0] + self.velocity[0]
        newY = self.location[1] + self.velocity[1]
        #inX = (newX > (SCREEN_X - self.size[0])) or (newX < 0)
        #inY = (newY > (SCREEN_Y - self.size[1])) or (newY < 0)
        #if inX:
            #self.velocity = (-1 * self.velocity[0], self.velocity[1])
        #else:
            #self.velocity = (randint(-25, 25), self.velocity[1])
        #if inY:
            #self.velocity = (self.velocity[0], -1 * self.velocity[1])
        #else:
            #self.velocity = (self.velocity[0], randint(-25, 25))
        self.location = (newX, newY)

    def render(self, display):
        display.blit(self.surface, self.location)

class Bullet(Entity):
    bullets = []
    def __init__(self, location, colour, velocity):
        Bullet.bullets.append(self)
        Entity.__init__(self, (5, 5), location, colour, velocity)

    def __del__(self):
        Entity.entities.remove(self)
        Bullet.bullets.remove(self)
        #Entity.__del__(self)

class Fighter(Entity):
    fighters = []
    def __init__(self, location, velocity=(0,0)):
        Fighter.fighters.append(self)
        Entity.__init__(self, (15, 15), location,
                        (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.front = 0

    def update(self):
        Entity.update(self)
        self.front = math.atan2(self.velocity[1], self.velocity[0])

    def shoot(self):
        bulletVX = 20 * (math.cos(self.front))
        bulletVY = 20 * (math.sin(self.front))
        Bullet((self.location[0] + 5, self.location[1] + 5), self.colour,
               (self.velocity[0] + bulletVX, self.velocity[1] + bulletVY))

    def collides(self, location):
        inX = (location[0] >= self.location[0] and
               location[0] <= (self.location[0] + self.size[0]))
        inY = (location[1] >= self.location[1] and
               location[1] <= (self.location[1] + self.size[1]))
        if inX and inY:
            return True
        else:
            return False
        
    def __del__(self):
        self.colour = (255, 0, 0)
        Entity.entities.remove(self)
        Fighter.fighters.remove(self)
        #Entity.__del__(self)

class Player(Fighter):
    def setVelocity(self, velocity):
        self.velocity = velocity
        Fighter.update(self)
        

pygame.init()
SCREEN_X = 800
SCREEN_Y = 500
window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

isOpen = True
entitiesList = Entity.entities
bulletsList = Bullet.bullets
fightersList = Fighter.fighters

player = Player((SCREEN_X / 2, SCREEN_Y / 2))
for i in range(10):
    location = (randint(0, SCREEN_X - 15), randint(0, SCREEN_Y - 15))
    velocity = (randint(5, 10), randint(5, 10))
    Fighter(location, velocity)

while isOpen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isOpen = False
    window.fill((0, 0, 0))
    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[pygame.K_UP]:
        player.setVelocity((player.velocity[0], -0.1))
    elif pressedKeys[pygame.K_DOWN]:
        player.setVelocity((player.velocity[0], 0.1))
    else:
        player.setVelocity((player.velocity[0], 0))
    
    if pressedKeys[pygame.K_LEFT]:
        player.setVelocity((-0.1, player.velocity[1]))
    elif pressedKeys[pygame.K_RIGHT]:
        player.setVelocity((0.1, player.velocity[1]))
    else:
        player.setVelocity((0, player.velocity[1]))

    if pressedKeys[pygame.K_SPACE]:
        player.shoot()
        
    for entity in entitiesList:
        entity.update()
        entity.render(window)
    bulletIndexes = []
    fighterIndexes = []
    for bullet in bulletsList:
        for fighter in fightersList:
            if fighter.collides(bullet.location):
                fighterIndexes.append(fightersList.index(fighter))
                bulletIndexes.append(bulletsList.index(bullet))
    for i in range(len(bulletIndexes) - 1,  -1, -1):
        bulletsList[bulletIndexes[i]].__del__()
        fightersList[fighterIndexes[i]].__del__()
            
    pygame.display.flip()
    if not isOpen:
        pygame.display.quit()

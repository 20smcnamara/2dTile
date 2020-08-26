import math
import random
import time
import requests
import pygame
from pyglet.gl import *


window = pyglet.window.Window(fullscreen=True)
height = window.height
width = window.width
player_images = (pyglet.image.load('Resources/Bottom.png'), pyglet.image.load('Resources/Middle.png'))
TileTypes = {"grass_image": pyglet.image.load('Resources/grass.png'),
             "water_image": pyglet.image.load('Resources/water.png'),
             "sand_image": pyglet.image.load('Resources/sand.png'),
             "bush_image": pyglet.image.load('Resources/bush.png'),
             "FBbush_image": pyglet.image.load('Resources/FBbush.png'),
             "NBbush_image": pyglet.image.load('Resources/NBbush.png')}
keys = []
baseURL = "http://7f61b73e.ngrok.io/GameData/"
tile_size = int(height / 22)


@window.event
def on_key_press(symbol, modifiers):
    keys.append(chr(symbol))


@window.event
def on_key_release(symbol, modifiers):
    keys.remove(chr(symbol))


class drawnObject:

    def __init__(self):
        self.cord = [0, 0]

    def draw(self):
        pass


class Bullet(drawnObject):

    def __init__(self, cords, direction, weapon, shooter):
        super().__init__()
        self.cords = cords
        self.size = weapon.get_bullet_size()
        self.damage = weapon.get_damage()
        self.direction = direction
        self.shot_by = shooter

    def update(self):
        self.update_pos()
        return self.check_organism_collision() or self.check_valid()

    def update_pos(self):
        self.cords = [self.cords[0] + self.direction[0], self.cords[1] + self.direction[1]]

    def check_valid(self):
        if self.cords[0] < tiles[0][0].cords[0] or self.cords[1] < tiles[0][0].cords[1] or \
                self.cords[0] < tiles[0][0].cords[0] or self.cords[1] < tiles[0][0].cords[1]:
            return False
        return True

    def check_organism_collision(self):
        if self.shot_by != playerIndex:
            for player in players:
                cords = player.cords
                if pygame.Rect(cords[0], cords[1], tile_size - 20, tile_size - 20).collidelist(rects) != -1:
                    return player.take_damage(self.damage)
        return False

    def draw(self):
        glBegin(GL_LINES)
        glVertex3f(self.cords[0], self.cords[0], 0)
        glVertex3f(self.cords[0] + self.direction[0], self.cords[1] + self.direction[1], 0)
        glEnd()


class Gun:

    def __init__(self, damage, ammo, clip_size, bullet_size=7, fire_rate=15, speed=5):
        self.ammo = ammo
        self.damage = damage
        self.clip_size = clip_size
        self.ammo_in_clip = 0
        self.bullet_size = bullet_size
        self.fire_rate = fire_rate
        self.reload()
        self.last_show_time = time.time()
        self.speed = speed

    def reload(self):
        if self.ammo - self.ammo_in_clip > 0:
            while self.ammo > 0 and self.ammo_in_clip <= self.clip_size:
                self.ammo_in_clip += 1
                self.ammo -= 1

    def get_damage(self):
        return random.randint(self.damage[0], self.damage[1])

    def get_speed(self):
        return self.speed

    def is_loaded(self):
        return self.ammo_in_clip > 0 or self.ammo_in_clip == self.clip_size

    def get_bullet_size(self):
        return self.bullet_size

    def get_fire_rate(self):
        return self.fire_rate


class PeaShooter(Gun):

    def __init__(self):
        super().__init__([2, 7], 100, 12)


class Pistol(Gun):

    def __init__(self):
        super().__init__([20, 35], 100, 12)


class Sniper(Gun):

    def __init__(self):
        super().__init__([9800, 10000], 50, 5, bullet_size=3, fire_rate=1)


class Akkk(Gun):

    def __init__(self):
        super().__init__([47, 67], 50, 5, fire_rate=5, speed=7)


class MiniGun(Gun):

    def __init__(self):
        super().__init__([5, 7], 10000, 1000, fire_rate=3)


class Tile(drawnObject):

    def __init__(self, x, y, tile_size, type):
        super().__init__()
        self.cords = [x, y]
        self.size = tile_size
        self.type = type

    def draw(self):
        x, y = self.cords
        TileTypes[self.type].blit(x, y)

    def use(self):
        pass

class BushTile(Tile):

    def __init__(self, x, y, tile_size, type="bush_image"):
        super().__init__(x, y, tile_size, type)

    def regen(self):
        if self.maxHealth > self.health:
            self.health += 1

    def draw(self):
        x, y = self.cords
        if self.health == 0:
            TileTypes["NBbush_image"].blit(x, y)
            return
        if self.health < 6:
            TileTypes["FBbush_image"].blit(x, y)
            return
        TileTypes["bush_image"].blit(x, y)

    def use(self):
        if self.health == 0:
            return "0H"
        self.health -= 1
        return "5H"

class WaterTile(Tile):

    def __init__(self, x, y, tile_size, type="water_image"):
        super().__init__(x, y, tile_size, type)

    def regen(self):
        if self.maxHealth > self.health:
            self.health += 1

    def use():
        if random.randint(0, 20) == 13:
            self.health -= 1
            return "10H"
        return "0H"


tiles = []
bullets = []
objects = []
for row in range(-50, 50):
    new_row = []
    for col in range(-50, 50):
        tile = Tile(row * tile_size, col * tile_size, tile_size, "grass_image")
        new_row.append(tile)
        objects.append(tile)
    tiles.append(new_row)

def updateWorld():
    global tiles, objects
    URL = baseURL
    r = requests.get(url=URL).text
    index = 0
    for tile in r.split("%"):
        row = int(index / 100)
        col = int(index - row * 100)
        if row == 100:
            break
        index += 1
        if tile[:1] == "s":
            newTile = Tile(tiles[row][col].cords[0], tiles[row][col].cords[1], tile_size, "sand_image")
        if tile[:1] == "g":
            newTile = Tile(tiles[row][col].cords[0], tiles[row][col].cords[1], tile_size, "grass_image")
        if tile[:1] == "w":
            newTile = WaterTile(tiles[row][col].cords[0], tiles[row][col].cords[1], tile_size)
        if tile[:1] == "b":
            newTile = BushTile(tiles[row][col].cords[0], tiles[row][col].cords[1], tile_size)
        tiles[row][col] = newTile
        objects[index - 1] = newTile


playerIndex = -1
def connect():
    global  playerIndex
    URL = baseURL + "Players/Login"
    r = requests.get(url=URL).text
    playerIndex = int(r)


def disconnect():
    global  playerIndex
    URL = baseURL + "Players/Logout/" + "str"
    r = requests.get(url=URL).text
    playerIndex = int(r)


connect()
updateWorld()


def shoot(target=[], leaving=[], direction=[], shot_by=playerIndex, weapon=Pistol()):
    if len(direction) == 0:
        axis_distances = [math.fabs(leaving[0] - target[0]), math.fabs(leaving[1] - target[1])]
    else:
        axis_distances = direction
    x_direction = 1.25
    y_direction = 1.25
    if len(target) != 0:
        if target[0] < leaving[0]:
            x_direction *= -1
        if target[1] < leaving[1]:
            y_direction *= -1
    distance = (axis_distances[0]**2 + axis_distances[1]**2)**0.5 / weapon.get_speed()
    try:
        towards = [axis_distances[0] / distance * x_direction]
    except ZeroDivisionError:
        towards = [axis_distances[0] * x_direction]
    try:
        towards.append(axis_distances[1] / distance * y_direction)
    except ZeroDivisionError:
        towards.append(axis_distances[1] * y_direction)
    bullets.append(Bullet([leaving[0] + towards[0] * 5, leaving[1] + towards[1] * 5], towards, weapon, shot_by))


class Player(drawnObject):

    def __init__(self, cords):
        super().__init__()
        self.cords = cords
        self.speed = 20
        self.index = 0
        self.max_health = 100
        self.health = self.max_health
        self.delta = [0, 0]
        self.drownTimer = 0
        self.drowning = False
        self.dead = False

    def updateSkin(self, dt):
        self.index += 1

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.dead = True

    def draw(self):
        if not self.dead:
            x, y = self.cords
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            if self.index % 2:
                y += player_images[0].height - player_images[1].height
            player_images[self.index % 2].blit(x, y)


class MainPlayer(Player):

    def __init__(self):
        super().__init__(cords=[width / 2, height / 2])

    def move(self, dt, delta=[0, 0]):
        self.delta = [0, 0]
        if delta != [0, 0]:
            self.delta = delta
        for key in keys:
            self.handleKeyDown(key)

        # Handle X cords
        if (self.cords[0] > width / 2 and self.delta[0] < 0):
            self.cords[0] += self.delta[0]
            self.delta[0] = 0
            if self.cords[0] < width / 2:
                self.delta[0] = 0
                self.cords[0] = width / 2
        if (self.cords[0] < width / 2 and self.delta[0] > 0):
            self.cords[0] += self.delta[0]
            self.delta[0] = 0
            if self.cords[0] > width / 2:
                self.delta[0] = 0
                self.cords[0] = width / 2

        cords = tiles[0][0].cords
        if cords[0] - self.delta[0] > 0:
            self.cords[0] += self.delta[0]
            self.delta[0] = 0
            if self.cords[0] < 1:
                self.cords[0] = 1
                self.delta[0] = 0
        cords = tiles[99][99].cords
        if cords[0] - self.delta[0] < width - tile_size:
            self.cords[0] += self.delta[0]
            self.delta[0] = 0
            if self.cords[0] > width - 20:
                self.cords[0] = width - 20
                self.delta[0] = 0

        # Handle Y cords
        if (self.cords[1] > height / 2 and self.delta[1] < 0):
            self.cords[1] += self.delta[1]
            self.delta[1] = 0
            if self.cords[1] < height / 2:
                self.delta[1] = 0
                self.cords[1] = height / 2
        if (self.cords[1] < height / 2 and self.delta[1] > 0):
            self.cords[1] += self.delta[1]
            self.delta[1] = 0
            if self.cords[1] > height / 2:
                self.delta[1] = 0
                self.cords[1] = height / 2

        cords = tiles[0][0].cords
        if cords[1] - self.delta[1] > 0:
            self.cords[1] += self.delta[1]
            self.delta[1] = 0
            if self.cords[1] < 1:
                self.cords[1] = 1
                self.delta[1] = 0
        cords = tiles[99][99].cords
        if cords[1] - self.delta[1] < height - tile_size:
            self.cords[1] += self.delta[1]
            self.delta[1] = 0
            if self.cords[1] > height - 94:
                self.cords[1] = height - 94
                self.delta[1] = 0

        for object in objects:
            object.cords = [object.cords[0] - self.delta[0], object.cords[1] - self.delta[1]]

        cords = tiles[0][0].cords
        cords = [cords[0] + (width / 2 - self.cords[0]), cords[1] + (height / 2 - self.cords[1])]
        row = int(cords[0] / tile_size * -1 + width / tile_size / 2)
        col = int(cords[1] / tile_size * -1 + height / tile_size / 2)

        if self.drowning:
            if time.time() >= self.drownTime:
                self.drown()
            if tiles[row][col].type != "water_image":
                self.drowning = False
        with open("C:\\Users\\Sean\\PycharmProjects\\2dTile\\Updates", 'w') as f:
            f.write(baseURL + "Players/Update/" + str(row) + "/" + str(col) + "/" + str(playerIndex))

    def handleKeyDown(self, key):
        if key == 'w':
            self.delta[1] = self.speed
        if key == 's':
            self.delta[1] = -self.speed
        if key == 'a':
            self.delta[0] = -self.speed
        if key == 'd':
            self.delta[0] = self.speed

    def drown(self):
        self.drowned = True

    def useTile(self, dt):
        if not (" " in keys):
            return
        cords = tiles[0][0].cords
        cords = [cords[0] + (width / 2 - self.cords[0]), cords[1] + (height / 2 - self.cords[1])]
        row = int(cords[0] / tile_size * -1 + width / tile_size / 2)
        col = int(cords[1] / tile_size * -1 + height / tile_size / 2)
        output = tiles[row][col].use()
        if output[-1] == "H":
            self.health += eval(output[:-1])
            if self.health > self.max_health:
                 self.health = 100

    def drawGUI(self):
        if self.drowning:
            pyglet.text.Label(text="Drowning in: " + str(int(self.drownTime - time.time())), color=[0, 0, 255, 255],
                          x=width / 20, y=height / 20 + height / 75 * 1.5, font_size=height/75).draw()
        pyglet.text.Label(text="Health: " + str(self.health / self.max_health * 100) + "%", color=[255, 0, 0, 255],
                      x=width / 20, y=height / 20, font_size=height / 75).draw()


Main = MainPlayer()
pyglet.clock.schedule_interval(Main.move, 0.03)
pyglet.clock.schedule_interval(Main.updateSkin, 1)
pyglet.clock.schedule_interval(Main.useTile, 1)
fps_display = pyglet.window.FPSDisplay(window=window)
players = []


def updatePlayers():
    global objects
    URL = baseURL + "Players/"
    r = requests.get(url=URL).text
    for index, player in enumerate(r.split("p")):
        if player == '':
            return
        if player == index:
            continue
        cords = player.split("%")
        cords = [100 - int(str(cords[0])), 100 - int(str(cords[1]))]
        Maincords = tiles[0][0].cords
        Maincords = [Maincords[0] + (width / 2 - Main.cords[0]), Maincords[1] + (height / 2 - Main.cords[1])]
        row = Maincords[0] / tile_size * -1 + width / tile_size / 2
        col = Maincords[1] / tile_size * -1 + height / tile_size / 2
        newCords = [int(row - cords[0]) * tile_size, int(col - cords[1]) * tile_size]
        players.append(Player(cords=newCords))
    for i in range(9999, len(objects)):
        if type(objects[i]) is Player:
            del objects[i]
updatePlayers()
objects += players


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == 1:
        shoot(target=[x, y], leaving=[width / 2, height / 2])


@window.event
def on_draw():
    window.clear()
    cords = tiles[0][0].cords
    rowStart = int(cords[0] / tile_size * -1)
    colStart = int(cords[1] / tile_size * -1) - 1
    width_padding = int(math.ceil(width / tile_size)) + 1
    height_padding = int(math.ceil(height / tile_size)) + 1
    for row_index in range(rowStart, rowStart + width_padding):
        if row_index > 99:
            break
        for col_index in range(colStart, colStart + height_padding):
            if col_index > 99:
                break
            tiles[row_index][col_index].draw()
    for player in players:
        player.draw()
    for bullet in bullets:
        bullet.draw()
    Main.draw()
    Main.drawGUI()
    fps_display.draw()


@window.event
def on_close():
    pyglet.app.exit()
    disconnect()


pyglet.app.run()

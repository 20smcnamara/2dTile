import random
import pyglet


class drawnObject:

    def __init__(self):
        self.cord = [0, 0]


class Tile(drawnObject):

    def __init__(self, x, y, tile_size, type):
        super().__init__()
        self.cords = [x, y]
        self.size = tile_size
        self.type = type
        self.maxHealth = 10
        self.health = self.maxHealth

    def draw(self):
        x, y = self.cords
        TileTypes[self.type].blit(x, y)

    def use(self):
        return "0H"


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
        self.health += 1

    def use(self):
        if random.randint(0, 20) == 13:
            return "10H"
        return "0H"


tiles = []
objects = []
tile_size = 22
for row in range(-50, 50):
    new_row = []
    for col in range(-50, 50):
        tile = Tile(row * tile_size, col * tile_size, tile_size, "grass_image")
        new_row.append(tile)
        objects.append(tile)
    tiles.append(new_row)

def spawnWater(spawn_range, prob):  #TODO make it the prob is the size
    if 99 < spawn_range[0] or 99 < spawn_range[1] or spawn_range[2] < 1 or spawn_range[3] < 1:
        return
    if spawn_range[0] < 0:
        if spawn_range[2] * -1 < spawn_range[0]:
            return
        spawn_range[2] += spawn_range[0]
        spawn_range[0] = 0
    if spawn_range[1] < 0:
        if spawn_range[3] * -1 < spawn_range[1]:
            return
        spawn_range[3] += spawn_range[1]
        spawn_range[1] = 0
    if random.randint(0, 100) <= prob * 100:
        for row in range(int(spawn_range[0]), int(spawn_range[0] + spawn_range[2])):
            for col in range(int(spawn_range[1]), int(spawn_range[1] + spawn_range[3])):
                tile = WaterTile(tiles[row][col].cords[0], tiles[row][col].cords[1], tile_size)
                tiles[row][col] = tile
                objects[row * 100 + col] = tile
                if tiles[row - 1][col].type == "grass_image":
                    tiles[row - 1][col].type = "sand_image"
                if tiles[row + 1][col].type == "grass_image":
                    tiles[row + 1][col].type = "sand_image"
                if tiles[row][col + 1].type == "grass_image":
                    tiles[row][col + 1].type = "sand_image"
                if tiles[row][col - 1].type == "grass_image":
                    tiles[row][col - 1].type = "sand_image"

                if tiles[row - 1][col - 1].type == "grass_image":
                    tiles[row - 1][col - 1].type = "sand_image"
                if tiles[row + 1][col + 1].type == "grass_image":
                    tiles[row + 1][col + 1].type = "sand_image"
                if tiles[row + 1][col - 1].type == "grass_image":
                    tiles[row + 1][col - 1].type = "sand_image"
                if tiles[row - 1][col + 1].type == "grass_image":
                    tiles[row - 1][col + 1].type = "sand_image"
        for i in range(4):
            spawnWater([spawn_range[0] + spawn_range[2], spawn_range[1] + spawn_range[3] - i * spawn_range[3] / 4,
                       spawn_range[2] / 4, spawn_range[3] / 4], prob * .75)
            spawnWater([spawn_range[0] + i * spawn_range[2] / 4, spawn_range[1] + spawn_range[3],
                        spawn_range[2] / 4, spawn_range[3] / 4], prob * .75)
            spawnWater([spawn_range[0] + i * spawn_range[2] / 4, spawn_range[1] - i * spawn_range[3] / 4,
                       spawn_range[2] / 4, spawn_range[3] / 4], prob * .75)
            spawnWater([spawn_range[0] + i * spawn_range[2] / 4, spawn_range[1],
                       spawn_range[2] / 4, spawn_range[3] / 4], prob * .75)


pond_size = 16  #Should keep %4 = 0
sp_range = [random.randint(pond_size * 1.5, 100 - pond_size * 1.5), random.randint(pond_size * 1.5, 100 - pond_size * 1.5),
            pond_size , pond_size]
spawnWater(sp_range, 1)
pond_size = 8
sp_range = [random.randint(pond_size * 1.5, 100 - pond_size * 1.5), random.randint(pond_size * 1.5, 100 - pond_size * 1.5),
            pond_size , pond_size]
spawnWater(sp_range, 1)

for i in range(5):
    pond_size = 4
    sp_range = [random.randint(-1 * (100 - pond_size * 1.5), 100 - pond_size * 1.5),
                random.randint(-1 * (100 - pond_size * 1.5), 100 - pond_size * 1.5),
                pond_size, pond_size]
    spawnWater(sp_range, 1)

for x in range(100):
    row = random.randint(0, 99)
    col = random.randint(0, 99)
    if tiles[row][col].type != "grass_image" or row == col == 50:
        x -= 1
        continue
    bush = BushTile(tiles[row][col].cords[0], tiles[row][col].cords[1], tile_size)
    tiles[row][col] = bush
    objects[row * 100 + col] = bush


for index in range(100):
    tiles[index][0].type = "sand_image"
    tiles[index][99].type = "sand_image"
    tiles[0][index].type = "sand_image"
    tiles[99][index].type = "sand_image"

string = ""
with open("C:\\Users\\Sean\\PycharmProjects\\Something2d\\Server\\Game\\GameData\\Updates", "w") as f:
    for row in tiles:
        for col in row:
            print(col.type[:1], col.type)
            string += col.type[:1]+str(col.health)+"%"
        string+="."
    f.write(string)

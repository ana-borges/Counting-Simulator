import os
import pygame as pg
import random

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "assets")


class SpriteSheet:
    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pg.image.load(filename).convert()
        except pg.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tups = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tups, colorkey)

    def load_2dstrip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tupsUp = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        tupsLeft = [
            (rect[0] + rect[2] * x, rect[1] + rect[3] * 1, rect[2], rect[3])
            for x in range(image_count)
        ]
        tupsDown = [
            (rect[0] + rect[2] * x, rect[1] + rect[3] * 2, rect[2], rect[3])
            for x in range(image_count)
        ]
        tupsRight = [
            (rect[0] + rect[2] * x, rect[1] + rect[3] * 3, rect[2], rect[3])
            for x in range(image_count)
        ]

        return {
            "up": self.images_at(tupsUp, colorkey),
            "left": self.images_at(tupsLeft, colorkey),
            "down": self.images_at(tupsDown, colorkey),
            "right": self.images_at(tupsRight, colorkey),
        }


class CountingObject(pg.sprite.Sprite):
    """adds an object at a given position and with a given movement"""

    currentSpriteIndex = 0
    ramSprites = None
    directionX = 1
    directionY = 0

    def __init__(self, initialPos=(200, 200), allowedRoamingSpace=200, maxChangeDirectionRandom=250):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        ramSS = SpriteSheet("assets/ram_walk.png")
        ramSprites = ramSS.load_2dstrip((0, 0, 128, 128), 4, colorkey=(0, 0, 0))
        self.ramSprites = ramSprites
        self.image = ramSprites["right"][0]
        self.rect = ramSprites["right"][0].get_rect()
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = initialPos
        self.initialPos = initialPos
        self.allowedRoamingSpace = allowedRoamingSpace
        self.maxChangeDirectionRandom = maxChangeDirectionRandom

    def update(self):
        self.currentSpriteIndex += 1

        if self.rect.x - self.initialPos[0] > self.allowedRoamingSpace:
            self.directionX = -1
            self.directionY = 0
        if self.initialPos[0] - self.rect.x > self.allowedRoamingSpace:
            self.directionX = 1
            self.directionY = 0
        if self.rect.y - self.initialPos[1] > self.allowedRoamingSpace:
            self.directionX = 0
            self.directionY = -1
        if self.initialPos[1] - self.rect.y > self.allowedRoamingSpace:
            self.directionX = 0
            self.directionY = 1

        changeDirectionRandom = random.randint(0, self.maxChangeDirectionRandom)
        if changeDirectionRandom == 1:
            self.directionX = 0
            self.directionY = 1
        if changeDirectionRandom == 2:
            self.directionX = 0
            self.directionY = -1
        if changeDirectionRandom == 3:
            self.directionX = -1
            self.directionY = 0
        if changeDirectionRandom == 4:
            self.directionX = 1
            self.directionY = 0

        self.image = self.ramSprites[self.getDirection()][int(self.currentSpriteIndex / 4) % 4]
        self.rect.x += 1 * self.directionX
        self.rect.y += 1 * self.directionY


    def getDirection(self):
        if self.directionX == 1 and self.directionY == 0:
            return "right"
        if self.directionX == -1 and self.directionY == 0:
            return "left"
        if self.directionX == 0 and self.directionY == 1:
            return "down"
        if self.directionX == 0 and self.directionY == -1:
            return "up"
        return "error"

def generateHerd(num):
    herd = []
    for _ in range(num):
        randX = random.randint(200, 600)
        randY = random.randint(200, 600)
        herd.append(CountingObject(initialPos=(randX,randY)))
    return herd

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

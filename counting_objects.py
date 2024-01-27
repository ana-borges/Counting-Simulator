import os
import pygame as pg

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

        print (tupsLeft)
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

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        ramSS = SpriteSheet('assets/ram_walk.png')
        ramSprites = ramSS.load_2dstrip((0, 0, 128, 128), 4, colorkey=(0, 0, 0))
        self.ramSprites = ramSprites
        self.image = ramSprites["right"][0]
        self.rect = ramSprites["right"][0].get_rect()
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 90
        #self.move = 18

    def _walk(self):
        """move the object across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, True, False)
        self.rect = newpos

    def update(self):
        self.rect.x += 1
        self.currentSpriteIndex += 1
        self.image = self.ramSprites["right"][int(self.currentSpriteIndex/4)%4]
        if self.rect.right > 500:
            self.kill()

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
import os
import pygame as pg
import counting_objects as co

from level import Level

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

def main():
    """this function is called when the program starts.
    it initializes everything it needs, then runs in
    a loop until the function returns."""
    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((1000, 1000), pg.SCALED)
    pg.display.set_caption("Counting Simulator")

    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((102, 204, 10))

    # Load level and failure sound
    currentLevel = Level("what is my age", "uh_you_suck.wav", 2, 5)
    failureSound = pg.mixer.Sound(currentLevel.failureSound)

    # Put Text On The Background, Centered
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("How many objects are there?", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=background.get_height() - 100)
        background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare Game Objects
    sheep = co.CountingObject()
    allobjects = pg.sprite.Group(sheep)
    allobjects.draw(screen)
    clock = pg.time.Clock()

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                # Close window if user presses ESC
                going = False
            elif event.type == pg.KEYDOWN:
                print("A key! A key, I say!")
                pg.mixer.Sound.play(failureSound)

        allobjects.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allobjects.draw(screen)
        pg.display.flip()

    pg.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

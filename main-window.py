import os
import pygame as pg
import counting_objects as co
import pygame_textinput as ti

from level import SheepLevel, LevelInterface

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
    currentLevel: LevelInterface = SheepLevel("How many objects are there?", 0, initial_timer=10)

    # Put Text On The Background, Centered
    if not pg.font:
        return 1

    font = pg.font.Font(None, 64)
    text = font.render("How many objects are there?", True, (0, 0, 0))
    textpos = text.get_rect(centerx=background.get_width() / 2, y=background.get_height() - 100)
    background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare Game Objects
    sheeps = co.generateHerd(currentLevel.get_amount_of_objects())
    allobjects = pg.sprite.Group(sheeps)
    allobjects.draw(screen)
    clock = pg.time.Clock()

    # Create TextInput-object with at most 15 characters
    manager = ti.TextInputManager(validator=lambda input: len(input) <= 15)
    textinput = ti.TextInputVisualizer(manager)

    # Start the timer of the level
    currentLevel.start()

    # Main Loop
    going = True
    timer = 0
    while going:
        clock.tick(60)
        if not currentLevel.is_stopped():
            timer = currentLevel.check_time_left()

        events = pg.event.get()

        # Handle Input Events
        for event in events:
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                # Close window if user presses ESC
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                allobjects = currentLevel.register_answer(textinput.value, allobjects)
                textinput.value = ""
                textinput.cursor_pos = 0

        allobjects.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allobjects.draw(screen)


        timerColor=(0,0,0)
        if timer <= 5:
            timerColor=(255,0,0)
        text = font.render(str(timer), True, timerColor)
        textpos = text.get_rect(centerx=background.get_width() - 100, y=50)
        screen.blit(text, textpos)

        textinput.update(events)
        screen.blit(textinput.surface, (background.get_width() / 2 - 150, background.get_height() - 50), (0,0,300,100))

        pg.display.flip()

    pg.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

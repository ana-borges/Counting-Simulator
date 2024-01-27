import math

import pygame as pg
import pygame.camera as ca
import pygame_textinput as ti

import counting_objects as co
import reaction
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
    ca.init()
    camlist = ca.list_cameras()
    if camlist:
        cam = ca.Camera(camlist[0], (1920, 1080), "RGB")
    cam.start()
    print(cam.get_size())
    screen = pg.display.set_mode((co.screen_width, co.screen_height), pg.SCALED)
    pg.display.set_caption("Counting Simulator")

    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((102, 204, 10))

    snapshot = pg.surface.Surface((1920, 1080), 0, screen)

    # Load level and failure sound
    currentLevel: LevelInterface = SheepLevel("How many objects are there?", 0)

    # Put Text On The Background, Centered
    if not pg.font:
        return 1

    font = pg.font.Font(None, 64)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Get the fence
    vertical_fence, vertical_fence_rect = co.load_image("vertical_fence.png",-1,2)
    horizontal_fence, horizontal_fence_rect = co.load_image("horizontal_fence.png",-1,2)

    # Get X
    errorScreen, errorScreenRect = co.load_image("x.png",-1,8)

    # Prepare Game Objects
    sheeps = co.generateHerd(currentLevel.get_amount_of_objects() - 1)
    allobjects = pg.sprite.Group(sheeps)
    clock = pg.time.Clock()

    # Sheep that dies
    dyingSheep = co.generateHerd(1)
    dyingSheepObjects = pg.sprite.Group(dyingSheep)

    # Create TextInput-object with at most 15 characters
    manager = ti.TextInputManager(validator=lambda input: len(input) <= 15)
    textinput = ti.TextInputVisualizer(manager)

    # Start the timer of the level
    currentLevel.start()

    # Main Loop
    going = True
    timer = 0
    errorScreenTimer = 0
    fps=60
    show_picture = False

    while going:
        clock.tick(fps)
        events = pg.event.get()
        if currentLevel.is_stopped():
            if reaction.ask_picture_question:
                if pg.mixer.get_busy():
                    continue
                for event in events:
                    if event.type == pg.QUIT:
                        going = False
                    elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        # Close window if user presses ESC
                        going = False
                    elif event.type == pg.KEYDOWN and event.key == pg.K_y:
                        pg.mixer.Sound.play(pg.mixer.Sound("sounds/YES_PICTURE.wav"))
                        reaction.ask_picture_question = False
                        snapshot = cam.get_image(snapshot)
                        screen.blit(snapshot, (-500, -200))
                        show_picture = True
                    elif event.type == pg.KEYDOWN and event.key == pg.K_n:
                        pg.mixer.Sound.play(pg.mixer.Sound("sounds/NO_PICTURE.wav"))
                        reaction.ask_picture_question = False
            else:
                for event in events:
                    if event.type == pg.QUIT:
                        going = False
                    elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        # Close window if user presses ESC
                        going = False
                    elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                        currentLevel.reset()
                        sheeps = co.generateHerd(currentLevel.get_amount_of_objects()-1)
                        allobjects = pg.sprite.Group(sheeps)
                        dyingSheep = co.generateHerd(1)
                        dyingSheepObjects = pg.sprite.Group(dyingSheep)
                        textinput.value = ""
                        textinput.cursor_pos = 0
                        errorScreenTimer = 0
                        show_picture = False
                        reaction.deadSheep = False
        else:
            timer = currentLevel.check_time_left()

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

        if not reaction.ask_picture_question and not show_picture:
            allobjects.update()
            dyingSheepObjects.update(currentLevel.is_stopped() and reaction.deadSheep, None)


        if not show_picture:
            # Draw background
            screen.blit(background, (0, 0))

            # Draw fence
            full_fence_height = co.rb_botleft[1] - co.rb_topleft[1]
            small_fence_height = vertical_fence.get_height()
            number_of_small_vfences = math.ceil(full_fence_height / small_fence_height)
            for i in range(number_of_small_vfences):
                screen.blit(vertical_fence,(co.rb_topleft[0], co.rb_topleft[1] + small_fence_height * i))
                screen.blit(vertical_fence,(co.rb_topright[0], co.rb_topright[1] + small_fence_height * i))

            full_fence_width = co.rb_topright[0] - co.rb_topleft[0]
            small_fence_width = horizontal_fence.get_width() + 5
            number_of_small_hfences = math.ceil(full_fence_width / small_fence_width)
            for i in range(number_of_small_hfences):
                screen.blit(horizontal_fence,(co.rb_topleft[0] + small_fence_width * i, co.rb_topleft[1]))
                screen.blit(horizontal_fence,(co.rb_botleft[0] + small_fence_width * i, co.rb_botleft[1]))

            allobjects.draw(screen)
            dyingSheepObjects.draw(screen)
        else:
            screen.blit(snapshot, (-500, -200))

        if currentLevel.is_stopped() and not reaction.ask_picture_question:
            text = font.render("Press enter to reset", True, (10, 10, 10))
            textpos = text.get_rect(centerx=background.get_width() / 2, y=background.get_height() / 2)
            screen.blit(text, textpos)
        elif reaction.ask_picture_question:
            text = font.render("Press 'y' to take a picture or 'n' if not.", True, (10, 10, 10))
            textpos = text.get_rect(centerx=background.get_width() / 2, y=background.get_height() / 2)
            screen.blit(text, textpos)
        elif not currentLevel.is_stopped():
            text = font.render(currentLevel.get_question(), True, (10, 10, 10))
            textpos = text.get_rect(centerx=background.get_width() / 2, y=background.get_height() - 100)
            screen.blit(text, textpos)

        

        if not currentLevel.is_stopped():
            textinput.update(events)
            screen.blit(textinput.surface, (background.get_width() / 2 - 100, textpos[1] + 50), (0,0,300,100))

        if currentLevel.is_stopped() and errorScreenTimer <= 3*fps and not reaction.ask_picture_question and not show_picture:
            screen.blit(errorScreen,(0,0))
            errorScreenTimer += 1

        # Timer
        timerColor=(0,0,0)
        if timer <= 5:
            timerColor=(255,0,0)
        text = font.render(str(timer), True, timerColor)
        textpos = text.get_rect(centerx=co.rb_topright[0], y=co.rb_topright[1] - 50)
        screen.blit(text, textpos)

        pg.display.flip()

    pg.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

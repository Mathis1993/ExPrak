from psychopy import visual, core, event
import random
import math


def present_instruction(win, dispsize, instruction):
    text = visual.TextStim(win,
                           text=instruction,
                           color=[-1, -1, -1],
                           font='Arial',
                           height=30,
                           wrapWidth=int(0.8 * dispsize[0])
                           )
    text.draw()
    win.flip()
    event.waitKeys(keyList=['return'])


def draw_fixation(win, time):
    fixation = visual.ShapeStim(win,
        vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
        lineWidth=5,
        closeShape=False,
        lineColor='black'
    )
    fixation.draw()
    win.flip()
    core.wait(time)
    # check for quit (the Esc key)
    if event.getKeys(keyList=["escape"]):
        core.quit()


def present_stimuli_day_1(win, stimulus, time):
    image = stimulus
    image.draw()
    win.flip()
    core.wait(time)


def feedback(win, dispsize, message, farbe, wait):
    FB = visual.TextStim(
            win,
            text=message,
            color=farbe,
            font="Arial",
            height=30,
            wrapWidth=int(0.8*dispsize[0])
        )
    FB.draw()
    win.flip()
    core.wait(wait)


def reminder(win, dispsize, text, position):
    reminder = visual.TextStim(win, text=text, pos=position,
                            color="black",
                            font='Arial',
                            height=30,
                            wrapWidth=int(0.8 * dispsize[0])
                            )
    reminder.draw()


def present_stimuli_day_2(win, stimulus, key_new, key_old, reminder_1, reminder_2, pos_new, pos_old, presentation_time):
    image = stimulus
    image.draw()
    win.flip()
    core.wait(presentation_time)
    win.flip()
    reminder_1.setText("New")
    reminder_1.setPos(pos_new)
    reminder_2.setText("Old")
    reminder_2.setPos(pos_old)
    reminder_1.draw()
    reminder_2.draw()
    win.flip()
    resp_on = event.waitKeys(keyList=[key_new, key_old])
    reminder_1.setText("Remember")
    reminder_1.setPos(pos_new)
    reminder_2.setText("Know")
    reminder_2.setPos(pos_old)
    reminder_1.draw()
    reminder_2.draw()
    win.flip()
    resp_rk = event.waitKeys(keyList=[key_new, key_old])
    return resp_on, resp_rk


def selection_rectangle(win, stim):
    # Instantiation of event class with mouse method
    myMouse = event.Mouse()  # will use win by default

    # Instantiation of Rectangle that makes up the selection rectangle (invisible at first, s. height and length)
    rect = visual.Circle(win, radius = 0.5, edges = 32, pos=(0, 0), lineColor="black")

    # Instantiate image object
    image = stim

    # Set up counter for only recording coordinates of the first left-button click and release (so the first drag)
    i = 0
    j = 0

    # Create current position variable so that it is known to the system in the frames where i ==0
    curr_pos = [0, 0]

    # Stop when any keyboard key is pressed
    while not event.getKeys():
        # Poll Mouse Button States (mouse1 is left button)
        mouse1, mouse2, mouse3 = myMouse.getPressed()
        image.draw()
        win.flip()

        # While mouse1 == True, so while left button is pressed
        while (mouse1):
            # Poll further to notice when being released (State switches to false again)
            mouse1, mouse2, mouse3 = myMouse.getPressed()

            # so that the starting position is only saved for the very first frame of the press
            if i == 0:
                # set starting position
                start_pos = myMouse.getPos()
                # make selection rectangle invisible so that after a "n" response the old one isn't displayed for one frame
                rect.setRadius(0)
                #rect.setWidth(0)
                # set starting position of selection rectangle (at current size of 1x1 pixel)
                rect.setPos(start_pos)
                # draw rectangle and flip window
                image.draw()
                rect.draw()
                win.flip()
                # print coordinates of starting position
                print(start_pos)
                # set counters to one so that this happens only for the first click
                i = 1
                j = 1

            # Update current mouse position every frame
            curr_pos = myMouse.getPos()
            # Take Betrag des Abstandes der Koordinaten to determine width and height of the current rectangle in this frame
            radius = math.sqrt(abs(start_pos[0] - curr_pos[0]) ** 2 + abs(start_pos[1] - curr_pos[1]) **2)
            #height = abs(start_pos[1] - curr_pos[1])
            # go from x-start to middle of the rectangle (i.e. position) relative to the value of pos_current in this frame
            #position = [start_pos[0] + 0.5 * (curr_pos[0] - start_pos[0]),
            #            start_pos[1] + 0.5 * (curr_pos[1] - start_pos[1])]
            # update rectangle
            rect.setRadius(radius)
            #rect.setHeight(height)
            #rect.setPos(position)
            image.draw()
            rect.draw()
            win.flip()

        # if left button is released, take end position (also only for one frame and not for every frame thereafter
        if j == 1:
            #end_pos = curr_pos
            #pos = position
            end_radius = radius
            # and print it out
            print(start_pos, end_radius)
            # wait for response: was that the part of the image the subject wanted to select?
            resp = event.waitKeys(keyList=["y", "n"])
            # if confirmed, exit
            if resp == ["y"]:
                break
                # win.close()
                # core.quit()
            # if not, start over again (rectangle is then set to zero height and length in lines 43 and 44 to make the old one disappear)
            else:
                i = 0
                j = 0

    return start_pos, end_radius
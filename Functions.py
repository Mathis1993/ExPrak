from psychopy import visual, core, event
import random


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


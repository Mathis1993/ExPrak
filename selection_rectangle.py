from psychopy import visual, core, event

win = visual.Window(
    size=[600, 600], #fullscr auf True ueberschreibt size
    units="pix",
    fullscr=False,
    color=[1, 1, 1]
)

def selection_rectangle(window, stim):

    #Instantiation of event class with mouse method
    myMouse = event.Mouse()  #  will use win by default
    
    #Instantiation of Rectangle that makes up the selection rectangle (invisible at first, s. height and length)
    rect = visual.Rect(window, width=0, height=0, pos=(0,0), lineColor="black")
    
    #Instantiate image object
    image = visual.ImageStim(win, image = stim, size = [600, 600])
    
    #Set up counter for only recording coordinates of the first left-button click and release (so the first drag)
    i = 0
    j = 0
    
    #Create current position variable so that it is known to the system in the frames where i ==0
    curr_pos=[0,0]
    
    #Stop when any keyboard key is pressed
    while not event.getKeys():
        #Poll Mouse Button States (mouse1 is left button)
        mouse1, mouse2, mouse3 = myMouse.getPressed()
        image.draw()
        win.flip()
    
        #While mouse1 == True, so while left button is pressed
        while (mouse1):
            #Poll further to notice when being released (State switches to false again)
            mouse1, mouse2, mouse3 = myMouse.getPressed()
    
            #so that the starting position is only saved for the very first frame of the press
            if i==0:
                #set starting position
                start_pos = myMouse.getPos()
                #make selection rectangle invisible so that after a "n" response the old one isn't displayed for one frame
                rect.setHeight(0)
                rect.setWidth(0)
                #set starting position of selection rectangle (at current size of 1x1 pixel)
                rect.setPos(start_pos)
                #draw rectangle and flip window
                image.draw()
                rect.draw()
                win.flip()
                #print coordinates of starting position
                print(start_pos)
                #set counters to one so that this happens only for the first click
                i = 1
                j = 1
    
            #Update current mouse position every frame
            curr_pos = myMouse.getPos()
            #Take Betrag des Abstandes der Koordinaten to determine width and height of the current rectangle in this frame 
            width = abs(start_pos[0] - curr_pos[0])
            height = abs(start_pos[1] - curr_pos[1])
            #go from x-start to middle of the rectangle (i.e. position) relative to the value of pos_current in this frame
            position = [start_pos[0] + 0.5*(curr_pos[0] - start_pos[0]), start_pos[1] + 0.5*(curr_pos[1] - start_pos[1])]
            #update rectangle
            rect.setWidth(width)
            rect.setHeight(height)
            rect.setPos(position)
            image.draw()
            rect.draw()
            win.flip()
        
        #if left button is released, take end position (also only for one frame and not for every frame thereafter
        if j == 1:
            end_pos = curr_pos
            #and print it out
            print(end_pos)
            #wait for response: was that the part of the image the subject wanted to select?
            resp = event.waitKeys(keyList = ["y", "n"])
            #if confirmed, exit
            if resp == ["y"]:
                break
                #win.close()
                #core.quit()
            #if not, start over again (rectangle is then set to zero height and length in lines 43 and 44 to make the old one disappear)
            else:
                i = 0
                j = 0

    return start_pos, end_pos

stimList = ["test_image.jpg", "test_image2.jpg"]

for image in stimList:
    start, end = selection_rectangle(win, image)
    print(start, end)
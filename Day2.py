#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, gui, data
import os, random, sys
import pandas as pd
from Functions import draw_fixation, present_stimuli_day_2, feedback, present_instruction, selection_rectangle, take_break

#instructions
welcome_instruction = "Willkommen!"
selection_instruction = "Now the selection circle."
break_instruktion = "Mach eine kurze Pause! \nWenn du soweit bist, druecke Enter, um weiter zu machen. \nNach drei Minuten geht es automatisch weiter."
thank_you_instruction = "Thank you Instruction"

#selectio circle color
color = "red"

file_experiment = 'stimFile.csv' #.xlsx-File mit Infos(memorability etc.)
expFile = pd.read_csv(file_experiment)
path_images = "images/"

#display
dispsize = [800, 800]

#reminder positions (old/new, remember/knwo)
pos_new = [-320, -320]
pos_old = [320, -320]

#keys
key_new = 'lctrl'
key_old = 'rctrl'

#timing
fixation_time = 0.01
presentation_time = 0.01

rounds = len(expFile['filename'])

# Get the subject number from Day1
expName = 'day2'
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
subNum = expInfo['participant']

# relevant info in separate lists
filenames = list(expFile["filename"])
category = expFile['category']
sunfolder = expFile['SUNfolder']
num = expFile['num']
hit_rate = expFile['hitRate']
human = expFile['human']
animal = expFile['animal']
scene_cat = expFile['sceneCat']
is_odd = expFile['isOdd']
memo = expFile['memo']
set = expFile['set']

#Provide window
win = visual.Window(
    size=dispsize, #fullscr auf True ueberschreibt size
    units="pix",
    fullscr=False,
    color=[1, 1, 1]
)

##Preload Images
#Create empty image list to hold the stimuli
images = []
#list of filenames with path relative to this file
list_of_files = path_images + expFile["filename"]

#fill list "images"
for file in list_of_files: #create an image stimulus from each file, and store it in the list
    images.append(visual.ImageStim(win=win, image=file))

# bind filenames to image stimuli
dict_filenames = {}
for i in range(len(filenames)):
   dict_filenames.update({filenames[i]: images[i]})

# Make clear, which ones are distractors and which ones are targets
dict_is_target = {}
if (int(subNum) % 2 == 0):
    set_targets = 2
else:
    set_targets = 1

for i in range(len(filenames)):
    if set[i] == set_targets:
        dict_is_target.update({filenames[i]:1})
    else:
        dict_is_target.update({filenames[i]:0})

# randomize
all_info = zip(filenames, category, sunfolder, num, hit_rate, human, animal, scene_cat, is_odd, memo, set)
random.shuffle(all_info)
filenames, category, sunfolder, num, hit_rate, human, animal, scene_cat, is_odd, memo, set = zip(*all_info)

# Prepare reminder
reminder_1 = visual.TextStim(win, text="", pos=[0,0],
                            color="black",
                            font='Arial',
                            height=30,
                            wrapWidth=int(0.8 * dispsize[0])
                            )

reminder_2 = visual.TextStim(win, text="", pos=[0,0],
                            color="black",
                            font='Arial',
                            height=30,
                            wrapWidth=int(0.8 * dispsize[0])
                            )

## Prepare to save output
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

filename_output = _thisDir + os.sep + 'data' + os.sep + '%s_%s_' %(expInfo['participant'], expName)
outputFile = open(filename_output + 'out' + '.csv','w')
outputFile.write("subject,filename,category,sunfolder,num,hitRate,human,animal,scene_cat,is_odd,memo,set,isTarget,correct,rk, start_x, start_y, radius")
outputFile.write("\n")

#count if first time selection circle
k = 0
# Now the trials
present_instruction(win,dispsize,welcome_instruction)
for i in range (rounds):
    #if new image no selection rectangle is drawn
    start_pos = [0, 0]
    end_pos = [0, 0]
    pos = [0, 0]
    end_radius = 0

    draw_fixation(win, fixation_time)
    resp_on, resp_rk = present_stimuli_day_2(win, dict_filenames[filenames[i]], key_new, key_old, reminder_1, reminder_2, pos_new, pos_old, presentation_time)

    if resp_on[0] == key_old:
        if k == 0:
            present_instruction(win, dispsize, selection_instruction)
            k += 1
        try:
            start_pos, end_radius = selection_rectangle(win, dict_filenames[filenames[i]], color)
        except:
            start_pos, end_radius = selection_rectangle(win, dict_filenames[filenames[i]], color)

    if (resp_on[0] == key_old) & (dict_is_target[filenames[i]] == 1):
        feedback(win, dispsize, "Richtig!", "green", 1)
        is_correct = 1
    elif (resp_on[0] == key_new) & (dict_is_target[filenames[i]] == 0):
        feedback(win, dispsize, "Richtig!", "green", 1)
        is_correct = 1
    else:
        feedback(win, dispsize, "Falsch!", "red", 1)
        is_correct = 0

    if resp_rk[0] == key_new:
        rk = "remember"
    elif resp_rk[0] == key_old:
        rk = "know"

    if i in [int(1/3.0*rounds), int(2/3.0*rounds)]:
        take_break(win, dispsize, break_instruktion)

    outputFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(subNum, filenames[i], category[i], sunfolder[i], num[i], hit_rate[i], human[i], animal[i], scene_cat[i], is_odd[i], memo[i], set[i], dict_is_target[filenames[i]], is_correct, rk, start_pos[0], start_pos[1], end_radius))

present_instruction(win,dispsize,thank_you_instruction)

win.close()

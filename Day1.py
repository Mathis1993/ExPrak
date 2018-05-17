#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, event, core, gui, data
import os, random, csv
import pandas as pd
from Functions import draw_fixation, present_stimuli_day_1, feedback, present_instruction, reminder, take_break

#instructions
welcome_instruction = "Welcome Instruction"
thank_you_instruction = "Thank you Instruction"
continue_encoding_instruction = "Continue Encoding Instruction"
end_of_block_instruction = "Test at end of block instruction"
break_instruction = "Mach eine kurze Pause! \nWenn du soweit bist, druecke Enter, um weiter zu machen. \nNach drei Minuten geht es automatisch weiter!"

#Display
dispsize = [600, 600]

#positions
pos_new = [-270, -270]
pos_old = [270, -270]

#keys
key_new = 'lctrl'
key_old = 'rctrl'


file_experiment = 'stimFile.csv' #.xlsx-File mit Infos(memorability etc.)
expFile = pd.read_csv(file_experiment)
path_images = "images/" #image path relative to this file
file_distractors_day_1 = 'distractors_day_1.xlsx'
distrFile = pd.read_excel(file_distractors_day_1, sheetname="Tabelle1")
path_distractors_day_1 = "distractors_day_1/"
#block runs over all 400 images, but only 200 will be shown; iterator nonetheless counts up to 400
image_test = [59, 119]
#actual block size - 1 due to 0-based index
block_size = 99
#column in the output file containing info about whether an image was tested at the end of one block
col_tested = 16
#positions of the reminders for old and new key at the end of each block
#time interval of fixation cross and image presentation
fixation_time = 0.01
presentation_time = 0.01

# Store info about the experiment session
expName = 'day1'
expInfo = {'participant':'', 'session':'001', 'age':'', 'gender':'', 'nationality':'', 'occupation':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
subNum = expInfo['participant']
age = expInfo['age']
gender = expInfo['gender']
nation = expInfo['nationality']
occupation = expInfo['occupation']

## Prepare to save output
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data' + os.sep + '%s_%s_' %(expInfo['participant'], expName)
print(filename)

#Provide window
win = visual.Window(
    size=dispsize, #fullscr auf True ueberschreibt size
    units="pix",
    fullscr=False,
    color=[1, 1, 1]
)

#Images with set == 1 are targets for subjects with an uneven number, == 2 for subjects with an even number
if (int(subNum) % 2 == 0):
    expFile = expFile.loc[expFile['set']==2]
else:
    expFile = expFile.loc[expFile['set'] == 1]

rounds_experiment = len(expFile['filename'])

##Preload Images
#Create empty image list to hold the stimuli
images = []
#Variable to bind Filenames to stimuli
filenames = list(expFile["filename"])
#list of filenames with path relative to this file
list_of_files = path_images + expFile["filename"]

#fill list "images"
for file in list_of_files: #create an image stimulus from each file, and store it in the list
    images.append(visual.ImageStim(win=win, image=file))

# bind filenames to image stimuli
dict_filenames = {}
for i in range(len(filenames)):
   dict_filenames.update({filenames[i]: images[i]})

##Preload distractor images for test after each block
distractors = path_distractors_day_1 + distrFile['stimuli']
random.shuffle(distractors)
new_images = []
for file in distractors:
    new_images.append(visual.ImageStim(win=win, image=file))

##Shuffle stimuli and open output files in preparation of trials
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
all_info = zip(filenames, category, sunfolder, num, hit_rate, human, animal, scene_cat, is_odd, memo, set)
random.shuffle(all_info)
filenames, category, sunfolder, num, hit_rate, human, animal, scene_cat, is_odd, memo, set = zip(*all_info)
outputFile = open(filename + 'out' + '.csv','w')
outputFile.write("subject,age,gender,nation,occupation,filename,category,sunfolder,num,hitRate,human,animal,scene_cat,is_odd,memo,set,tested")
outputFile.write("\n")
outputFile_winner = open(filename + 'winner' + '.csv', 'w')
outputFile_winner.write("subject, correct")
outputFile_winner.write("\n")
count_distractors = 0

# 0 is written in every row at first, then overwritten with 1 for the images that were tested at the end of a block
tested = 0
tested_images = []
present_instruction(win,dispsize,welcome_instruction)

## This is a trial
# only 2 times so after the second time we dont need the continue encoding instruction
#k = 0
for i in range(0,rounds_experiment,1):
    draw_fixation(win, fixation_time)
    present_stimuli_day_1(win,dict_filenames[filenames[i]], presentation_time)

    '''
    #after each block of 100 images, test 2 images
    if i in image_test:
        #random.randint(i-99, i)
        #assign a random image from the last block
        index = random.randint(i-block_size,i)
        tested_images.append(index)
        #expFile.at[index,9] = expFile.at[index,9].replace(0,1)
        #print(expFile.at[index,9])
        old_image = dict_filenames[filenames[index]]
        new_image = new_images[count_distractors]
        count_distractors += 1
        test = [old_image, new_image]
        dict_is_target = {old_image:0, new_image:1}
        random.shuffle(test)
        present_instruction(win, dispsize, end_of_block_instruction)

        for j in range (2):
            draw_fixation(win, fixation_time)
            test[j].draw()
            reminder(win,dispsize,"new",pos_new)
            reminder(win,dispsize,"old",pos_old)
            win.flip()
            resp = event.waitKeys(keyList=[key_new, key_old])
            #resp is a list
            if (resp[0] == key_new) & (dict_is_target[test[j]] == 1):
                feedback(win,dispsize,"Richtig!","green", 1)
                is_correct = 1
            elif (resp[0] == key_old) & (dict_is_target[test[j]] == 0):
                feedback(win,dispsize,"Richtig!", "green", 1)
                is_correct = 1
            else:
                feedback(win,dispsize,"Falsch!", "red",1)
                is_correct = 0
            outputFile_winner.write("{},{}\n".format(subNum, is_correct))
        if k == 0:
            present_instruction(win, dispsize, continue_encoding_instruction)
        k += 1
        '''
    # break after half of the trials
    if i == rounds_experiment/2:
        take_break(win, dispsize, break_instruction)
    outputFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(subNum, age, gender, nation, occupation, filenames[i], category[i], sunfolder[i], num[i], hit_rate[i], human[i], animal[i], scene_cat[i], is_odd[i], memo[i], set[i], tested))

present_instruction(win,dispsize, thank_you_instruction)

win.close()

'''
## Mark the images that were tested at the end of each block
r = csv.reader(open(filename + 'out' + '.csv'))
lines = list(r)
# + 1 because the index on the list "tested_images" is without column names, but the output file contains these
for index in tested_images:
    lines[index+1][col_tested] = 1
#mode 'wb' to prevent empty columns being written
writer = csv.writer(open(filename + 'out' + '.csv', 'wb'))
writer.writerows(lines)
'''

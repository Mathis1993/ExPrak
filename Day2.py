from psychopy import visual, core, gui, data
import os, random, sys
import pandas as pd
from Functions import draw_fixation, present_stimuli_day_2, feedback, present_instruction, selection_rectangle

path_targets = "images/"
file_distractors_day_2 = 'distractors_day_2.xlsx'
distrFile = pd.read_excel(file_distractors_day_2, sheetname="Tabelle1")
path_distractors_day_2 = "distractors_day_2/"
dispsize = [600, 600]
pos_new = [-270, -270]
pos_old = [270, -270]
key_new = 'lctrl'
key_old = 'rctrl'
fixation_time = 0.01
presentation_time = 0.01
rounds = 220

# Get the subject number from Day1
expName = 'day2'
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
subNum = expInfo['participant']

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Access respective subject's outputfile from Day1
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data' + os.sep + '%s_%s_' %(expInfo['participant'], 'day1') + 'out' + '.csv'
# Test if file exists
if os.path.exists(filename) == False:
    sys.exit(filename + " does not exist!")

# Else read in data
expFile = pd.read_csv(filename)

# Select targets that were not tested at the end of a block on day1
stimuli = expFile["filename"]
wasTarget = expFile["isTarget"]
wasTested = expFile["tested"]
targets = []
for i in range (len(stimuli)):
    if (wasTarget[i] == 1) & (wasTested[i] == 0):
        targets.append(stimuli[i])

# Distractors
distractors = distrFile["stimuli"]

# Make clear, which ones are distractors and which ones are targets
dict_is_target = {}
for stimulus in targets:
    dict_is_target.update({stimulus:1})
for stimulus in distractors:
    dict_is_target.update({stimulus:0})

#Provide window
win = visual.Window(
    size=dispsize, #fullscr auf True ueberschreibt size
    units="pix",
    fullscr=False,
    color=[1, 1, 1]
)

# Preload Stimuli
#Create empty image list to hold the stimuli
images = []
#fill list "images" with targets
for file in targets: #create an image stimulus from each file, and store it in the list
    images.append(visual.ImageStim(win=win, image=path_targets + file))

#bind filenames to image stimuli
dict_filenames = {}
for i in range(len(targets)):
   dict_filenames.update({targets[i]: images[i]})

#and fill it with distractors
for file in distractors: #create an image stimulus from each file, and store it in the list
    images.append(visual.ImageStim(win=win, image=path_distractors_day_2 + file))

#bind filenames to image stimuli
for i in range(len(distractors)):
   dict_filenames.update({distractors[i]: images[i]})

# Targets and distractors on one list
stimuli = targets + list(distractors)

# randomize
random.shuffle(stimuli)

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


filename_output = _thisDir + os.sep + 'data' + os.sep + '%s_%s_' %(expInfo['participant'], expName)
outputFile = open(filename_output + 'out' + '.csv','w')
outputFile.write("subject,filename,isTarget,correct,rk, start_x, start_y, radius")
outputFile.write("\n")

# Now the trials
present_instruction(win, dispsize, "Instruction")
for i in range (rounds):
    #if new image no selection rectangle is drawn
    start_pos = [0, 0]
    end_pos = [0, 0]
    pos = [0, 0]

    draw_fixation(win, fixation_time)
    resp_on, resp_rk = present_stimuli_day_2(win, dict_filenames[stimuli[i]], key_new, key_old, reminder_1, reminder_2, pos_new, pos_old, presentation_time)

    if resp_on[0] == key_old:
        if i == 0:
            present_instruction(win, dispsize, "Now the selection rectangle.")
        start_pos, end_radius = selection_rectangle(win, dict_filenames[stimuli[i]])

    if (resp_on[0] == key_old) & (dict_is_target[stimuli[i]] == 1):
        feedback(win, dispsize, "Richtig!", "green", 1)
        is_correct = 1
    elif (resp_on[0] == key_new) & (dict_is_target[stimuli[i]] == 0):
        feedback(win, dispsize, "Richtig!", "green", 1)
        is_correct = 1
    else:
        feedback(win, dispsize, "Falsch!", "red", 1)
        is_correct = 0

    if resp_rk[0] == key_new:
        rk = "remember"
    elif resp_rk[0] == key_old:
        rk = "know"
    outputFile.write("{},{},{},{},{},{},{},{}\n".format(subNum, stimuli[i], dict_is_target[stimuli[i]], is_correct, rk, start_pos[0], start_pos[1], end_radius))

present_instruction(win,dispsize,"Thank you Instruction")

win.close()

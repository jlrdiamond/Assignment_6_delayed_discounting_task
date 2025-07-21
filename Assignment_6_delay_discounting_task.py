import pandas as pd 
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim, Rect, TextBox
from psychopy.core import Clock, quit, wait
from psychopy.event import Mouse
from psychopy.hardware.keyboard import Keyboard
from psychopy import event
import random

### DIALOG BOX ROUTINE ###
exp_info = {'participant_nr': '', 'age': '','condition':['future','past','present']} #DLG box input areas
dlg = DlgFromDict(exp_info)	#Initialize this instance of DlgFromDict() and assign it to variable, dig

# If pt pressed Cancel in dialogue box, quit
if not dlg.OK:
    quit()

# Initialize a fullscreen window with my monitor (HD format) size
# and my monitor specification called "samsung" from the monitor center
# Changed to fig mac monitor
win = Window(size=(1200, 800), fullscr=False, monitor='testMonitor', useRetina=True)

# Also initialize a mouse, although we're not going to use it
mouse = Mouse(visible=False)

# Initialize a (global) clock
clock = Clock()

# Initialize Keyboard
kb = Keyboard()
kb.clearEvents() #Clear any leftover keypresses from keyboard's memory buffer (so any keypresses (which have been recorded by Keyboard component) before start of experiment are not registered as response for the upcoming trial in the experiment. Only keys pressed after this point will now be recorded as trial response data. 

### START BODY OF EXPERIMENT ###
#
# This is where we'll add stuff from the second
# Coder tutorial.
#
### END BODY OF EXPERIMENT ###

### WELCOME ROUTINE ###
# Create a welcome screen and show for 2 seconds
welcome_txt_stim = TextStim(win, text="Welcome to this experiment!", color=(1, 0, -1), font='Calibri')	#PsychoPy color is RGB (255, 128, 0), orange
welcome_txt_stim.draw()
win.flip()
wait(2)

### INSTRUCTION ROUTINE ###
#Note, experiment includes real-life consequences, which is known to improve signal-to-noise ratio. 
instruct_txt = """ 
In this experiment, you will make choices between monetary amounts.

On each trial you will choose between whether you prefer an immediate amount
or an amount available after a delay.
    
One trial will be randomly selected and you will receive the amount you chose on that 
trial. If you selected a delayed amount, the money will be paid to you after the respective delay.

You can click the offer you prefer

(Press ‘enter’ to start the experiment!)
 """
     
# Show instructions and wait until response (return)
instruct_txt = TextStim(win, instruct_txt, alignText='left', height=0.085)
instruct_txt.draw()
win.flip()

# Initialize keyboard and wait for response
kb = Keyboard()
while True:
    keys = kb.getKeys()
    if 'return' in keys:
        # The for loop was optional
        for key in keys:
            print(f"The {key.name} key was pressed within {key.rt:.3f} seconds for a total of {key.duration:.3f} seconds.")
        break  # break out of the loop!
        

#Read in .csv files: with immediate vs. delay offer trials as rows, and intervention cues for an intervention group
offers = ['Offers_hw.csv']	
random.shuffle(offers)	#shuffle function in random module shuffles standard Python lists. here, rearrange elements (immediate vs. delay offers) in the offers list. output is shuffled list. 

cues=pd.read_csv('cues.csv')	#Intervention cues; note: not in GitHub, need to make
cue=cues.loc[0,'event']		#Locate 1st column which is titled "event" 

### TRIAL LOOP ROUTINE ###
offer_trial = pd.read_csv(offers[0])	#Read .csv file with path offers[0] (i.e., start with first item in offers list. assign this to a new dataframe, variable offer_trail
offer_trial = offer_trial.sample(frac=1)	#create new dataframe, offer_trial, with rows in random order

# Create fixation target (a plus sign)
fix_target = TextStim(win, '+')
trial_clock = Clock()

# START experinent clock
clock.reset()

# Show initial fixation
fix_target.draw()
win.flip()
wait(1)

#Create rectangles in experiment window for pt to chose between [likely by clicking on]
rec1= Rect(win=win, size=0.4, fillColor=[0, 1, 0], lineColor=[1, 0, 0],pos=(-0.5,0)) #rec1 is green with red outline, on L side of window
rec2 = Rect(win=win, size=0.4, fillColor=[0, 1, 0], lineColor=[1, 0, 0],pos=(0.5,0)) #rec2 is green with red outline, on R side of window
rec_select1= Rect(win=win, size=0.6, fillColor=None, lineColor=[1, 0, 0],lineWidth=10, pos=(-0.5,0)) 		#rectangle of no color with thick red outline [see below, likely appears around rec1 if that is the selected rectangle after pt makes selection]
rec_select2 = Rect(win=win, size=0.6, fillColor=None, lineColor=[1, 0, 0],lineWidth=10, pos=(0.5,0)) 		#rectangle of no color with thick red outline [see below, likely appears around rec1 if that is the selected rectangle after pt makes selection]

for idx, row in offer_trial.iterrows():	#Iterate through rows in offer_trial dataframe

    imm_off_amt = str(row['immediate_amount']) + " today"	#Initialize string and the word today and assign to variable imm_off
    del_off_amt = str(row['delayed_amount']) + " in " + str(row['delay']) + " days"		#Initialize string for monetary amount, word in, string in row delay with ant of days, word days and assign to variable del_off_amt

    n=random.randint(0, 1)	#Select a random integer of either 0 or 1 and assign it to variable n
    if n < 0.5:			#If value n <0.5, 
        stim_txt1 = TextStim(win, imm_off_amt, pos=(0.5, 0.0))	#Show imm_off (i.e., immediate reward option) slightly R of center of exp window
        stim_txt2 = TextStim(win, del_off_amt, pos=(-0.5, 0.0))	#Show del_off_amt (i.e., delay reward option) slightly L of center of exp window
    else:			#Otherwise (i.e., n≥0.5)
        stim_txt1 = TextStim(win, imm_off_amt, pos=(-0.5, 0.0))	#Show (i.e., immediate reward option) slightly L of center of exp window
        stim_txt2 = TextStim(win, del_off_amt, pos=(0.5, 0.0))	#Show del_off_amt (i.e., delay reward option) slightly R of center of exp window


    m=random.randint(0, 1)	##Select a random integer of either 0 or 1 and assign it to variable m
    if m == 0:	
        present=cue	#Assign cue variable, (from above, i.e., pd.read_csv('cues.csv')), to variable present
    else:
        present=""	#Assign empty string to variable, present
    cue_present=TextStim(win,present,pos=(0,0.5))
    offer_trial.loc[idx, 'cue shown'] = (m == 0) #HW: Record in offer_trial dataframe that cue was shown for the scenario where m == 0


	#Assign whichever text is presented to variable, cue_present; i.e., alternate whether cue or nothing is shown. *this is a within-group design!*
    
    offer_trial.loc[idx, 'onset'] = -1	#In offer_trial dataframe, create/locate cell by row and onset column and put value -1 in it

    trial_clock.reset()			#Start timer by resetting trial clock
    x=0					#Assign value 0 to variable x (set x equal to 0)
    click=0				#Assign value 0 to variable click (a mouse click)
    while trial_clock.getTime() < 4:	#While loop that runs continuously for 4 s 
        if click == 0:			#If click is 0 (it will always be because we set it to 0 before the loop)
            win.mouseVisible=True	#Make the mouse visible in the experiment window (will always be visible in this loop)
        rec1.draw()			#Draw the choice options into exp window
        rec2.draw()
        stim_txt1.draw()
        stim_txt2.draw()
        cue_present.draw()		#Draw the cue_present variable (where present either = cue or = "") into exp window
        win.flip()			#Flip all of that from back to front buffer so pt can see

        if mouse.isPressedIn(rec1):	#If pt clicks mouse in rec1 (choosing either imm_off_amt or del_off_amt, depending on value of n)
            if x == 0:			#If x is equal to 0, which is also a click
                rt=trial_clock.getTime()	#Record the time and assign to variable, rt
            x=1				#Set x equal to 1, which is not a click
            if n < 0.5 and click ==0:	#If n is <0.5 and click is equal to 0 (we set it =0 so it has to be)
                resp = "delayed"	#Assign string "delay" string to variable resp
                click = 1		#Set click equal to 1 (assign value 1 to variable click)
            else:			#Otherwise
                resp="immediate"	#Assign string "immediate" to variable resp
                click = 1		#Set click equal to 1 (assign value 1 to variable click)
            win.mouseVisible=False	#Make the mouse not visible in exp window
            rec1.draw()			#Draw the choice options into exp window
            rec2.draw()
            stim_txt1.draw()
            stim_txt2.draw()
            rec_select1.draw()
            cue_present.draw()		#Draw the cue_present variable (where present either = cue or = "") into exp window
            win.flip()			#Flip all of that from back to front buffer so pt can see
            
        if mouse.isPressedIn(rec2):	#If pt clicks mouse in rec 2 (choosing either imm_off_amt or del_off_amt, depending on value of n)
            if x == 0:			#If x equals 0 (this will return false, since we most recently set x=1)
                rt=trial_clock.getTime()	#Record the time and assign to variable rt
            x=1				#Set x equal to 1
            if n < 0.5 and click==0:	#If n <0.5 and click is equivalent to 0 (will return false, since we most recently set click equal to 1)
                resp = "immediate"	
                click=1			#Set click equal to 1
            else:
                resp="delayed"
                click=1			#Set click equal to 1
        ## make mouse not visible	
            win.mouseVisible=False
            rec1.draw()			#Draw the choice options into exp window
            rec2.draw()
            stim_txt1.draw()
            stim_txt2.draw()
            rec_select2.draw()
            cue_present.draw()		#Draw the cue_present variable (where present either = cue or = "") into exp window
            win.flip()			#Flip all of that from back to front buffer so pt can see
    else:
        mouse.visible=False		
        fix_target.draw()
        win.flip()
        wait(1)
    #Recording data in dataframe    
    if offer_trial.loc[idx, 'onset'] == -1:
        offer_trial.loc[idx, 'onset'] = clock.getTime()
        

    resp_kb = kb.getKeys()
    if resp_kb:

        if 'q' in resp_kb:
            quit()

    if x == 0:
        resp = "miss"
        rt = "miss"
        
    print(resp)				#Print pt responses
    offer_trial.loc[idx, 'rt'] = rt	#
    offer_trial.loc[idx, 'resp'] = resp	#

#HW: Calculate number of times pt chooses delayed option in the condition where future event cue is shown (i.e., for n ≥ 0.5 (i.e., resp="delayed") and m == 0)
offer_trial = offer_trial[(offer_trial['cue_shown'] == True) & 
    (offer_trial['resp'] == 'delayed')
]

#HW: Calculate number of times pt chooses delayed option in the condition where future event cue is not shown (i.e., if m == 0 is false)
offer_trial = offer_trial[(offer_trial['cue_shown'] == False) & 
    (offer_trial['resp'] == 'delayed')
]


#Save dataframe as csv file with pt number and no manipulation in title
offer_trial.to_csv(f"sub-{exp_info['participant_nr']}_results_no_manipulation.csv")


# Finish experiment (window and quit)
win.close()
quit() 	
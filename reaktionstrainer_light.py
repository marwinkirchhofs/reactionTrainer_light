
# light version of the reaction trainer
# just consists of a window with colour area and start/stop button


from tkinter import *
from threading import *
from time import sleep
from random import random
from math import floor


# colors used
colors=["red","green","blue","yellow"]
# variable and file to store waiting times
waitTimes={"low":1, "high":3}
f_waitTimes=".reactionTrainer_waitTimes.pkl"


# copied from https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()
        self._pause_event = Event()

    def start(self):
        if self.paused():
            self.resume()
        else:
            super(StoppableThread, self).start()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def pause(self):
        self._pause_event.set()

    def paused(self):
        return self._pause_event.is_set()

    def resume(self):
        self._pause_event.clear()


def fct_runColors(arg_label):

	sleepOffset = waitTimes["low"]
	sleepDuration = waitTimes["high"] - waitTimes["low"]

	# initial color 
	numColor = floor( len(colors)*random() )
	newColor = numColor
	arg_label.configure(bg=colors[numColor])
	print("new color = " + colors[numColor])
	timeSleep = sleepOffset + ( sleepDuration*random() )
	sleep(timeSleep)
	while True:
		# close thread if stop signal is set
		if current_thread().stopped():
			return 0
		elif not current_thread().paused():
			sleepOffset = waitTimes["low"]
			sleepDuration = waitTimes["high"] - waitTimes["low"]

			# compute next color (must not be current color)
			newColor = floor( len(colors)*random() )
			while newColor == numColor:
				newColor = floor( len(colors)*random() )
			numColor = newColor
			print("new color = " + colors[numColor])
			# set new color
			arg_label.configure(bg=colors[numColor])

			timeSleep = sleepOffset + (sleepDuration*random() )
			sleep(timeSleep)
			

def btCmd_start(event=0):
	print("start button clicked")
	

def btCmd_stop(event=0):
	print("stop button clicked")
	print("max: " + str_maxWait + ", min: " + str_minWait)

def updateWait(str_minWait, str_maxWait, f_waitTimes):
	print("min: " + str_minWait.get() + "max: " + str_maxWait.get())
	# update time values if valid
	try:
		minWaitTime = int(str_minWait.get())
		maxWaitTime = int(str_maxWait.get())
		if not maxWaitTime < minWaitTime:
			# update wait time values 
			waitTimes["low"] = minWaitTime
			waitTimes["high"] = maxWaitTime
			
			# store new wait time values
#			with open(f_waitTimes, "wb") as file_waitTimes:
#				pickle.dump(waitTimes, file_waitTimes, protocol=0)
	except:
		pass
	
 
################ PROGRAM START ################




####################
#### set up gui ####
####################

## create window
mainWindow = Tk()
mainWindow.title("reaction trainer light")

## create start and stop buttons
bt_start = Button(mainWindow, text="Start")
bt_stop = Button(mainWindow, text="Stop")
bt_quit = Button(mainWindow, text="Quit", command=mainWindow.quit)

## create empty label as colour area
label_colourArea = Label(mainWindow, text="", bg="red")

## labels and entry fields for wait values
# tkinter variables to store minWait and maxWait
str_minWait = StringVar(mainWindow)
str_maxWait = StringVar(mainWindow)
str_minWait.trace_add("write", lambda name, index, mode, str_minWait=str_minWait, str_maxWait=str_maxWait, f_waitTimes=f_waitTimes: updateWait(str_minWait, str_maxWait, f_waitTimes))
str_maxWait.trace_add("write", lambda name, index, mode, str_minWait=str_minWait, str_maxWait=str_maxWait, f_waitTimes=f_waitTimes: updateWait(str_minWait, str_maxWait, f_waitTimes))
# window components for wait times
label_waitTime = Label(mainWindow, text="Anzeigezeit:")
label_minWait = Label(mainWindow, text="min.")
label_maxWait = Label(mainWindow, text="max.")
entry_minWait = Entry(mainWindow, textvariable=str_minWait)
entry_minWait.insert(10, str_minWait.get())
entry_maxWait = Entry(mainWindow, textvariable=str_maxWait)
entry_maxWait.insert(10, str_maxWait.get())
scale_minWait = Scale(mainWindow, from_=0, to=10, orient=HORIZONTAL, showvalue=0, variable=str_minWait)
scale_maxWait = Scale(mainWindow, from_=0, to=10, orient=HORIZONTAL, showvalue=0,variable=str_maxWait)
# set initial values of minWait, maxWait variables (get passed to widgets automatically)
str_minWait.set("4")
str_maxWait.set("7")

## add components to mainWindow
label_colourArea.grid(row=0, column=0, sticky=W+E+N+S, columnspan=5)
label_waitTime.grid(row=1, column=0)
label_minWait.grid(row=1, column=1)
entry_minWait.grid(row=1, column=2)
label_maxWait.grid(row=1, column=3)
entry_maxWait.grid(row=1, column=4)
scale_minWait.grid(row=2, column=1, columnspan=2)
scale_maxWait.grid(row=2, column=3, columnspan=2)
bt_start.grid(row=3, column=0, columnspan=2)
bt_stop.grid(row=3, column=2, columnspan=2)
bt_quit.grid(row=3, column=4)

## set up row and column weights
mainWindow.grid_rowconfigure(0, weight=4)
mainWindow.grid_rowconfigure(1, weight=0)
mainWindow.grid_rowconfigure(2, weight=0)
mainWindow.grid_columnconfigure(0, weight=1)
mainWindow.grid_columnconfigure(1, weight=1)
mainWindow.grid_columnconfigure(2, weight=1)
mainWindow.grid_columnconfigure(4, weight=1)
mainWindow.grid_columnconfigure(3, weight=1)


##############################
#### set up functionality ####
##############################

# create thread which will be started and stopped by the respective buttons
thread_switchColors = StoppableThread(target=fct_runColors, args=(label_colourArea, ), daemon=True ) 


###############################
#### add gui functionality ####
################################

bt_start.configure(command=thread_switchColors.start)
bt_stop.configure(command=thread_switchColors.pause)

############################
#### "start" mainWindow ####
############################
mainWindow.mainloop()

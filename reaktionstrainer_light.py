
# light version of the reaction trainer
# just consists of a window with colour area and start/stop button


from tkinter import *
from threading import *
from time import sleep
from random import random
from math import floor


colors=["red","green","blue","yellow"]
sleepRange=(1,3)


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
	sleepOffset = sleepRange[0]
	sleepDuration = sleepRange[1] - sleepRange[0]

	# initial color 
	numColor = floor( 4*random() )
	newColor = numColor
	arg_label.configure(bg=colors[numColor])
	print("new color = " + colors[numColor])
	timeSleep = sleepOffset + floor( sleepDuration*random() )
	sleep(timeSleep)
	while True:
		# close thread if stop signal is set
		if current_thread().stopped():
			return 0
		elif not current_thread().paused():
			# compute next color (must not be current color)
			newColor = floor( 4*random() )
			while newColor == numColor:
				newColor = floor( 4*random() )
			numColor = newColor
			print("new color = " + colors[numColor])
			# set new color
			arg_label.configure(bg=colors[numColor])

			timeSleep = sleepOffset + floor( sleepDuration*random() )
			sleep(timeSleep)
			

def btCmd_start(event=0):
	print("start button clicked")
	

def btCmd_stop(event=0):
	print("stop button clicked")

 
################ PROGRAM START ################




####################
#### set up gui ####
####################

# create window
mainWindow = Tk()
mainWindow.title("reaction trainer light")

# create start and stop buttons
bt_start = Button(mainWindow, text="Start")
bt_stop = Button(mainWindow, text="Stop")
bt_quit = Button(mainWindow, text="Quit", command=mainWindow.quit)

# create empty label as colour area
label_colourArea = Label(mainWindow, text="", bg="red")

# add components to mainWindow
bt_start.grid(row=1, column=0)
bt_stop.grid(row=1, column=1)
bt_quit.grid(row=1, column=2)
label_colourArea.grid(row=0, column=0, sticky=W+E+N+S, columnspan=3)

# set up row and column weights
mainWindow.grid_rowconfigure(0, weight=4)
mainWindow.grid_rowconfigure(1, weight=0)
mainWindow.grid_columnconfigure(0, weight=1)
mainWindow.grid_columnconfigure(1, weight=1)
mainWindow.grid_columnconfigure(2, weight=1)


##############################
#### set up functionality ####
##############################

# create thread which will be started and stopped by the respective buttons
thread_switchColors = StoppableThread(target=fct_runColors, args=(label_colourArea, ) ) 


###############################
#### add gui functionality ####
################################

bt_start.configure(command=thread_switchColors.start)
bt_stop.configure(command=thread_switchColors.pause)

############################
#### "start" mainWindow ####
############################
mainWindow.mainloop()
#################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: 
#################################

# import the configs
from bomb_configs import *
# other imports
from tkinter import *
import tkinter
from threading import Thread
from time import sleep
import os
import sys
import random
#importing pillow for image resizing purposes
from PIL import ImageTk, Image
#create global variables to change clock
ADD = 0
SET = 0

#create global variable for media directory
MEDIA = "/home/spartans/LMB-CSC102-Final/media"

#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    #add the game phase parameter to the constructor
    def __init__(self, window, gamephase):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        #initialize the gamephase
        self._gamephase = gamephase
        # setup the initial "boot" GUI
        self.setupBoot()

    # sets up the LCD "boot" GUI
    def setupBoot(self):
        #access the global variable: media
        global MEDIA 
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        #destroy previous image label
        if hasattr(self, "_lebronImage"):
            self._lebronImage.destroy()
        #getting the image path based on current game phase (e.g. Cavs, Heat, etc.)
        if self._gamephase == "Cavs":
            image_path = os.path.join(MEDIA, "bronphotocavs.png")
        elif self._gamephase == "Heat":
            image_path = os.path.join(MEDIA, "bronphotoheat.png")
        elif self._gamephase == "Lakers":
            image_path = os.path.join(MEDIA, "bronphotolakers.png")
        elif self._gamephase == "Final":
            image_path = os.path.join(MEDIA, "akronohiophoto.png")
        else:
            image_path = os.path.join(MEDIA, "lebrontrophies1.png") 
        #opening the image
        image = Image.open(image_path)
        #resizing the image
        resized = image.resize((100, 100), Image.LANCZOS)
        #updating the opened image
        updated = ImageTk.PhotoImage(resized)
        #creating the label and gridding the image
        self._lebronImage = Label(self, image=updated, bg="black")
        self._lebronImage.image = updated
        self._lebronImage.grid(row=0, column=2)
        #packing
        self.pack(fill=BOTH, expand=True)

    # sets up the LCD GUI
    def setup(self):
        #special setup for final game phase
        if self._gamephase == "Final":
            #keypad label
            self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
            self._lkeypad.grid(row=3, column=0, columnspan=3, sticky=W)
            #timer label
            self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
            self._ltimer.grid(row=4, column=0, columnspan=3, sticky=W)
            #strikes label
            self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
            self._lstrikes.grid(row=4, column=1, sticky=W)
            #hint label
            self._lfinalhint = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Hint: ")
            self._lfinalhint.grid(row=2, column=0, columnspan=3, sticky=W)
            #current game phase
            self._lgamephase = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Game phase: {}".format(self._gamephase))
            self._lgamephase.grid(row=1, column=0, sticky=W)
            #showbuttons
            if (SHOW_BUTTONS):
                # the pause button (pauses the timer)
                self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause", anchor=CENTER, command=self.pause)
                self._bpause.grid(row=6, column=0, pady=40)
                # the quit button
                self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
                self._bquit.grid(row=6, column=2, pady=40)
        #all other phases
        else:
            # the timer
            self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
            self._ltimer.grid(row=4, column=0, columnspan=3, sticky=W)
            # the keypad passphrase
            self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
            self._lkeypad.grid(row=3, column=1, columnspan=3, sticky=W)
            # the jumper wires status
            self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
            self._lwires.grid(row=2, column=1, columnspan=3, sticky=W)
            # the pushbutton status
            self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
            self._lbutton.grid(row=3, column=0, columnspan=3, sticky=W)
            # the toggle switches status
            self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Toggles phase: ")
            self._ltoggles.grid(row=2, column=0, columnspan=2, sticky=W)
            # the strikes left
            self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
            self._lstrikes.grid(row=4, column=1, sticky=W)
            #current game phase
            self._lgamephase = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Game phase: {}".format(self._gamephase))
            self._lgamephase.grid(row=1, column=0, sticky=W)
            #hint label
            self._lfinalhint = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Hint: ")
            self._lfinalhint.grid(row=1, column=1, columnspan=3, sticky=W)
            #showbuttons
            if (SHOW_BUTTONS):
                # the pause button (pauses the timer)
                self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause", anchor=CENTER, command=self.pause)
                self._bpause.grid(row=6, column=0, pady=40)
                # the quit button
                self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
                self._bquit.grid(row=6, column=2, pady=40)

    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    #mimic the conclusion method but for concluding each game phase
    def gamephaseconclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        #destroy the game phase label
        self._lgamephase.destroy()
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()

        # reconfigure the GUI
        #add a label to state the game phase is complete and that the next phase is starting
        #special message for final phase
        if self._gamephase == "Lakers":
            self._lcompletedMessage = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text=f"{self._gamephase} phase complete! Final phase starting...")
        else:
            self._lcompletedMessage = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text=f"{self._gamephase} phase complete! Next phase starting...")
        #grid the message label
        self._lcompletedMessage.grid(row=1, column=1, sticky=W)

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        #destroy the game phase label
        self._lgamephase.destroy()
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()
        
        #if bomb is defused, show a success message
        if success:
            self._lcompletedMessage = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Bomb defused! You win!")
            self._lcompletedMessage.grid(row=1, column=1, sticky=W)
        #else show a failure message
        else:
            self._lfailedMessage = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Bomb exploded! You lose!")
            self._lfailedMessage.grid(row=1, column=1, sticky=W)

        # reconfigure the GUI
        # the retry button
        self._bretry = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Retry", anchor=CENTER, command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        # the quit button
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)

    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        # re-launch the program (and exit this one)
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # exit the application
        exit(0)

# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False

# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, gamephase, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        if gamephase == "Cavs":
            self._value = initial_value
        elif gamephase == "Heat":
            self._value = initial_value-60
        elif gamephase == "Lakers":
            self._value = initial_value-120
        elif gamephase == "Final":
            self._value = 90
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            #call global variables
            global ADD, SET
            if (not self._paused):
                #if global set changed it sets timer value to global set then changes global set back to 0
                if SET != 0:
                    self._value = SET
                    SET = 0
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value == 0):
                    self._running = False
                #adds ADD and sets to 0 after
                #if ADD = 0 nothing happens anyways, so only changes timer value when global set is changed.
                self._value += ADD
                self._value -= 1
                ADD = 0
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)
    
    
    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

# the keypad phase
class Keypad(PhaseThread):
    def __init__(self, component, gamephase, target, name="Keypad"):
        super().__init__(name, component, target)
        # the default value is an empty string
        self._value = ""
        #need to check the genKeypadCombo in bomb_configs later
        if gamephase == "Cavs":
            self._target = "2009"
        elif gamephase == "Heat":
            self._target = "2014"
        elif gamephase == "Lakers":
            self._target = "2020"
        elif gamephase == "Final":
            self._target = "1111"

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # process keys when keypad key(s) are pressed
            if (self._component.pressed_keys):
                # debounce
                while (self._component.pressed_keys):
                    try:
                        # just grab the first key pressed if more than one were pressed
                        key = self._component.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                if key == "#":
                    self._value = self._value[:-1]
                else:
                    self._value += str(key)
                # the combination is correct -> phase defused
                if (self._value[-1] == "*"):
                    self._value = self._value[:-1]
                    if (self._value == self._target):
                        self._defused = True
                    # the combination is incorrect -> phase failed (strike)
                    elif (self._value != self._target):
                        self._failed = True
            sleep(0.1)

    # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return self._value

# the jumper wires phase
class Wires(PhaseThread):
    #set the target equal to the correct combination
    def __init__(self, component, gamephase, target, name="Wires"):
        super().__init__(name, component, target)
        #set the value of the wires to an empty string
        self._value = ""
        #setting new targets based on the gamephase
        if gamephase == "Cavs":
            self._target = "10010"
        elif gamephase == "Heat":
            self._target = "00010"
        elif gamephase == "Lakers":
            self._target = "10100"

    # runs the thread
    def run(self):
        #set the phase running to True
        self._running = True
        #main loop for the phase
        while (self._running):
            # get the jumper wire states (0->False, 1->True)
            self._value = "".join([str(int(pin.value)) for pin in self._component]) 
            #check if the value of the wires is equal to the target
            if (self._value == self._target):
                #the phase is defused
                self._defused = True
                
            sleep(0.1)

    # returns the jumper wires state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
           #return the value of the wires as a string
           return f"{self._value}"

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, gamephase, target, colors, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        #set gamephase
        self._gamephase = gamephase
        # the pushbutton's randomly selected LED color
        #0 = red
        #1 = green
        #2 = blue
        self._cList = colors
        self._color = self._cList[0]
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer

    # runs the thread
    def run(self):
        i = 0
        count = 0
        wasGreen = False
        self._running = True
        # set the RGB LED color
        while (self._running):
            self._rgb[2].value = True
            self._rgb[1].value = True
            self._rgb[0].value = True
            # get the pushbutton's state
            #red
            if i == 0:
                self._rgb[0].value = False #if self._color == "R" else True
                self._color = "R"
                wasGreen = False
            #green
            if i == 1:
                self._rgb[1].value = False #if self._color == "G" else True
                self._color = "G"
                wasGreen = True
            #blue
            if i == 2:
                self._rgb[2].value = False #if self._color == "B" else True
                self._color = "B"
                wasGreen = False
            self._value = self._component.value
            # it is pressed
            if (self._value):
                # note it
                self._pressed = True
            # it is released
            else:
                # was it previously pressed?
                if (self._pressed):
                    # check the release parameters
                    # for R, nothing else is needed
                    # for G or B, a specific digit must be in the timer (sec) when released
                    #             if (not self._target or self._target in self._timer._sec):
                    if wasGreen:
                        self._defused = True
                        #REMEMBER TO CHANGE BACK TO TRUE
                    else:
                        self._failed = True
                    # note that the pushbutton was released
                    self._pressed = False
            #randomly pick color
            rand = random.randint(0, 100)
            if rand >= 99:
                i = 1
            elif rand <=5:
                i = 2
            else:
                i = 0
            #count will go up every 0.1 seconds
            #time for first phase
            if self._gamephase == "Cavs":
                if wasGreen and count<8:
                    count+=1
                    i = 1
                else:
                    count = 0
            #time for second phase
            if self._gamephase == "Heat":
                if wasGreen and count<6:
                    count+=1
                    i = 1
                else:
                    count = 0
            #time for third phase
            if self._gamephase == "Lakers":
                if wasGreen and count<4:
                    count+=1
                    i = 1
                else:
                    count = 0
            sleep(0.1)

    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")

# the toggle switches phase
class Toggles(PhaseThread):
    def __init__(self, component, gamephase, target, name="Toggles"):
        super().__init__(name, component, target)
        self._value = ""
        #setting targets depending on phase (cavs, heat, lakers) for parlay puzzle
        if gamephase == "Cavs":
            self._target = "0111"
        elif gamephase == "Heat":
            self._target = "0011"
        elif gamephase == "Lakers":
            self._target = "1101"
        
    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # get the toggle switch values (0->False, 1->True)
            self._value = "".join([str(int(pin.value)) for pin in self._component])
            #call global variables
            global ADD, SET
            
            #checks if self._value and self._target are the same, defusing the toggles phase
            if (self._value == self._target):
                self._defused = True        
            sleep(0.1)
            
    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return f"{self._value}"

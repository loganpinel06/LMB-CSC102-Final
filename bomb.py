#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: 
#################################

# import the configs
from bomb_configs import *
# import the phases
from bomb_phases import *

###########
# functions
###########
# generates the bootup sequence on the LCD
#def bootup(n=0):
#    # if we're not animating (or we're at the end of the bootup text)
#    if (not ANIMATE or n == len(boot_text)):
#        # if we're not animating, render the entire text at once (and don't process \x00)
#        if (not ANIMATE):
#            gui._lscroll["text"] = boot_text.replace("\x00", "")
#        # configure the remaining GUI widgets
#        gui.setup()
#        # setup the phase threads, execute them, and check their statuses
#        if (RPi):
#            setup_phases()
#            check_phases()
#    # if we're animating
#    else:
#        # add the next character (but don't render \x00 since it specifies a longer pause)
#        if (boot_text[n] != "\x00"):
#            gui._lscroll["text"] += boot_text[n]
#
#        # scroll the next character after a slight delay (\x00 is a longer delay)
#        gui.after(25 if boot_text[n] != "\x00" else 750, bootup, n + 1)
#
## sets up the phase threads
#def setup_phases():
#    global timer, keypad, wires, button, toggles
#    
#    # setup the timer thread
#    timer = Timer(component_7seg, COUNTDOWN)
#    # bind the 7-segment display to the LCD GUI so that it can be paused/unpaused from the GUI
#    gui.setTimer(timer)
#    # setup the keypad thread
#    keypad = Keypad(component_keypad, keypad_target)
#    # setup the jumper wires thread
#    wires = Wires(component_wires, wires_target)
#    # setup the pushbutton thread
#    button = Button(component_button_state, component_button_RGB, button_target, button_color, timer)
#    # bind the pushbutton to the LCD GUI so that its LED can be turned off when we quit
#    gui.setButton(button)
#    # setup the toggle switches thread
#    toggles = Toggles(component_toggles, toggles_target)
#
#    # start the phase threads
#    timer.start()
#    keypad.start()
#    wires.start()
#    button.start()
#    toggles.start()
#
## checks the phase threads
#def check_phases():
#    global active_phases
#    
#    # check the timer
#    if (timer._running):
#        # update the GUI
#        gui._ltimer["text"] = f"Time left: {timer}"
#    else:
#        # the countdown has expired -> explode!
#        # turn off the bomb and render the conclusion GUI
#        turn_off()
#        gui.after(100, gui.conclusion, False)
#        # don't check any more phases
#        return
#    # check the keypad
#    if (keypad._running):
#        # update the GUI
#        gui._lkeypad["text"] = f"Combination: {keypad}"
#        # the phase is defused -> stop the thread
#        if (keypad._defused):
#            keypad._running = False
#            active_phases -= 1
#        # the phase has failed -> strike
#        elif (keypad._failed):
#            strike()
#            # reset the keypad
#            keypad._failed = False
#            keypad._value = ""
#    # check the wires
#    if (wires._running):
#        # update the GUI
#        gui._lwires["text"] = f"Wires: {wires}"
#        # the phase is defused -> stop the thread
#        if (wires._defused):
#            wires._running = False
#            active_phases -= 1
#        # the phase has failed -> strike
#        elif (wires._failed):
#            strike()
#            # reset the wires
#            wires._failed = False
#    # check the button
#    if (button._running):
#        # update the GUI
#        gui._lbutton["text"] = f"Button: {button}"
#        # the phase is defused -> stop the thread
#        if (button._defused):
#            button._running = False
#            active_phases -= 1
#        # the phase has failed -> strike
#        elif (button._failed):
#            strike()
#            # reset the button
#            button._failed = False
#    # check the toggles
#    if (toggles._running):
#        # update the GUI
#        gui._ltoggles["text"] = f"Toggles: {toggles}"
#        # the phase is defused -> stop the thread
#        if (toggles._defused):
#            toggles._running = False
#            active_phases -= 1
#        # the phase has failed -> strike
#        elif (toggles._failed):
#            strike()
#            # reset the toggles
#            toggles._failed = False
#
#    # note the strikes on the GUI
#    gui._lstrikes["text"] = f"Strikes left: {strikes_left}"
#    # too many strikes -> explode!
#    if (strikes_left == 0):
#        # turn off the bomb and render the conclusion GUI
#        turn_off()
#        gui.after(1000, gui.conclusion, False)
#        # stop checking phases
#        return
#
#    # the bomb has been successfully defused!
#    if (active_phases == 0):
#        # turn off the bomb and render the conclusion GUI
#        turn_off()
#        gui.after(100, gui.conclusion, True)
#        # stop checking phases
#        return
#
#    # check the phases again after a slight delay
#    gui.after(100, check_phases)
#
## handles a strike
#def strike():
#    global strikes_left
#    
#    # note the strike
#    strikes_left -= 1
#
## turns off the bomb
#def turn_off():
#    # stop all threads
#    timer._running = False
#    keypad._running = False
#    wires._running = False
#    button._running = False
#    toggles._running = False
#
#    # turn off the 7-segment display
#    component_7seg.blink_rate = 0
#    component_7seg.fill(0)
#    # turn off the pushbutton's LED
#    for pin in button._rgb:
#        pin.value = True
#
#######
## MAIN
#######
#
## initialize the LCD GUI
#window = Tk()
##pass the color phase parameter to the Lcd class
#gui = Lcd(window, COLORPHASES)
#
## initialize the bomb strikes and active phases (i.e., not yet defused)
#strikes_left = NUM_STRIKES
#active_phases = NUM_PHASES
#
## "boot" the bomb
#gui.after(1000, bootup)
#
## display the LCD GUI
#window.mainloop()

#create a class for the BombPhases
#this will act as a parent class to run all bomb phases but will allow us to do this three times
#for each color phase
class BombPhase:
    #constructor passing in the colorphase and the gui element
    def __init__(self, colorphase, gui):
        #initialize instance variables
        self._colorphase = colorphase
        self._gui = gui
        self._timer = None
        self._keypad = None
        self._wires = None
        self._button = None
        self._toggles = None
        self._active_phases = NUM_PHASES
        self._strikes_left = NUM_STRIKES

    #method to setup the phases
    def setup_phases(self):
        #setup the timer thread
        self._timer = Timer(component_7seg, COUNTDOWN)
        #bind the 7-segment display to the LCD GUI so that it can be paused/unpaused from the GUI
        self._gui.setTimer(self._timer)
        #setup the keypad thread
        self._keypad = Keypad(component_keypad, keypad_target)
        #setup the jumper wires thread
        self._wires = Wires(component_wires, wires_target)
        #setup the pushbutton thread
        self._button = Button(component_button_state, component_button_RGB, button_target, button_color, self._timer)
        #bind the pushbutton to the LCD GUI so that its LED can be turned off when we quit
        self._gui.setButton(self._button)
        #setup the toggle switches thread
        self._toggles = Toggles(component_toggles, toggles_target)

        #start the phase threads
        self._timer.start()
        self._keypad.start()
        self._wires.start()
        self._button.start()
        self._toggles.start()

    #method to check the phases
    def check_phases(self):
        # check the timer
        if (self._timer._running):
            # update the GUI
            #might not need to update the colorphase but here if needed
            #self._gui._lcolorphase["text"] = f"Color Phase: {self._colorphase}"
            self._gui._ltimer["text"] = f"Time left: {self._timer}"
        else:
            # the countdown has expired -> explode!
            # turn off the bomb and render the conclusion GUI
            self.turn_off()
            self._gui.after(100, self._gui.conclusion, False)
            # don't check any more phases
            return
        # check the keypad
        if (self._keypad._running):
            # update the GUI
            self._gui._lkeypad["text"] = f"Combination: {self._keypad}"
            # the phase is defused -> stop the thread
            if (self._keypad._defused):
                self._keypad._running = False
                self._active_phases -= 1
            # the phase has failed -> strike
            elif (self._keypad._failed):
                self.strike()
                # reset the keypad
                self._keypad._failed = False
                self._keypad._value = ""
        # check the wires
        if (self._wires._running):
            # update the GUI
            self._gui._lwires["text"] = f"Wires: {self._wires}"
            # the phase is defused -> stop the thread
            if (self._wires._defused):
                self._wires._running = False
                self._active_phases -= 1
            # the phase has failed -> strike
            elif (self._wires._failed):
                self.strike()
                # reset the wires
                self._wires._failed = False
        # check the button
        if (self._button._running):
            # update the GUI
            self._gui._lbutton["text"] = f"Button: {self._button}"
            # the phase is defused -> stop the thread
            if (self._button._defused):
                self._button._running = False
                self._active_phases -= 1
            # the phase has failed -> strike
            elif (self._button._failed):
                self.strike()
                # reset the button
                self._button._failed = False
        # check the toggles
        if (self._toggles._running):
            # update the GUI
            self._gui._ltoggles["text"] = f"Toggles: {self._toggles}"
            # the phase is defused -> stop the thread
            if (self._toggles._defused):
                self._toggles._running = False
                self._active_phases -= 1
            # the phase has failed -> strike
            elif (self._toggles._failed):
                self.strike()
                # reset the toggles
                self._toggles._failed = False
    
        # note the strikes on the GUI
        self._gui._lstrikes["text"] = f"Strikes left: {self._strikes_left}"
        # too many strikes -> explode!
        if (self._strikes_left == 0):
            # turn off the bomb and render the conclusion GUI
            self.turn_off()
            self._gui.after(1000, self._gui.conclusion, False)
            # stop checking phases
            return
    
        # the bomb has been successfully defused!
        if (self._active_phases == 0):
            # turn off the bomb and render the conclusion GUI
            self.turn_off()
            self._gui.after(100, self._gui.conclusion, True)
            # stop checking phases
            return
    
        # check the phases again after a slight delay
        self._gui.after(100, self.check_phases)

    #method to setup strikes
    def strike(self):
        #note the strike
        self._strikes_left -= 1

    #method to setup turn off
    def turn_off(self):
        #stop all threads
        self._timer._running = False
        self._keypad._running = False
        self._wires._running = False
        self._button._running = False
        self._toggles._running = False

        #turn off the 7-segment display
        component_7seg.blink_rate = 0
        component_7seg.fill(0)
        #turn off the pushbutton's LED
        for pin in self._button._rgb:
            pin.value = True

#main method
#bootup method
def bootup(phase, n=0):
    # if we're not animating (or we're at the end of the bootup text)
    if (not ANIMATE or n == len(boot_text)):
        # if we're not animating, render the entire text at once (and don't process \x00)
        if (not ANIMATE):
            phase._gui._lscroll["text"] = boot_text.replace("\x00", "")
        # configure the remaining GUI widgets
        phase._gui.setup()
        # setup the phase threads, execute them, and check their statuses
        if (RPi):
            phase.setup_phases()
            phase.check_phases()
    # if we're animating
    else:
        # add the next character (but don't render \x00 since it specifies a longer pause)
        if (boot_text[n] != "\x00"):
            phase._gui._lscroll["text"] += boot_text[n]

        # scroll the next character after a slight delay (\x00 is a longer delay)
        phase._gui.after(25 if boot_text[n] != "\x00" else 750, bootup, phase, n + 1)


window = Tk()

red_phase=BombPhase("red", Lcd(window, "red"))
green_phase=BombPhase("green", Lcd(window, "green"))

# initialize the bomb strikes and active phases (i.e., not yet defused)
strikes_left = NUM_STRIKES
active_phases = NUM_PHASES

# "boot" the bomb
window.after(1000, bootup, green_phase)

# display the LCD GUI
window.mainloop()
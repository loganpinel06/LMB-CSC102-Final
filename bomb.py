#################################
#CSC 102 Defuse the Bomb Project
#Main program
#Team: 
#################################

#import the configs
from bomb_configs import *
#import the phases
from bomb_phases import *

#create a class for the BombPhases
#this will act as a parent class to run all bomb phases but will allow us to do this three times
#for each game phase
class BombPhase:
    #constructor passing in the gamephase and the gui element
    def __init__(self, gamephase, gui):
        #initialize instance variables for the main bomb
        self._gamephase = gamephase
        self._gui = gui
        self._timer = None
        self._keypad = None
        self._wires = None
        self._button = None
        self._toggles = None
        self._active_phases = NUM_PHASES
        self._strikes_left = NUM_STRIKES

        #SETUP TEXT VARIABLES FOR EACH PHASE FOR BOOTUP
        #CAVS PHASE
        if self._gamephase == "Cavs":
            #set the toggles hint text
            togglesText = "1"
            wiresText = "1"
            buttonText = "1"
            keypadText = "1"
        elif self._gamephase == "Heat":
            #set the toggles hint text
            togglesText = "2"
            wiresText = "2"
            buttonText = "2"
            keypadText = "2"
        elif self._gamephase == "Lakers":
            #set the toggles hint text
            togglesText = "3"
            wiresText = "3"
            buttonText = "3"
            keypadText = "3"
        #setup the bootup text in bomb.py so we can use the gampphase variable to change the hints throughout the game
        self._boot_text = f"Booting LEBOMB...\n\x00\x00"\
                        f"Lebron is the GOAT\n"\
                        f"Initializing subsystems...\n\x00"\
                        f"Toggles: {togglesText}\n"\
                        f"Wires: {wiresText}\n"\
                        f"Button: {buttonText}\n\x00"\
                        f"Keypad: {keypadText}\n"\
                        f"Rendering phases...\x00"

    #method to setup the phases
    def setup_phases(self):
        #setup the timer thread
        self._timer = Timer(component_7seg, COUNTDOWN)
        #bind the 7-segment display to the LCD GUI so that it can be paused/unpaused from the GUI
        self._gui.setTimer(self._timer)
        #setup the keypad thread
        self._keypad = Keypad(component_keypad, keypad_target)
        #setup the jumper wires thread
        self._wires = Wires(component_wires, self._gamephase, wires_target)
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
        #check the timer
        if (self._timer._running):
            #update the GUI
            self._gui._ltimer["text"] = f"Time left: {self._timer}"
        else:
            #the countdown has expired -> explode!
            #turn off the bomb and render the conclusion GUI
            self.turn_off()
            self._gui.after(100, self._gui.conclusion, False)
            #don't check any more phases
            return
        #check the keypad
        if (self._keypad._running):
            #update the GUI
            self._gui._lkeypad["text"] = f"Combination: {self._keypad}"
            #the phase is defused -> stop the thread
            if (self._keypad._defused):
                self._keypad._running = False
                self._active_phases -= 1
            #the phase has failed -> strike
            elif (self._keypad._failed):
                self.strike()
                #reset the keypad
                self._keypad._failed = False
                self._keypad._value = ""
        #check the wires
        if (self._wires._running):
            #update the GUI
            self._gui._lwires["text"] = f"Wires: {self._wires}"
            #the phase is defused -> stop the thread
            if (self._wires._defused):
                self._wires._running = False
                self._active_phases -= 1
            #the phase has failed -> strike
            elif (self._wires._failed):
                self.strike()
                #reset the wires
                self._wires._failed = False
        #check the button
        if (self._button._running):
            #update the GUI
            self._gui._lbutton["text"] = f"Button: {self._button}"
            #the phase is defused -> stop the thread
            if (self._button._defused):
                self._button._running = False
                self._active_phases -= 1
            #the phase has failed -> strike
            elif (self._button._failed):
                self.strike()
                #reset the button
                self._button._failed = False
        #check the toggles
        if (self._toggles._running):
            #update the GUI
            self._gui._ltoggles["text"] = f"Toggles: {self._toggles}"
            #the phase is defused -> stop the thread
            if (self._toggles._defused):
                self._toggles._running = False
                self._active_phases -= 1
            #the phase has failed -> strike
            elif (self._toggles._failed):
                self.strike()
                #reset the toggles
                self._toggles._failed = False
    
        #note the strikes on the GUI
        self._gui._lstrikes["text"] = f"Strikes left: {self._strikes_left}"
        #too many strikes -> explode!
        if (self._strikes_left == 0):
            #turn off the bomb and render the conclusion GUI
            self.turn_off()
            self._gui.after(1000, self._gui.conclusion, False)
            #stop checking phases
            return
    
        #the bomb has been successfully defused!
        #bomb will only fully shut off after the lakers game phase
        if (self._active_phases == 0 and self._gamephase == "Lakers"):
            #turn off the bomb and render the conclusion GUI
            self.turn_off()
            self._gui.after(100, self._gui.conclusion, True)
            #stop checking phases
            return
        
        #game phase has been successfully defused!
        if (self._active_phases == 0 and self._gamephase != "Lakers"):
            #start the next game phase
            start_next_phase(self)
            #stop checking phases
            return
    
        #check the phases again after a slight delay
        self._gui.after(100, self.check_phases)

    #method to setup strikes
    def strike(self):
        #note the strike
        self._strikes_left -= 1

    #method to setup turn off
    #this will also be used to stop a phase when changing the game phases
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
    #if we're not animating (or we're at the end of the bootup text)
    if (not ANIMATE or n == len(phase._boot_text)):
        #if we're not animating, render the entire text at once (and don't process \x00)
        if (not ANIMATE):
            phase._gui._lscroll["text"] = phase._boot_text.replace("\x00", "")
        #configure the remaining GUI widgets
        phase._gui.setup()
        #setup the phase threads, execute them, and check their statuses
        if (RPi):
            phase.setup_phases()
            phase.check_phases()
    #if we're animating
    else:
        #add the next character (but don't render \x00 since it specifies a longer pause)
        if (phase._boot_text[n] != "\x00"):
            phase._gui._lscroll["text"] += phase._boot_text[n]

        #scroll the next character after a slight delay (\x00 is a longer delay)
        phase._gui.after(25 if phase._boot_text[n] != "\x00" else 750, bootup, phase, n + 1)

#method to start the next game phase
def start_next_phase(current_phase):
    #stop the current phase
    current_phase.turn_off()
    #conclude the current game phase
    current_phase._gui.after(100, current_phase._gui.gamephaseconclusion, True)
    #destroy the LCD GUI after 5 seconds
    current_phase._gui.after(5000, current_phase._gui.destroy)
    
    #start the next game phase
    if (current_phase == cavs_phase):
        #bootup the heat phase
        window.after(5000, bootup, heat_phase)
    elif (current_phase == heat_phase):
        #bootup the lakers phase
        window.after(5000, bootup, lakers_phase)

#initialize the LCD GUI
window = Tk()

#create objects of the BombPhase class for each game phase
cavs_phase=BombPhase("Cavs", Lcd(window, "Cavs"))
heat_phase=BombPhase("Heat", Lcd(window, "Heat"))
lakers_phase=BombPhase("Lakers", Lcd(window, "Lakers"))

#initialize the bomb strikes and active phases (i.e., not yet defused)
strikes_left = NUM_STRIKES
active_phases = NUM_PHASES

# Ensure the GUI is properly initialized before setting fullscreen
window.update_idletasks() #update the tasks so we can force the window to be fullscreen
window.attributes("-fullscreen", True)

#"boot" the bomb
window.after(1000, bootup, cavs_phase)

#display the LCD GUI
window.mainloop()
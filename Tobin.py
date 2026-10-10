import tkinter as tk
from tkinter import messagebox

vTitle = "Tobin's Spirit Guide"

# EMF Level 5
# Freezing Temps
# Spirit Box
# Ghost Writing
# Ghost Orbs
# Fingerprints
# DOTS Projector
dTobin = {
    'Goryo' : ['EMF Level 5','Fingerprints','DOTS Projector','Strength: A Goryo will usually only show itself on camera if there are no people nearby.\nWeakness: They are rarely seen far from their place of death.'],
    'Myling' : ['EMF Level 5','Fingerprints','Ghost Writing','Strength: Known to be quieter when hunting,\nWeakness: More frequently make paranormal sounds.'],
    'Hantu' : ['Fingerprints','Ghost Orbs','Freezing Temps','Strength: Lower temperatures can cause the Hantu to move at faster speeds\nWeakness: A Hantu will move slower in warm areas.'],
    'Yokai' : ['Spirit Box','Ghost Orbs','DOTS Projector','Strength: Talking near a Yokai will anger it and increase it\'s chance of attacking.\nWeakness: When hunting, a Yokai can only hear voices close to it.'],
    'Spirit' : ['EMF Level 5','Spirit Box','Ghost Writing','Weakness: Smudge Sticks will stop it from attacking for a long time period of time.'],
    'Wraith' : ['EMF Level 5','Spirit Box','DOTS Projector','Strength: Can\'t be tracked by footseps.\nWeakness: Toxic reaction to salt.'],
    'Phantom' : ['Spirit Box','Fingerprints','DOTS Projector','Strength: Sanity drops considerably when looking at a Phantom.\nWeakness: Taking a photo of a Phantom will make it temporarily disappear.'],
    'Poltereist' : ['Spirit Box','Fingerprints','Ghost Writing','Strength: Throws a huge amount of objects at once.\nWeakness: Ineffective in an empty room.'],
    'Banshee' : ['Fingerprints','Ghost Orbs','DOTS Projector','Strength: Only targets one person at a time.\nWeakness: Fear the Crucifix and are less aggressive near one.'],
    'Jinn' : ['EMF Level 5','Fingerprints','Freezing Temps','Strength: Travels at a faster speed if a victim is far away.\nWeakness: Turning off a power source will prevent the Jinn from using it\'s ability.'],
    'Mare' : ['Spirit Box','Ghost Orbs','Ghost Writing','Strength: Increased chance to attack in the dark.\nWeakness: Turning the lights on lowers it\'s chance to attack.'],
    'Revenant' : ['Ghost Orbs','Ghost Writing','Freezing Temps','Strength: Travels significantly faster when hunting a victim.\nWeakness: Hiding from a Revenant causes it to move very slowly.'],
    'Shade' : ['EMF Level 5','Ghost Writing','Freezing Temps','Strength: Shy, making it diificult to locate.\nWeakness: Will not enter hunting mode with multiple people nearby.'],
    'Demon' : ['Fingerprints','Ghost Writing','Freezing Temps','Strength: Attacks more often than any other ghost.\nWeakness: Asking a Demon successful Ouija board questions won\'t lower your sanity.'],
    'Yurei' : ['Ghost Orbs','Freezing Temps','DOTS Projector','Strength: Have a stronger effect on your sanity.\nWeakness: Using Smudge Sticks on a Yurei\'s room will prevent it from wandering for a long time.'],
    'Oni' : ['EMF Level 5','Freezing Temps','DOTS Projector','Strength: Can move objects and are more active with people nearby.\nWeakness: Is easy to find and identify due to being very active.']
}

dTracking = {}
for i in dTobin.keys():
    dTracking.update({i: [0, 0, dTobin[i][0], dTobin[i][1], dTobin[i][2]]})

dSliderTRK = {}
dSlider = []
dsclWGTTRKR = []
ddspWGTTRKR = []
dtmrWGTTRKR = []
vsec = int
vEvidence = []
for key, value in dTobin.items():
    if len(value[1]) < 20:
        vEvidence.append(value[0])
        vEvidence.append(value[1])
        vEvidence.append(value[2])
vEvidenceL = []
for i in vEvidence:
    if i not in vEvidenceL:
        vEvidenceL.append(i)
vEvidenceL = sorted(vEvidenceL)

def resetSliders():
    global dSlider
    dSlider = []
    enhancedSlider()
    enhancedDisplay()

def wgtdestry(dvar):
    for i in dvar:
        i.destroy()
        i.forget()
    dvar.clear()

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds) 
      
if __name__ == '__main__':

    window = tk.Tk()

    def countdowninit2():
        global vsec, vsecp
        vsec = 60*2
        vsecp = 0
        countdown()

    def countdowninit5():
        global vsec, vsecp
        vsec = 60*5
        vsecp = 0
        countdown()
    
    def countdownstop():
        global vsec, vsecp
        vsec = 0
        vsecp = -1

    def countdown(): 
        global vsec, vsecp
        wgtdestry(dtmrWGTTRKR)
        if vsec >= 0:
            ltimer = tk.Label(fTimer, text=convert(vsec), bg='black', fg='cyan', anchor='center', font=('Bold',18))
            ltimer.grid(row=1, column=2)
            vsec -= 1
            if vsec >= 0:
                window.after(1000, countdown)
        if vsecp >= 0 and  vsec == -1:
            ltimer = tk.Label(fTimer, text=convert(vsecp), bg='black', fg='red', anchor='center', font=('Bold',18))
            ltimer.grid(row=1, column=2)
            vsecp += 1
            if vsecp >= 0:
                window.after(1000, countdown)
        dtmrWGTTRKR.append(ltimer)

    def enhancedSlider():
        wgtdestry(dsclWGTTRKR)
        vwdth = 20 #Default 15
        vlngth = 200 #Default 100
        vslwdth = 75 # Default 30

        vrn = 1
        for i in vEvidenceL:
            levd = tk.Label(fSlider, text=i, bg='black', fg='white')
            levd.grid(row=vrn, column=1)
            scEv = tk.Scale(fSlider, from_=-1, to=1, orient=tk.HORIZONTAL, showvalue=0, bg='black', width=vwdth, length=vlngth, sliderlength=vslwdth)
            scEv.grid(row=vrn, column=2)
            scEv.set(0)
            dSlider.append(scEv)
            dsclWGTTRKR.append(levd)
            dsclWGTTRKR.append(scEv)
            vrn += 1

    def enhancedDisplay():
        wgtdestry(ddspWGTTRKR)
        ln = 0
        for i in dSlider:
                b = i.get()
                dSliderTRK.update({vEvidenceL[ln]: b})
                ln += 1

        for key, value in dTracking.items():
            dTracking[key][0] = 0
            dTracking[key][1] = 0
            for i in value:
                if i in dSliderTRK:
                    if dSliderTRK[i] == 1:
                        dTracking[key][0] += 1
                    if dSliderTRK[i] == -1:
                        dTracking[key][1] += 1

        vlnGhstWdth = 9
        vlnE1Wdth = 10
        vlnE2Wdth = 12
        vlnE3Wdth = 15
        vdrow = 1

        for i in dTobin:
            bhg = 'white'
            fge1 = 'white'
            fge2 = 'white'
            fge3 = 'white'
            hlc = 'green2'
            if dTracking[i][0] == 3:
                bhg = 'green2'
            if dTracking[i][0] == 2:
                bhg = 'orange'
                if dSliderTRK[dTobin[i][0]] == 0:
                    fge1 = hlc
                if dSliderTRK[dTobin[i][1]] == 0:
                    fge2 = hlc
                if dSliderTRK[dTobin[i][2]] == 0:
                    fge3 = hlc
            if dTracking[i][0] == 1:
                bhg = 'yellow'
            if dTracking[i][1] >= 1:
                bhg = 'grey12'
                fge1 = 'grey12'
                fge2 = 'grey12'
                fge3 = 'grey12'

            lnGhst = tk.Button(fDisplay, text=i, width=vlnGhstWdth, bg=bhg, command=lambda i=i: tk.messagebox.showwarning(title=vTitle +': ' + i, message=dTobin[i][3]))
            lnGhst.grid(row=vdrow, column=1)
            lnGhstE1 = tk.Label(fDisplay, bg='black', fg=fge1, text=dTobin[i][0], width=vlnE1Wdth)
            lnGhstE1.grid(row=vdrow, column=2)
            lnGhstE2 = tk.Label(fDisplay, bg='black', fg=fge2, text=dTobin[i][1], width=vlnE2Wdth)
            lnGhstE2.grid(row=vdrow, column=3)
            lnGhstE3 = tk.Label(fDisplay, bg='black', fg=fge3, text=dTobin[i][2], width=vlnE3Wdth)
            lnGhstE3.grid(row=vdrow, column=4)
            ddspWGTTRKR.append(lnGhst)
            ddspWGTTRKR.append(lnGhstE1)
            ddspWGTTRKR.append(lnGhstE2)
            ddspWGTTRKR.append(lnGhstE3)
            vdrow += 1

    window.title(vTitle)

    # HEADER FRAME
    fhdr = tk.Frame(window, bg='black')
    hdrTitle = tk.Label(fhdr, text=vTitle, bg='black', fg='white', anchor='center', font=('Bold',18))
    hdrTitle.grid(column=1, row=1)
    fhdr.grid_columnconfigure(1,weight=1)
    fhdr.grid_rowconfigure(1,weight=1)

    # DYNAMIC SLIDER FRAME
    fSlider = tk.Frame(window, bg='black')
    fSlider.grid_columnconfigure(1,weight=1)
    fSlider.grid_columnconfigure(2,weight=1)
    vfsr = 1
    for i in vEvidenceL:
        fSlider.grid_rowconfigure(vfsr,weight=1)
        vfsr += 1

    # DISPLAY FRAME
    fDisplay = tk.Frame(window, bg='black')
    fDisplay.grid_columnconfigure(2,weight=1)
    fDisplay.grid_columnconfigure(3,weight=1)
    fDisplay.grid_columnconfigure(4,weight=1)
    vrr = 1
    for i in dTobin:
        fDisplay.grid_rowconfigure(vrr,weight=1)
        vrr += 1

    # TIMER FRAME
    fTimer = tk.Frame(window, bg='black')
    fTimer.grid_rowconfigure(1,weight=1)
    fTimer.grid_columnconfigure(2,weight=1)

    # EVIDENCE DELTA FRAME
    fevdncdlta = tk.Frame(window, bg='black')

    # BUTTON FRAME
    fbtn = tk.Frame(window, bg='black')
    btn_quit = tk.Button(fbtn, text='Quit', command=window.quit)
    btn_quit.grid(column=1, row=1)
    btn_updt = tk.Button(fbtn, text='Reset', command=resetSliders)
    btn_updt.grid(column=3, row=1)
    btn_updt = tk.Button(fbtn, text='2 Min', command=countdowninit2)
    btn_updt.grid(column=4, row=1)
    btn_updt = tk.Button(fbtn, text='5 Min', command=countdowninit5)
    btn_updt.grid(column=5, row=1)
    btn_updt = tk.Button(fbtn, text='Stop', command=countdownstop)
    btn_updt.grid(column=6, row=1)
    btn_dispupdt = tk.Button(fbtn, text='Update Evidence', command=enhancedDisplay)
    btn_dispupdt.grid(column=7, row=1)
    fbtn.grid_rowconfigure(1,weight=1)
    for i in range(1, 8): 
        fbtn.grid_columnconfigure(i,weight=1)

    # PACK FRAMES
    fhdr.pack(fill='both', expand='yes')
    fSlider.pack(fill='both', expand='yes')
    fbtn.pack(fill='both', expand='yes')
    fevdncdlta.pack(fill='both', expand='yes')
    fDisplay.pack(fill='both', expand='yes')
    fTimer.pack(fill='both', expand='yes')

    enhancedSlider()
    enhancedDisplay()
    window.mainloop()


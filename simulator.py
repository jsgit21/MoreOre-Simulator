import time
import math
import random
from tkinter import *
from tkinter.ttk import Progressbar
from asyncio.windows_events import NULL
from tkinter import font
from tkinter.font import BOLD
from tkinter.ttk import Style

from bossData import *
import colors

# Used for abbreviated number conversions, order is important
# Adding more to the array will allow for more conversions
# https://idlechampions.fandom.com/wiki/Large_number_abbreviations
numAbbreviation = {
    '': None,
    'K':'Thousand',
    'M':'Million',
    'B':'Billion',
    't':'Trillion',
    'q':'Quadrillion',
    'Q':'Quintillion',
    's':'Sextillion',
    'S':'Septillion',
    }
numAbbreviationArray = list(numAbbreviation.keys())

def convertAbbrevNum(num):
    if num == '':
        return False

    # 300M, abbrev = M numPortion = 300
    abbrev = num[len(num)-1]
    numPortion = num[:len(num)-1]
    if abbrev.isdigit():
        abbrev = ''
        numPortion = num

    # A single decimal point will be replaced so that valid floats will pass isdigit
    if numPortion.replace('.','',1).isdigit() and abbrev in numAbbreviationArray:
        magnitude = numAbbreviationArray.index(abbrev)
        return float(numPortion) * (1000 ** magnitude)
    else:
        return False

# Format number to abbreviated form
def formatNum(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), numAbbreviationArray[magnitude])


statNames = {
    'HP':'HP',
    'ARM':'Armor',
    'LUK':'Luck',
    'ATK':'Attack',
    'DEX':'Dexterity',
    'APS':'Attacks/s',
    'SPD':'Speed',
    'STR':'Strength',
    'AGI':'Agility',
}

window = Tk()

winx = 735
winy = 600
window.geometry('{}x{}'.format(winx, winy))
window.title('More Ore Combat Simulator')

playerStatFields = {
    'ATK':{'value':None, 'statLabel':NULL, 'statEntry':NULL, 'row':0, 'column':0},
    'ARM':{'value':None, 'statLabel':NULL, 'statEntry':NULL, 'row':1, 'column':0},
    'HP':{'value':None, 'statLabel':NULL, 'statEntry':NULL, 'HPLabel':NULL, 'row':2, 'column':0},
    'SPD':{'value':None, 'statLabel':NULL, 'statEntry':NULL, 'row':3, 'column':0},
    'AGI':{'value':None, 'statLabel':NULL, 'statEntry':NULL, 'row':0, 'column':1},
    'DEX':{'value':None, 'statLabel':NULL, 'statEntry':NULL, 'row':1, 'column':1},
    'LUK':{'value':None, 'statLabel':NULL, 'statEntry':NULL, 'row':2, 'column':1},
    'STR':{'value':None, 'statLabel':NULL, 'statEntry':NULL, 'row':3, 'column':1},
}

def setMainHP(dataField, value):
    dataField['HP']['HPLabel'].config(text=value)

# Bound to statEntry Entries
def setStatsData(event, dataField, statGiven):
    userInput = event.widget.get()

    # Reset stat value and field label if user clears data
    if userInput == '':
        dataField[statGiven]['value'] = NULL
        dataField[statGiven]['statLabel'].config(foreground='black')
        if statGiven == 'HP':
            setMainHP(dataField, '--')
        return

    userInputValue = convertAbbrevNum(userInput)

    if userInputValue == False:
        dataField[statGiven]['statLabel'].config(foreground='red')
        dataField[statGiven]['value'] = NULL
        if statGiven == 'HP':
            setMainHP(dataField, 'ERR')
    else:
        dataField[statGiven]['statLabel'].config(foreground='green')
        dataField[statGiven]['value'] = userInputValue
        dataField[statGiven]['statEntry'].delete(0, 'end')
        dataField[statGiven]['statEntry'].insert(0, formatNum(userInputValue))
        if statGiven == 'HP':
            setMainHP(dataField, formatNum(userInputValue))

    # for stat, fieldData in dataField.items():
    #     print('{} - {}'.format(stat, fieldData))

abbrevFrame = Frame() #------------------------------------------------------------ Abbrev Key Frame START
abbrevFrame.grid(row=0,column=0,padx=10,pady=20,sticky=N)
abbrevTitle = Label(master=abbrevFrame, pady=12, text='Abbreviations are\n case sensitive', font=('Arial',9))
abbrevTitle.grid(row=0,column=0,sticky=W)

for index in range(1,9):
    abbrev = numAbbreviationArray[index]
    abbrevDef = numAbbreviation[abbrev]
    Label(master=abbrevFrame, text='{} = {}'.format(abbrev, abbrevDef)).grid(row=index, column=0)

#------------------------------------------------------------------------------------ Abbrev Key Frame END

playerStats = Frame() #------------------------------------------------------------ playerStats Frame START
playerStats.grid(row=0,column=1,padx=10)

playerStatsLabel = Label(master=playerStats, text='PLAYER STATS', font=('Arial',10))
playerStatsLabel.pack(pady=(16,24))

playerStatsInnerFrame = Frame(master=playerStats)
playerStatsInnerFrame.pack()

for stat, fieldData in playerStatFields.items():
    playerFrame = Frame(master=playerStatsInnerFrame)
    playerLabel = Label(master=playerFrame, text=statNames[stat], font=('Arial',9,BOLD))
    fieldData['statLabel'] = playerLabel
    playerLabel.pack()
    playerEntry = Entry(master=playerFrame, justify=CENTER)
    playerEntry.bind('<Return>', lambda event, dataField = playerStatFields, statGiven = stat: setStatsData(event, dataField, statGiven))
    playerEntry.bind('<FocusOut>', lambda event, dataField = playerStatFields, statGiven = stat: setStatsData(event, dataField, statGiven))
    fieldData['statEntry'] = playerEntry
    playerEntry.pack()
    playerFrame.grid(row=fieldData['row'], column=fieldData['column'], padx=10)

#------------------------------------------------------------------------------------ playerStats Frame END

bossStatFields = {
    'HP':{'value':None, 'statEntry':NULL, 'statLabel':NULL, 'HPLabel':NULL,  'row':0, 'column':0},
    'ARM':{'value':None, 'statEntry':NULL, 'statLabel':NULL,  'row':1, 'column':0},
    'LUK':{'value':None, 'statEntry':NULL, 'statLabel':NULL,  'row':2, 'column':0},
    'ATK':{'value':None, 'statEntry':NULL, 'statLabel':NULL,  'row':0, 'column':1},
    'DEX':{'value':None, 'statEntry':NULL, 'statLabel':NULL,  'row':1, 'column':1},
    'APS':{'value':None, 'statEntry':NULL, 'statLabel':NULL,  'row':2, 'column':1},
}

def setBossData(boss):

    for stat, fieldData in bossStatFields.items():
        if boss != 'CUSTOM':
            bossData = getBossInfo(boss)
            statShowValue = formatNum(bossData[stat])
            fieldData['value'] = bossData[stat]
            fieldData['statEntry'].config(state=NORMAL)
            fieldData['statEntry'].delete(0, 'end')
            fieldData['statEntry'].insert(0, statShowValue)
            fieldData['statLabel'].config(foreground='green')
            fieldData['statEntry'].config(state=DISABLED)
            if stat == 'HP':
                fieldData['HPLabel'].config(text=statShowValue)
        else:
            fieldData['statEntry'].config(state=NORMAL)
    

bossStats = Frame() #---------------------------------------------------------------- bossStats Frame START
bossStats.grid(row=0, column=2,padx=10)

bossStatsLabel = Label(master=bossStats, text='BOSS STATS', font=('Arial',10))
bossStatsLabel.pack(pady=(18,22))

bossStatsInnerFrame = Frame(master=bossStats)
bossStatsInnerFrame.pack(pady=(0,10))
 
#Create and store fields for boss stats
for stat, fieldData in bossStatFields.items():
    bossFrame = Frame(master=bossStatsInnerFrame)
    bossLabel = Label(master=bossFrame, text=statNames[stat], font=('Arial',9,BOLD))
    fieldData['statLabel'] = bossLabel
    bossLabel.pack()
    bossEntry = Entry(master=bossFrame, justify=CENTER)
    bossEntry.bind('<Return>', lambda event, dataField = bossStatFields, statGiven = stat: setStatsData(event, dataField, statGiven))
    bossEntry.bind('<FocusOut>', lambda event, dataField = bossStatFields, statGiven = stat: setStatsData(event, dataField, statGiven))
    fieldData['statEntry'] = bossEntry
    bossEntry.pack()
    bossFrame.grid(row=fieldData['row'], column=fieldData['column'], padx=10)

selected = StringVar()
selected.set('Choose Boss')
options = allBossNames()
bossDropdown = OptionMenu(bossStats, selected, *options, command=setBossData)
bossDropdown.config(width=20)
bossDropdown.pack()

#-------------------------------------------------------------------------------------- bossStats Frame END

PLAYER_LIFE = NULL
BOSS_LIFE = NULL
CLICK_DAMAGE = NULL
playerCombatAfterID = None
bossCombatAfterID = None

def moveAttackButton():
    rndx = random.randint(200,620)
    rndy = random.randint(380,410)
    manualAttack.place(x=rndx,y=rndy)


def click():
    global BOSS_LIFE
    BOSS_LIFE -= CLICK_DAMAGE
    bossHP.config(text= formatNum(int(BOSS_LIFE)))
    bossProgressBar['value'] = BOSS_LIFE
    moveAttackButton()

def calcClickDamage(pATK, pSTR, pLUK):
    global CLICK_DAMAGE

    damage = pATK + ((pATK * pSTR) / 6)
    clickMulti = 1 #artifacts change
    critChance = min((pLUK / 4 / 100), 1)
    critMulti = 1.5 
    for i, button in critButtons.items():
        if button['clicked']:
            critMulti += button['value']
    print('CritMulti:',critMulti)

    CLICK_DAMAGE = max(
        (damage * clickMulti * critChance * critMulti), 
        ((damage * clickMulti) + (damage * critChance * critMulti))
    )

def battleEnded():
    if PLAYER_LIFE == 0 or BOSS_LIFE == 0:
        return True
    else:
        return False

def dealPlayerDamage(pAPS, damage, hitChance):
    if battleEnded():
        return

    global BOSS_LIFE
    global playerCombatAfterID
    print('Player Damage:',damage)

    rndHitChance = random.random()
    if rndHitChance <= hitChance:
        #print('HIT random:',rndHitChance,'hitchance:',hitChance)
        BOSS_LIFE -= damage

        if BOSS_LIFE <= 0:
            BOSS_LIFE = 0

        bossHP.config(text=formatNum(int(BOSS_LIFE)))
        bossProgressBar['value'] = BOSS_LIFE
    else:
        print('MISS random:',rndHitChance,'hitchance:',hitChance)

    playerCombatAfterID = bossHP.after(int(1000/pAPS), dealPlayerDamage, pAPS, damage, hitChance)

def dealBossDamage(bAPS, damage, playerDodgeChance):
    if battleEnded():
        return

    global bossCombatAfterID
    global PLAYER_LIFE

    # Boss hitChance is player's dodge chance
    rndDodgeChance = random.random()
    if rndDodgeChance > playerDodgeChance:
        PLAYER_LIFE -= damage

        if PLAYER_LIFE <= 0:
            PLAYER_LIFE = 0

        playerHP.config(text=formatNum(int(PLAYER_LIFE)))
        playerProgressBar['value'] = PLAYER_LIFE
    else:
        print('PLAYER DODGED')
    bossCombatAfterID = playerHP.after(int(1000/bAPS), dealBossDamage, bAPS, damage, playerDodgeChance)

def playerValue(stat):
    return playerStatFields[stat]['value']

def bossValue(stat):
    return bossStatFields[stat]['value']

def startCombat():
    global PLAYER_LIFE 
    global BOSS_LIFE

    PLAYER_LIFE = playerValue('HP')
    playerProgressBar.config(maximum= PLAYER_LIFE, value=PLAYER_LIFE)

    BOSS_LIFE = bossValue('HP')
    bossProgressBar.config(maximum= BOSS_LIFE, value=BOSS_LIFE)

    print('player life',PLAYER_LIFE)
    print('boss life',BOSS_LIFE)

    pATK = playerValue('ATK')
    pLUK = playerValue('LUK')
    pSTR = playerValue('STR')
    calcClickDamage(pATK, pSTR, pLUK) # damage for manual click

    pAPS = (1 + (1 * playerValue('AGI') * 0.004)) # Player Attacks per second
    pDMG = pATK + ((pATK * pSTR) / 6) # Raw Player damage
    pDMG -= (bossValue('ARM') * 0.1) # Player damage against boss armor
    pDMG = max(pDMG, 0) # Prevents Player damage from being negative if caused to be negative due to boss armor
    pHIT = min(max((100 - (bossValue('LUK') + 1)/(playerValue('DEX') + 1))/100, 0.1),1) # Player hit chance

    bAPS = bossValue('APS') # Boss Attacks per second
    bDMG = bossValue('ATK') - (playerValue('ARM') * 0.1) # Boss damage
    bDMG = max(bDMG, 0) # Prevents Boss damage from being negative if caused to be negative due to player armor
    pDDG = min((pLUK + 1)/(bossValue('DEX') + 1)/100, 0.9) # Player dodge chance
    #print('Boss DPS: ', bDMG * (1-pDDG) * bAPS)

    dealPlayerDamage(pAPS, pDMG, pHIT)
    dealBossDamage(bAPS, bDMG, pDDG)

    combatButton.config(state=DISABLED, bg=colors.btnGrey)
    stopCombatButton.config(state=NORMAL, bg=colors.btnRed)

def setEntryStates(status):
    currentBoss = selected.get()
    if currentBoss == 'CUSTOM':
        for stat, data in bossStatFields.items():
            data['statEntry'].config(state=status)
    for stat, data in playerStatFields.items():
        data['statEntry'].config(state=status)

def initiateCombat():
    missingData = []
    for stat, data in playerStatFields.items():
        if data['value'] is None:
            missingData.append('Player {}'.format(statNames[stat]))
    for stat, data in bossStatFields.items():
        if data['value'] is None:
            missingData.append('Boss {}'.format(statNames[stat]))
    
    if len(missingData) > 0:
        print(missingData)
        return

    manualAttack.place(x = random.randint(200,620), y = random.randint(380,410))
    setEntryStates(DISABLED)
    startCombat()

def stopCombat():
    if bossCombatAfterID and playerCombatAfterID:
        playerHP.after_cancel(bossCombatAfterID)
        bossHP.after_cancel(playerCombatAfterID)
        setEntryStates(NORMAL)
        combatButton.config(state=NORMAL, bg=colors.btnGreen)
        stopCombatButton.config(state=DISABLED, bg=colors.btnGrey)
        manualAttack.place_forget()

playerHP = 1000
playerFrame = Frame()
labelPlayer = Label(master=playerFrame, text='Player')
playerHP = Label(master=playerFrame, text='--', font=('Ariel', 30, BOLD))
playerStatFields['HP']['HPLabel'] = playerHP

style = Style()
style.theme_use('alt')
style.configure("red.Horizontal.TProgressbar",
            foreground='red', background='red')

playerProgressBar = Progressbar(
    master=playerFrame,
    style="red.Horizontal.TProgressbar",
    orient = HORIZONTAL,
    length = 260,
    mode = 'determinate',
)
playerProgressBar['value'] = 100
playerProgressBar.pack()

labelPlayer.pack()
playerHP.pack()

bossFrame = Frame()
labelBoss = Label(master=bossFrame, text='Boss')
bossHP = Label(master=bossFrame, text='--', font=('Ariel', 30, BOLD))
bossStatFields['HP']['HPLabel'] = bossHP

style = Style()
style.theme_use('alt')
style.configure("red.Horizontal.TProgressbar",
            foreground='red', background='red')

bossProgressBar = Progressbar(
    master=bossFrame,
    style="red.Horizontal.TProgressbar",
    orient = HORIZONTAL,
    length = 260,
    maximum = 100,
    mode = 'determinate'
)
bossProgressBar['value'] = 100
bossProgressBar.pack()

labelBoss.pack()
bossHP.pack()

playerFrame.grid(row=1,column=1,padx=20,pady=20)
bossFrame.grid(row=1,column=2,padx=20,pady=20)

manualAttackFrame = Frame(height=70) # used for padding space for manual attack sword
manualAttackFrame.grid(row=3, column=0)
sword = PhotoImage(file = ".\\Media\\Resources\\combatSword.png")
manualAttack = Button(window, image=sword, command=click, relief=FLAT)


btnFrame = Frame()
combatButton = Button(btnFrame, text='Start Combat', command=initiateCombat, bg=colors.btnGreen, activebackground=colors.btnActiveGreen)
combatButton.grid(row=0, column=0)

stopCombatButton = Button(btnFrame, text='Stop Combat', command=stopCombat, state=DISABLED, bg=colors.btnGrey, activebackground=colors.btnActiveRed)
stopCombatButton.grid(row=1, column=0, pady=10)
btnFrame.grid(row=1, column=0)

researchFrame = Frame()
researchFrame.grid(row=4, column=0, columnspan=2, sticky=W, padx=12)
buffsFrame = Frame(master=researchFrame)
buffsFrame.grid(row=1, column=0, sticky=W)
researchTitle = Label(master=researchFrame, text='RESEARCH', font=('Arial',10))
researchTitle.grid(row=0)

def toggle(x, btnDict):
    button = btnDict[x]
    if button['clicked']:
        button['btn'].config(bg=colors.btnGrey, activebackground=colors.btnGrey)
        button['clicked'] = False
    else:
        button['btn'].config(bg=colors.btnActiveGreen, activebackground=colors.btnActiveGreen)
        button['clicked'] = True

critButtons = {} # 0:{'img': <img>, 'btn': <btn-object>, 'clicked': <bool>, 'value': <int>}
for i in range(0,3):
    critButtons[i] = {'img':None, 'btn': None, 'clicked':False, 'value':0.5}
    if i == 2:
        # Crit 1: 0.5, Crit 2: 0.5, Crit 3: 1
        critButtons[i]['value'] = 1
    critButtons[i]['img'] = PhotoImage(file = ".\\Media\\Resources\\crit{}.png".format(i+1))
    critBtn = Button(buffsFrame, image=critButtons[i]['img'], command=lambda x=i, btnDict=critButtons: toggle(x, btnDict), relief=FLAT, bg=colors.btnGrey)
    critBtn.grid(row=0, column=i, padx=4, pady=2)
    critButtons[i]['btn'] = critBtn

ravButtons = {}
for i in range(0,3):
    ravButtons[i] = {'img': None, 'btn': None, 'clicked': False, 'value': i+1}
    ravButtons[i]['img'] = PhotoImage(file = ".\\Media\\Resources\\rav{}.png".format(i+1))
    ravBtn = Button(buffsFrame, image = ravButtons[i]['img'], command=lambda x=i, btnDict=ravButtons: toggle(x, btnDict), relief=FLAT, bg=colors.btnGrey)
    ravBtn.grid(row=1, column=i, padx=4, pady=2)
    ravButtons[i]['btn'] = ravBtn

window.mainloop()
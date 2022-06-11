import math
from tkinter import *
from asyncio.windows_events import NULL
from tkinter import font
from tkinter.font import BOLD
from dataSet import getBossInfo, allBossNames

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
print(numAbbreviationArray)

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

playerLife = 10000
bossLife = 5000

def click():
    global bossLife
    bossLife -= 100
    bossHP.config(text=bossLife)


window = Tk()

winx = 735
winy = 420
window.geometry('{}x{}'.format(winx, winy))

playerStatFields = {
    'ATK':{'value':NULL, 'statLabel':NULL, 'statEntry':NULL, 'row':0, 'column':0},
    'ARM':{'value':NULL, 'statLabel':NULL, 'statEntry':NULL, 'row':1, 'column':0},
    'HP':{'value':NULL, 'statLabel':NULL, 'statEntry':NULL, 'row':2, 'column':0},
    'SPD':{'value':NULL, 'statLabel':NULL, 'statEntry':NULL, 'row':3, 'column':0},
    'AGI':{'value':NULL, 'statLabel':NULL, 'statEntry':NULL, 'row':0, 'column':1},
    'DEX':{'value':NULL, 'statLabel':NULL, 'statEntry':NULL, 'row':1, 'column':1},
    'LUK':{'value':NULL, 'statLabel':NULL, 'statEntry':NULL, 'row':2, 'column':1},
    'STR':{'value':NULL, 'statLabel':NULL, 'statEntry':NULL, 'row':3, 'column':1},
}

# Bound to statEntry Entries
def setStatsData(event, dataField, statGiven):
    userInput = event.widget.get()

    # Reset stat value and field label if user clears data
    if userInput == '':
        dataField[statGiven]['value'] = NULL
        dataField[statGiven]['statLabel'].config(foreground='black')
        return

    userInputValue = convertAbbrevNum(userInput)

    if userInputValue == False:
        dataField[statGiven]['statLabel'].config(foreground='red')
        dataField[statGiven]['value'] = NULL
    else:
        dataField[statGiven]['statLabel'].config(foreground='green')
        dataField[statGiven]['value'] = userInputValue
        dataField[statGiven]['statEntry'].delete(0, 'end')
        dataField[statGiven]['statEntry'].insert(0, formatNum(userInputValue))

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
    'HP':{'value':NULL, 'statEntry':NULL, 'statLabel':NULL,  'row':0, 'column':0},
    'ARM':{'value':NULL, 'statEntry':NULL, 'statLabel':NULL,  'row':1, 'column':0},
    'LUK':{'value':NULL, 'statEntry':NULL, 'statLabel':NULL,  'row':2, 'column':0},
    'ATK':{'value':NULL, 'statEntry':NULL, 'statLabel':NULL,  'row':0, 'column':1},
    'DEX':{'value':NULL, 'statEntry':NULL, 'statLabel':NULL,  'row':1, 'column':1},
    'APS':{'value':NULL, 'statEntry':NULL, 'statLabel':NULL,  'row':2, 'column':1},
}

def setBossData(boss):
    for stat, fieldData in bossStatFields.items():
        bossData = getBossInfo(boss)
        statShowValue = formatNum(bossData[stat])
        fieldData['value'] = bossData[stat]
        fieldData['statEntry'].delete(0, 'end')
        fieldData['statEntry'].insert(0, statShowValue)
        fieldData['statLabel'].config(foreground='green')
    

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
playerHP = 1000
playerFrame = Frame()
labelPlayer = Label(master=playerFrame, text='Player')
playerHP = Label(master=playerFrame, text=playerLife, font=('Ariel', 30, BOLD))
labelPlayer.pack()
playerHP.pack()

bossFrame = Frame()
labelBoss = Label(master=bossFrame, text='Boss')
bossHP = Label(master=bossFrame, text=bossLife, font=('Ariel', 30, BOLD))
labelBoss.pack()
bossHP.pack()

playerFrame.grid(row=1,column=1,padx=20,pady=20)
bossFrame.grid(row=1,column=2,padx=20,pady=20)

myButton = Button(window, text='Click', command=click)
myButton.grid(row=2, column=2)

window.mainloop()
# '':{'HP':, 'ARM':, 'LUK':, 'ATK':, 'DEX':, 'APS':},


bossData = {
    'CUSTOM':{},
    'Your Shadow':{'HP':50, 'ARM':1, 'LUK':0, 'ATK':1, 'DEX':0, 'APS':1},
    'Radroach':{'HP':500, 'ARM':10, 'LUK':1, 'ATK':10, 'DEX':3, 'APS':0.5},
    'Frail Scavenger':{'HP':2600, 'ARM':25, 'LUK':5, 'ATK':20, 'DEX':10, 'APS':1},
    'Rat Soldier':{'HP':6000, 'ARM':100, 'LUK':50, 'ATK':25, 'DEX':100, 'APS':3},
    'Momma rat':{'HP':40000, 'ARM':250, 'LUK':500, 'ATK':55, 'DEX':200, 'APS':4},
    'Rat King':{'HP':300000, 'ARM':1500, 'LUK':3000, 'ATK':200, 'DEX':400, 'APS':7},
    'Sentient Poo':{'HP':7400, 'ARM':60, 'LUK':60, 'ATK':60, 'DEX':60, 'APS':1},
    'Sewer Clown':{'HP':18000, 'ARM':100, 'LUK':3000, 'ATK':50, 'DEX':10, 'APS':3},
    'Fecal Mountain':{'HP':40000, 'ARM':500, 'LUK':300, 'ATK':600, 'DEX':300, 'APS':0.8},
    'Scavenger':{'HP':40000, 'ARM':300, 'LUK':300, 'ATK':300, 'DEX':300, 'APS':1},
    'Lowly Bandit':{'HP':72000, 'ARM':500, 'LUK':1000, 'ATK':250, 'DEX':400, 'APS':2},
    'Lubed Assailant':{'HP':200000, 'ARM':800, 'LUK':7000, 'ATK':200, 'DEX':400, 'APS':4},
    'Bandit Boss':{'HP':2200000, 'ARM':3500, 'LUK':20000, 'ATK':600, 'DEX':1000, 'APS':6},
    'Cloud of Flies':{'HP':110000, 'ARM':300, 'LUK':50000, 'ATK':300, 'DEX':500, 'APS':4},
    'Desperate Thief':{'HP':500000, 'ARM':600, 'LUK':2000, 'ATK':700, 'DEX':500, 'APS':1.5},
    'Black Swordsman':{'HP':20000000, 'ARM':3000, 'LUK':1500, 'ATK':1600, 'DEX':200, 'APS':1.5},
    'Lil D':{'HP':80000000, 'ARM':6000, 'LUK':5000, 'ATK':3500, 'DEX':1000, 'APS':2},
}

def getBossInfo(bossName):
    return bossData[bossName]

def allBossNames():
    return bossData.keys()
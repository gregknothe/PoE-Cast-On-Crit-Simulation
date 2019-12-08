import random

cocNovaDmg = 228232.6               #6-Link, CoC Average Ice Nova Damage
cmNovaDmg = 54539.7                 #Cospri's Malice Average Ice Nova Damage
cmBoltDmg = 72987.4                 #Cospri's Malice Average Frost Bolt Damage

mainCycDmg = 8632.2                 #Main Hand Average Cyclone Damage
mainCycSS = 1 / 9.37                #Main Hand Cyclone Swing Speed ( 1 / Attacks Per Sec)
mainCycAcc = .89                    #Main Hand Cyclone Accuracy
mainCycCrit = .7078                 #Main Hand Cyclone Critical Strike Chance

offCycDmg = 5015                    #Off Hand Average Cyclone Damage
offCycSS = 1 / 7.21                 #Off Hand Cyclone Swing Speed ( 1 / Attacks Per Sec)
offCycAcc = .89                     #Off Hand Cyclone Accuracy
offCycCrit = .7228                  #Off Hand Cyclone Critical Strike Chance

cocCD = .016                        #CoC Internal Cooldown (Factoring in Server Ping)
cmCD = .016                         #Cospri's Malice Internal Cooldown

def frostboltExistance(currFBTime):
    #Checks to see if there are close frostbolts to double the nova damage
    #Notes: .75sec is just a estimation of time in which the bolts are in range.
    if currFBTime > .75:
        return 2
    else:
        return 1

def mainHandSwing(currCoCCD, currFBTime, currCMCD, cmA):
    swingDmg = 0
    if random.random() <= mainCycAcc:                                       #Chance to land hit
        swingDmg += mainCycDmg
        if random.random() <= mainCycCrit:                                  #Chance to land critical hit
            if currCoCCD <= 0:                                              #Proc CoC Ice Nova
                swingDmg += frostboltExistance(currFBTime) * cocNovaDmg
                currCoCCD = .016
            if currCMCD <= 0:                                               #Proc either CMBolt or CMNova
                if cmA == 0:
                    swingDmg += cmBoltDmg
                    cmA = 1
                else:
                    swingDmg += frostboltExistance(currFBTime) * cmNovaDmg
                    cmA = 0
                currCMCD = .016
    return swingDmg, currCoCCD, currCMCD, cmA

def offHandSwing(currCoCCD, currFBTime):
    swingDmg = 0
    if random.random() <= offCycAcc:                                        #Chance to land hit
        swingDmg += offCycDmg
        if random.random() <= offCycCrit:                                   #Chance to land critical hit
            if currCoCCD <= 0:                                              #Proc CoC Ice Nova
                swingDmg += frostboltExistance(currFBTime) * cocNovaDmg
                currCoCCD = .016
    return swingDmg, currCoCCD

def CoC_DPS_Calculation():
    currTime, endTime = 0, 60
    cycA = 0                        #Cyclone Alternation: Cyclone alternates weapon attacks (0 = Main, 1 = Off)
    cmA = 0                         #Cospri's Malice Alternation: It cycles the spells if multiple are present.
    totalDmg = 0
    currCoCCD, currCMCD= 0, 0
    currFBTime = 0
    mainSwingTimer, offSwingTimer = 0, offCycSS
    while currTime < endTime:
        if cycA == 0 and mainSwingTimer <= 0:                        #Main Hand Swing
            x = mainHandSwing(currCoCCD, currFBTime, currCMCD, cmA)
            totalDmg += x[0]
            currCoCCD, currCMCD, cmA = x[1], x[2], x[3]
            cycA = 1
            mainSwingTimer, offSwingTimer = mainCycSS, offCycSS
        elif offSwingTimer <= 0:                                     #Off Hand Swing
            y = offHandSwing(currCoCCD, currFBTime)
            totalDmg += y[0]
            currCoCCD = y[1]
            cycA = 0
            mainSwingTimer, offSwingTimer = mainCycSS, offCycSS
        currTime += .001
        currFBTime += -.001
        currCMCD += -.001
        currCoCCD += -.001
        mainSwingTimer += -.001
        offSwingTimer += -.001
    return totalDmg / endTime

def CoC_DPS_Simulation():
    total = 0
    for x in range(0,100):
        total += CoC_DPS_Calculation()
    return total / 100

print str(round(CoC_DPS_Simulation())) + " Shaper DPS"
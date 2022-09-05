import random
import math
import sys
import time
class Die:
    val=0
    held=False
    def __init__(self, val, held):
        self.val = val
        self.held = held
    def __lt__(self, other):
        return self.val < other.val
class Points:
    val=0
    selected=False
    def __init__(self, val, selected):
        self.val = val
        self.selected = selected
    def __lt__(self, other):
        return self.val < other.val
rolls=0
turns=0
size=5 if len(sys.argv) == 1 or (len(sys.argv) > 2 and not sys.argv[1].isnumeric()) or (int(sys.argv[1]) <= 1) else int(sys.argv[1])
maxdiceval=size+1 if len(sys.argv) <= 2 or (len(sys.argv) > 3 and (not sys.argv[1].isnumeric() or not sys.argv[2].isnumeric())) or (int(sys.argv[1]) <= 1 or int(sys.argv[2]) <= 1) else int(sys.argv[2])
bfound=False
tosort=False
tocompress=False
toquit=False
maxrolls=int(math.ceil(max(size, maxdiceval)) * 0.5)
half=int(math.ceil(size * 0.5))
quarters=int(math.ceil(size * 0.75))
dice=[Die(0, False) for i in range(size)]
freqs = [0 for i in range(maxdiceval)]
bonus=0
bonuscore=0
numoptions={i:Points(0, False) for i in range(1, maxdiceval + 1)}
mscoptions={str(half) + " of a kind": Points(0, False), str(quarters) + " of a kind": Points(0, False), str(size >> 1) + " by " + str(half) + " Pair": Points(0, False), str(quarters) + " Straight": Points(0, False), str(size) + " Straight": Points(0, False), "Yahtzee": Points(0, False), "Chance": Points(0, False)}
numscore=0
mscscore=0
totalscore=0

def bonusScore():
    # right shift 1 bit to divide by 2, left shift 1 bit to multiply by 2
    global bonus
    global bonuscore
    global size
    global half
    littlekind=float(half) / size
    n=maxdiceval * size
    # Bonus score is obtained by taking sum of 1..maxdiceval * ceil(# of dice / 2)
    bonus=int(((maxdiceval * (maxdiceval + 1)) >> 1) * (math.ceil(size / 2.0)))
    bonuscore=int(math.ceil(maxdiceval * size * 1.162))

def rolldice():
    global rolls
    global freqs
    global bonuscore
    global size
    global tosort
    global tocompress
    global half
    freqs = [0 for i in range(maxdiceval)]
    if not tosort:
        delay = 0
        while delay <= 10:
            randstr = ""
            for i in range(size):
                if dice[i].held:
                    randstr = randstr + str(dice[i].val) + " "
                else:
                    # Get only last digit of result to keep string length the same
                    # so \r output doesn't leave extra chars
                    randstr = randstr + str(random.randrange(1, maxdiceval + 1) % 10) + " "
            sys.stdout.write("\r" + randstr)
            sys.stdout.flush()
            time.sleep(0.05)
            delay = delay + 1
        sys.stdout.write("\r")
        sys.stdout.flush()
    if rolls < maxrolls or tosort:
        for i in range(0, size):
            if not dice[i].held and not tosort:
                dice[i].val = random.randrange(1, maxdiceval + 1)
            if not tocompress:
                print(str(dice[i].val), end=" ")
            freqs[dice[i].val - 1] += 1
        if not tocompress:
            print('\n')
        if not tosort:
            rolls += 1
        if tocompress:
            for i in range(0, len(freqs)):
                print(str(i + 1) + ":" + str(freqs[i]), end=" ")
            print('\n')
    else:
        print("Can't use!!")

def initializeOptions():
    for i in numoptions.keys():
        numoptions[i].val = 0
    for k in mscoptions.keys():
        mscoptions[k].val = 0

def setNumOptions():
    for i in range(1, maxdiceval + 1):
        if not numoptions[i].selected:
            numoptions[i].val = 0
            for j in range(0, size):
                if (dice[j].val == i):
                    numoptions[i].val += dice[j].val
def findkinds():
    hfound = False
    h2found = False
    global freqs
    global mscscore
    global totalscore
    global bonuscore
    global size
    global half
    halfsize = size >> 1
    evenhalfs = halfsize == half
    sum=0
    h12found=0
    for k in mscoptions.keys():
        if not mscoptions[k].selected:
            mscoptions[k].val = 0
    for i in range(0, size):
        sum+=dice[i].val
    for i in freqs:
        if i == size:
            if mscoptions["Yahtzee"].selected:
                if mscoptions["Yahtzee"].val > 0:
                    mscscore += int(math.ceil(maxdiceval * size * 3.32))
                    totalscore = mscscore + numscore
                    print("ANOTHER YAHTZEE!!!")
                else:
                    print("Yahtzee Had to happen now?!  How dare you!  No bonus for you!")
            else:
                mscoptions["Yahtzee"].val = int(math.ceil(maxdiceval * size * 1.66))
            if not mscoptions[str(quarters) + " of a kind"].selected:
                mscoptions[str(quarters) + " of a kind"].val = sum
            if not mscoptions[str(half) + " of a kind"].selected:
                mscoptions[str(half) + " of a kind"].val = sum
        if i >= quarters and i < size:
            if not mscoptions["Yahtzee"].selected:
                mscoptions["Yahtzee"].val = 0
            if not mscoptions[str(quarters) + " of a kind"].selected:
                mscoptions[str(quarters) + " of a kind"].val = sum
            if not mscoptions[str(half) + " of a kind"].selected:
                mscoptions[str(half) + " of a kind"].val = sum
        if i >= half and i < quarters:
            if not mscoptions["Yahtzee"].selected:
                mscoptions["Yahtzee"].val = 0
            if not mscoptions[str(quarters) + " of a kind"].selected:
                mscoptions[str(quarters) + " of a kind"].val = 0
            if not mscoptions[str(half) + " of a kind"].selected:
                mscoptions[str(half) + " of a kind"].val = sum
            h2found=True
        if i == halfsize:
            hfound=True
            h12found+=1
        if not evenhalfs:
            if hfound and h2found:
                if not mscoptions[str(size >> 1) + " by " + str(half) + " Pair"].selected:
                    mscoptions[str(size >> 1) + " by " + str(half) + " Pair"].val = int(math.ceil(maxdiceval * size * 0.83))
        else:
            if h12found == 2:
                if not mscoptions[str(size >> 1) + " by " + str(half) + " Pair"].selected:
                    mscoptions[str(size >> 1) + " by " + str(half) + " Pair"].val = int(math.ceil(maxdiceval * size * 0.83))
    if not mscoptions["Chance"].selected:
        mscoptions["Chance"].val = sum

def findstraight(large):
    global quarters
    global size
    global freqs
    global bonuscore
    found=True
    maxstrcount=0
    currstrcount=0
    value = size if large else quarters
    for i in range(0, len(freqs)):
        if freqs[i] >= 1:
            currstrcount += 1
            if currstrcount > maxstrcount:
                maxstrcount = currstrcount
            if maxstrcount == value:
                break
        else:
            currstrcount = 0
    found = maxstrcount == value
    if found:
        if value == size or size <= 3:
            if not mscoptions[str(size) + " Straight"].selected:
                mscoptions[str(size) + " Straight"].val = int(math.ceil(maxdiceval * size * 1.33))
        if not mscoptions[str(quarters) + " Straight"].selected and size > 3:
            mscoptions[str(quarters) + " Straight"].val = maxdiceval * size
    else:
        if value == size or size <= 3:
            if not mscoptions[str(size) + " Straight"].selected:
                mscoptions[str(size) + " Straight"].val = 0
        if not mscoptions[str(quarters) + " Straight"].selected and size > 3:
            mscoptions[str(quarters) + " Straight"].val = 0

def nextMove():
    global bonus
    global bonuscore
    global bfound
    global numscore
    global mscscore
    global totalscore
    global rolls
    global turns
    global tosort
    global tocompress
    global size
    global toquit
    tosort = False
    validcmd = False
    toquit=False
    while not validcmd:
        allnums = True
        move = input("Your move!! ")
        if "q" in move or "quit" in move:
            toquit=True
            break
        if "sort" in move:
            dice.sort()
            validcmd = True
            tosort = True
            break
        if "compress" in move:
            dice.sort()
            validcmd = True
            tocompress = True
            tosort = True
            break
        if "expand" in move:
            dice.sort()
            validcmd = True
            tocompress = False
            tosort = True
            break
        if "roll" in move:
            if rolls >= maxrolls:
                print('Invalid!  All rolls used up!')
            else:
                numbers = move.split(' ')
                for i in range(1, len(numbers)):
                    n = numbers[i]
                    if not n.isnumeric():
                        if ":" in n:
                            m = n.split(':')
                            if len(m) == 2 or len(m) == 3:
                                if len(m) == 2:
                                    if m[0].isnumeric() and m[1].isnumeric():
                                        begin = int(m[0])
                                        end = int(m[1])
                                        if begin <= end and (begin > 0 and begin <= size) and (end > 0 and end <= size):
                                            for i in range(begin, end + 1):
                                                dice[i - 1].held = True
                                        else:
                                            print('Invalid.  Numbers must be in range!')
                                            allnums = False
                                            break
                                    else:
                                        print('Invalid.  Only numbers allowed')
                                        allnums = False
                                        break
                                else:
                                    if m[0].isnumeric() and m[1].isnumeric() and m[2].isnumeric():
                                        begin = int(m[0])
                                        end = int(m[1])
                                        step = int(m[2])
                                        if begin <= end and (begin > 0 and begin <= size) and (end > 0 and end <= size) and (step > 0):
                                            for i in range(begin, end + 1, step):
                                                dice[i - 1].held = True
                                        else:
                                            print('Invalid.  Numbers must be in range!')
                                            allnums = False
                                            break
                                    else:
                                        print('Invalid.  Only numbers allowed')
                                        allnums = False
                                        break
                            else:
                                print('Invalid.  Only numbers allowed')
                                allnums = False
                                break
                        else:
                            print('Invalid.  Only numbers allowed')
                            allnums = False
                            break
                    else:
                        if int(n) < 1 or int(n) >= maxdiceval:
                            print('Invalid range!')
                            allnums = False
                        else:
                            dice[int(n) - 1].held = True
                if allnums:
                    validcmd = True
                    break
        else:
            if move.isnumeric():
                try:
                    if not numoptions[int(move)].selected:
                        numscore += numoptions[int(move)].val
                        totalscore = numscore + mscscore
                        for die in dice:
                            die.held = False
                        if numscore >= bonus:
                            if not bfound:
                                print("BONUSPOINTS!!")
                                numscore += bonuscore
                                totalscore = numscore + mscscore
                            bfound = True
                        validcmd = True
                        numoptions[int(move)].selected = True
                        turns += 1
                        rolls = 0
                        break
                    else:
                        print('Invalid.  Already Selected!!')
                except:
                    print('Invalid.  Not in range!!')
            else:
                try:
                    if not mscoptions[move].selected:
                        mscscore += mscoptions[move].val
                        totalscore = mscscore + numscore
                        validcmd = True
                        mscoptions[move].selected = True
                        turns += 1
                        rolls = 0
                        for die in dice:
                            die.held = False
                        break
                    else:
                        print('Invalid.  Already Selected!!')
                except:
                    print('Invalid.  Not in options!!')
def main():
    global bonus
    global bonuscore
    global bfound
    global maxdiceval
    global numscore
    global mscscore
    global size
    global tosort
    global toquit
    bonusScore()
    initializeOptions()
    while(turns < len(numoptions) + len(mscoptions) and not toquit):
        print('Turns Taken: ' + str(turns) + ' / ' + str(len(numoptions) + len(mscoptions)))
        rolldice()
        if not tosort:
            setNumOptions()
            findkinds()
            if not mscoptions[str(size) + " Straight"].selected:
                findstraight(True)
            if not mscoptions[str(quarters) + " Straight"].selected:
                findstraight(False)
        for i in numoptions.keys():
            select = ""
            if numoptions[i].selected:
                select = "(Already Selected!!)"
            print(str(i) + ": " + str(numoptions[i].val) + " / " + str(i * size) + select)
        #bon = ""
        #if bfound:
        #    bon = " (Bonus earned +" + str(bonuscore) + " )"
        print("NUMSCORE: " + str(numscore) + " / " + str(bonus) + " Possible bonus points: " + str(bonuscore) + "\n")
        for k in mscoptions.keys():
            select = ""
            if mscoptions[k].selected:
                select = "(Already Selected!!)"
            if "Pair" in k:
                print(str(k) + ": " + str(mscoptions[k].val) + " / " + str(int(math.ceil(maxdiceval * size * 0.83))) + select)
            else:
                if "Straight" in k:
                    if int(k[0:len(k) - len(" Straight")]) == size:
                        print(str(k) + ": " + str(mscoptions[k].val) + " / " + str(int(math.ceil(maxdiceval * size * 1.33))) + select)
                    else:
                        print(str(k) + ": " + str(mscoptions[k].val) + " / " + str(maxdiceval * size) + select)
                else:
                    if "Yahtzee" in k:
                        print(str(k) + ": " + str(mscoptions[k].val) + " / " + str(int(math.ceil(maxdiceval * size * 1.66))) + select)
                    else:
                        print(str(k) + ": " + str(mscoptions[k].val) + " / " + str(maxdiceval * size) + select)
        mscsum = (int(math.ceil(maxdiceval * size * 0.83))) + (int(math.ceil(maxdiceval * size * 1.33))) + (int(math.ceil(maxdiceval * size * 1.66))) + ((maxdiceval * size) << 2)
        print("MSCSCORE: " + str(mscscore) + " / " + str(mscsum) + " Possible bonus per extra earned Yahtzee: " + str(math.ceil(maxdiceval * size * 3.32)))
        print("\nTOTAL SCORE: " + str(totalscore) + " / " + str(mscsum + bonus) + "\n")
        print("Rolls used: " + str(rolls) + " / " + str(maxrolls))
        nextMove()

    print("\nGAME OVER!!")
    if not mscoptions[str(size) + " Straight"].selected:
        findstraight(True)
    if not mscoptions[str(quarters) + " Straight"].selected:
        findstraight(False)
    for i in numoptions.keys():
        select = ""
        if numoptions[i].selected:
            select = "(Already Selected!!)"
        print(str(i) + ": " + str(numoptions[i].val) + " / " + str(i * size) + select)
    #bon = ""
    #if bfound:
    #    bon = " (Bonus earned +" + str(bonuscore) + " )"
    print("NUMSCORE: " + str(numscore) + " / " + str(bonus) + " Possible bonus points: " + str(bonuscore) + "\n")
    for k in mscoptions.keys():
        select = ""
        if mscoptions[k].selected:
            select = "(Already Selected!!)"
        if "Pair" in k:
            print(str(k) + ": " + str(mscoptions[k].val) + " / " + str(int(math.ceil(maxdiceval * size * 0.83))) + select)
        else:
            if "Straight" in k:
                if int(k[0:len(k) - len(" Straight")]) != size:
                    print(str(k) + ": " + str(mscoptions[k].val) + " / " + str(maxdiceval * size) + select)
                else:
                    print(str(k) + ": " + str(mscoptions[k].val) + " / " + str(int(math.ceil(maxdiceval * size * 1.33))) + select)
            else:
                if "Yahtzee" in k:
                    print(str(k) + ": " + str(mscoptions[k].val) + " / " + str(int(math.ceil(maxdiceval * size * 1.66))) + select)
                else:
                    print(str(k) + ": " + str(mscoptions[k].val) + " / " + str(maxdiceval * size) + select)
    mscsum = (int(math.ceil(maxdiceval * size * 0.83))) + (int(math.ceil(maxdiceval * size * 1.33))) + (int(math.ceil(maxdiceval * size * 1.66))) + ((maxdiceval * size) << 2)
    print("MSCSCORE: " + str(mscscore) + " / " + str(mscsum) + " Possible bonus per extra earned Yahtzee: " + str(math.ceil(maxdiceval * size * 3.32)))
    print("\nTOTAL SCORE: " + str(totalscore) + " / " + str(mscsum + bonus) + "\n")

if __name__=="__main__":
    main()

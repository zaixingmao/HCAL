#!/usr/bin/env python

#Generates .txt file in formatt same with oneRun.py from a list of RBXs

def WordStrip(iStr="", index=""): #iStr: input string, index: the index-th word in the string that you're looking for
    nWord = 0
    i=0
    while i < len(iStr):
        while iStr[i] == " ": 
            i+=1 #get to next word
            if i==len(iStr): break
        iStart = i
        while iStr[i] != " " and i < len(iStr): 
            i+=1
            if i==len(iStr): break
        nWord+=1
        if i==len(iStr): i = len(iStr)-1 #remove '/n' a the end of line
        if nWord == index: return iStr[iStart:i]
    
    return "#%s word not found in string: %s" %(index, iStr)


def WordSpace(iStr="", nSpace=""): 
    while len(iStr) < nSpace:   iStr = " " + iStr
    if len(iStr) == nSpace: return iStr
    else:   print "Error in fixing #char per word"
    

def DoubleSpace(iStr=""):
    oStr = []
    for i in range(0, len(iStr)):   oStr.append(iStr[i])
    return "  ".join(oStr)

def subString(line, newWord, index):
    nWord = 0
    i = 0
    wordLength = len(newWord)
    while i < len(line):
        while line[i] == ' ':
            i+=1 #get to next word
            if i==len(line): break
        iStart = i
        while line[i] != " " and i < len(line): 
            i+=1
            if i==len(line): break
        nWord += 1
        if i==len(line): i = len(line)-1 #remove '/n' a the end of line
        if nWord == index:
            if (i-iStart) > wordLength:
                newLine = line[0:iStart] 
                for j in range(i-iStart-wordLength): newLine += ' ' #clear previous word
            else:
                newLine = line[0:i-wordLength]

            for k in range(len(newWord)): newLine += newWord[k]
            newLine += line[i:len(line)]
            return newLine
    return "#%s word not found in string: %s" %(index, line)


def makeEMap(ifile = "", ofile = ""):

    output = open(ofile, "w")  #opens & write the file

    lines = open(ifile, "r").readlines()

    
    for i in range(0, len(lines)):   #loop through Map file
        current_line = lines[i] 
        if "#" in current_line:   #over pass un_needed lines
            output.writelines(current_line) 
            continue

        subDet = WordStrip(current_line, 9)
        if subDet == 'HF':
            crate = int(WordStrip(current_line, 2))
            sl = int(WordStrip(current_line, 3))
            tb = WordStrip(current_line, 4)
            dcc = int(WordStrip(current_line, 5))
            spigot = int(WordStrip(current_line, 6))
            fiber = int(WordStrip(current_line, 7))
            
            #changes
            current_line = subString(current_line, str(crate+20), 2)

            if sl in range(2,8): current_line = subString(current_line, str(sl-1), 3)
            elif sl in range(13,19): current_line = subString(current_line, str(sl-6), 3)
            else: current_line = subString(current_line, '-', 3)

            current_line = subString(current_line, 'u', 4)
            current_line = subString(current_line, '0', 5)
            current_line = subString(current_line, '0', 6)

            if tb == 'b': current_line = subString(current_line, str(fiber+1), 7)
            elif tb == 't': current_line = subString(current_line, str(fiber+13), 7)
                    
        output.writelines(current_line)


    output.close() 


makeEMap(ifile = "/Users/zmao/Downloads/version_E_emap.txt", ofile = "version_E_emap_new3.txt") 

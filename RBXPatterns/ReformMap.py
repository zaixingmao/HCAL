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

def getKeyPosition(mapFileName = ""):
    keyPosition = {}
    keyPosition["RBXname"] = 8
    keyPosition["rm"] = 10
    keyPosition["rm_fib"] = 14
    keyPosition["fi_ch"] = 15
    
    if "HBEF" in mapFileName:
        keyPosition["htr_fib"] = 19
        keyPosition["spigo"] = 21
        keyPosition["fedid"] = 31
    if "HO" in mapFileName:
        keyPosition["htr_fib"] = 20
        keyPosition["spigo"] = 22
        keyPosition["fedid"] = 24
    if "CALIB" in mapFileName:
        keyPosition["RBXname"] = 7
        keyPosition["rm"] = 9
        keyPosition["rm_fib"] = 10
        keyPosition["fi_ch"] = 11
        keyPosition["htr_fib"] = 15
        keyPosition["spigo"] = 17
        keyPosition["fedid"] = 19

    return keyPosition
        
        

def ReformMap(iMapfile = "", iListfile = "", ofile = "", oFileOpenMode = "w"):

    lines = open(iMapfile, "r").readlines() #opens & read the file
    output = open(ofile, oFileOpenMode)  #opens & write the file

    ListLines = open(iListfile, "r").readlines()

    subdet = []
    for i in range(0, len(ListLines)): #store subdet names
        current_line = ListLines[i]
        subdet.append(current_line[0:current_line.find(",")])

    RBXnameRange = subdet
    rmRange = ['1','2','3','4']
    if "CALIB" in iMapfile: rmRange = ['4','5']
    keyPosition = getKeyPosition(iMapfile)

    for i in range(0, len(lines)):   #loop through Map file
        if "## file created" in lines[i]: continue  #over pass un_needed lines
        if "#   side    eta    phi   dphi" in lines[i]: continue
        current_line = lines[i]
    
        RBXname = WordStrip(current_line, keyPosition["RBXname"])
        rm = str(WordStrip(current_line, keyPosition["rm"]))
        rm_fib = str(WordStrip(current_line, keyPosition["rm_fib"]))
        fi_ch = str(WordStrip(current_line, keyPosition["fi_ch"]))
        htr_fib = str(WordStrip(current_line, keyPosition["htr_fib"]))
        spigo = str(WordStrip(current_line, keyPosition["spigo"]))
        fedid = str(WordStrip(current_line, keyPosition["fedid"]))

        spigo = WordSpace(spigo,2)
        htr_fib = WordSpace(htr_fib,2)
    
        if RBXname in RBXnameRange:
            if rm in rmRange and fi_ch == "0": #save only once per 3 channels
                if len(RBXname)==5: outline = fedid + " " + spigo + " " + htr_fib + ":  " + RBXname + "  " + rm + " " + rm_fib + "\n"
                else: outline = fedid + " " + spigo + " " + htr_fib + ":  " + RBXname + " " + rm + " " + rm_fib + "\n"
                output.writelines(outline)

    output.close()   

ReformMap(iMapfile = "HCALmapHO_A.txt", iListfile = "CCM_numbers.txt", ofile = "all_Map.txt") 
ReformMap(iMapfile = "HCALmapHBEF_B.txt", iListfile = "CCM_numbers.txt", ofile = "all_Map.txt", oFileOpenMode = "a") 
ReformMap(iMapfile = "HCALmapCALIB_A.txt", iListfile = "CCM_numbers.txt", ofile = "all_Map.txt", oFileOpenMode = "a")
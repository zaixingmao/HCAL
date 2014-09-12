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

 


def ReformMapNew(iMapfile = "", iListfile = "", ofile = ""):

    lines = open(iMapfile, "r").readlines() #opens & read the file
    output = open(ofile, "w")  #opens & write the file

    ListLines = open(iListfile, "r").readlines()

    subdet = []
    for i in range(0, len(ListLines)): #store subdet names
        current_line = ListLines[i]
        subdet.append(current_line[0:current_line.find(",")])

    RBXnameRange = subdet
    rmRange = ["1","2","3","4"]
    PrevSpigo = " "
    
    RBXPatterns = []
    
    for i in range(0, len(lines)):   #loop through Map file
        if "## file created" in lines[i]: continue  #over pass un_needed lines
        if "#   side    eta    phi   dphi" in lines[i]: continue
        current_line = lines[i]
    
        RBXname = WordStrip(current_line, 8)
        rm = str(WordStrip(current_line, 10))
        rm_fib = str(WordStrip(current_line, 14))
        fi_ch = str(WordStrip(current_line, 15))
        htr_fib = str(WordStrip(current_line, 19))
        spigo = str(WordStrip(current_line, 21))
        fedid = str(WordStrip(current_line, 31))

        spigo = WordSpace(spigo,2)
        htr_fib = WordSpace(htr_fib,2)

        RBXPatterns.append((fedid, spigo, htr_fib, RBXname, rm, rm_fib))
        print RBXPatterns
    output.close() 
'''
        if RBXname in RBXnameRange:
            if rm in rmRange and fi_ch == "0": #save only once per 3 channels
                if len(RBXname)==5: outline = fedid + " " + spigo + " " + htr_fib + ":   " + DoubleSpace(RBXname) + "  " + rm + "  " + rm_fib + "  -  -  -  0  0  0  0  0  0  0  0  0  0\n"
                else: outline = fedid + " " + spigo + " " + htr_fib + ":   " + DoubleSpace(RBXname) + "  " + rm + "  " + rm_fib + "  -  -  0  0  0  0  0  0  0  0  0  0\n"
                output.writelines(outline)
'''  

ReformMapNew(iMapfile = "HCALmapHBEF_B.txt", iListfile = "CCM_numbers.txt", ofile = "test.txt") 

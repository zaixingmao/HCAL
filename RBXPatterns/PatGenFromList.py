#!/usr/bin/env python

#Generates all possible pattern bricks with elements in ascii hex values for a list of RBXs, stores in new xml file

def encode(input):
    output = input - 32
    output = output*2
    return output

def generator(rbx="", rm="", card="", qie=""):
    out = []
    for letter in rbx:
        out.append(format(encode(ord(letter)),"x"))
    for i in str(rm):
        out.append(format(encode(ord(str(i))),"x"))
    rm_fib = 2*card + qie/4
    if "HF" in rbx: 
        rm_fib -= 1
    for i in str(rm_fib):
        out.append(format(encode(ord(str(i))),"x"))
    return " ".join(out)


def generatorCM(rbx="", rm="", qie=""):
    out = []
    rm_new = encode(rm)
    qie_new = encode(qie)

    for letter in rbx:
        out.append(format(encode(ord(letter)),"x"))
    for i in str(rm):
        out.append(format(encode(ord(str(i))),"x"))
    rm_fib = 1 + qie/4
    for i in str(rm_fib):
        out.append(format(encode(ord(str(i))),"x"))
    return " ".join(out)


def PatGenFromList(ifile = "", ofile = ""):

    hyphen = '1a'
    hyphen_10 = hyphen
    for i in range(9):
        hyphen_10 += ' %s' %hyphen
    lines = open(ifile, "r").readlines()
    output = open(ofile, "w")

    rmRange = range(1,5)
    cardRange = range(1,4)
    subdet = []
    for i in range(0, len(lines)):
        current_line = lines[i]
        subdet.append(current_line[0:current_line.find(",")])

    #for subdet in ["HEP"]: 
    for rbx in subdet:   #Select Sub-Detector Range
        
        brick_begin = '<CFGBrick>\n'
        param1 = '  <Parameter name="RBX" type="string">%s</Parameter>\n' % rbx
        param2 = '  <Parameter name="INFOTYPE" type="string">PATTERNS</Parameter>\n'
        param3 = '  <Parameter name="CREATIONTAG" type="string">pattern_test</Parameter>\n'
        param4 = '  <Parameter name="CREATIONSTAMP" type="string">13-08-13</Parameter>\n'
        output.writelines(brick_begin + param1 + param2 + param3 + param4)
        
        if "HF" in rbx: #for special case of HF
            rmRange = range(1,4)
            cardRange = range(1,5)
        else:
            rmRange = range(1,5)
            cardRange = range(1,4)

        for rm in rmRange:
            if rm == 4 and (rbx[0:2] == "HF" or rbx[0:2] == "HE"):
                preSpace = ""
                postSpace = hyphen_10
            else:
                preSpace = hyphen_10
                preSpace += " "
                postSpace = ""

            for card in cardRange:
                for qie in [0,4]:
                    if rbx[0:4] in ["HO1M", "HO2M", "HO1P", "HO2P"]:
                        brick = '   <Data elements="20" encoding="hex" rm="%s" card="%s" qie="%s">%s%s %s %s %s</Data>\n' %(rm, card, qie, preSpace, hyphen, generator(rbx, rm, card, qie), hyphen, postSpace)
                        output.writelines(brick)
                    else:
                        brick = '   <Data elements="20" encoding="hex" rm="%s" card="%s" qie="%s">%s%s %s %s %s %s</Data>\n' %(rm, card, qie, preSpace, hyphen, generator(rbx, rm, card, qie), hyphen, hyphen, postSpace)
                        output.writelines(brick)

        #For Calibration Module
        rm += 1
        card = 1
        for qie in [0,4]:
            if rbx[0:4] in ["HO1M", "HO2M", "HO1P", "HO2P"]:
                brick = '   <Data elements="20" encoding="hex" rm="%s" card="1" qie="%s">%s%s %s %s %s</Data>\n' %(rm, qie, preSpace, hyphen, generatorCM(rbx, rm, qie), hyphen, postSpace)
                output.writelines(brick)
            else:
                brick = '   <Data elements="20" encoding="hex" rm="%s" card="1" qie="%s">%s%s %s %s %s %s</Data>\n' %(rm, qie, preSpace, hyphen, generatorCM(rbx, rm, qie), hyphen, hyphen, postSpace)
                output.writelines(brick)
        brick_end = '</CFGBrick>\n\n'
        output.writelines(brick_end)
                
    output.close()

PatGenFromList("CCM_numbers.txt", "patterns_test.xml")

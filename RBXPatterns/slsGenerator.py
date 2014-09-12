#!/usr/bin/env python

#Generates all possible pattern bricks with elements in ascii hex values, stores in new xml file
def RMcore(rbx="", rm=""):
    rmAddMap = ['0x20','0x10','0x02','0x01']
    if rbx in ["HEP", "HEM"]:
        rmAddMap = ['0x01', '0x02', '0x10', '0x20']
    return rmAddMap[rm-1]


def generator1(rbx=""):
    out = []
    i = 0
    for letter in rbx:
        i+=1
        if i<6:
            out.append('0x'+format(ord(letter),"x"))
    return " ".join(out)

def generator2(rm="", card="", cca=""):
    out = []
    for i in str(rm):
        out.append('0x'+format(ord(str(i)),"x"))
    rm_fib = 2*(card-1) + 2 + cca/2
    for i in str(rm_fib):
        out.append('0x'+format(ord(str(i)),"x"))
    return " ".join(out)

def generator2_2(rbx="",rm="", card="", cca=""):
    out = []
    out.append('0x'+format(ord(str(rbx[5])),"x"))
    for i in str(rm):
        out.append('0x'+format(ord(str(i)),"x"))
    rm_fib = 2*(card-1) + 2 + cca/2
    for i in str(rm_fib):
        out.append('0x'+format(ord(str(i)),"x"))
    return " ".join(out)

output = open("PATTERNS_new10.sls", "w")


for subdet in ["HEP"]:   #Select Sub-Detector Range
    for box in [10]:    #Select rbx Range
        box = "%02d" % box   #adds a leading 0 to single digits
        rbx = subdet+str(box)
        
        rmRange = [1,2,3,4] #Select rm Range
        
        FillEmpty = '0x2d'
        
        param1 = '; RBX: %s\n' % rbx
        param2 = '; specify and enable patterns for RM: %s\n' %rmRange
        output.writelines(param1 + param2)
        
        for rm in rmRange:
            param3 = '; rm: %s\n' %rm
            output.writelines(param3)
            for card in range(1,4):
                param4 = '; card: %s\n' %card
                output.writelines(param4)
                for cca in [0,1,2]:
                    brick0 = '; cca: %s\n' %(cca+1)
                    brick = 'W 0 %s 1 0x%s%s 0x0  0x02\n' %(RMcore(subdet, rm), card-1, cca)
                    output.writelines(brick0+brick)
                    brick1 = 'W 0 %s 5 0x%s%s 0x8  %s\n' %(RMcore(subdet, rm), card-1, cca, generator1(rbx))
                    if subdet in ["HO1M", "HO2M", "HO1P", "HO2P"]:
                        brick2 = 'W 0 %s 5 0x%s%s 0xd  %s %s %s\n' %(RMcore(subdet, rm), card-1, cca, generator2_2(rbx, rm, card, cca), FillEmpty, FillEmpty)
                    else:
                        brick2 = 'W 0 %s 5 0x%s%s 0xd  %s %s %s %s\n' %(RMcore(subdet, rm), card-1, cca, generator2(rm, card, cca), FillEmpty, FillEmpty, FillEmpty)
                    brick3 = 'W 0 %s 5 0x%s%s 0x12 %s %s %s %s %s\n' %(RMcore(subdet, rm), card-1, cca, FillEmpty, FillEmpty, FillEmpty, FillEmpty, FillEmpty)
                    brick4 = 'W 0 %s 5 0x%s%s 0x17 %s %s %s %s %s\n' %(RMcore(subdet, rm), card-1, cca, FillEmpty, FillEmpty, FillEmpty, FillEmpty, FillEmpty)
                    output.writelines(brick1+brick2+brick3+brick4)
        
        brick_end = '\n'
        output.writelines(brick_end)
                
output.close()
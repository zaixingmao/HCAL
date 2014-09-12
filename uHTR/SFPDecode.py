#!/usr/bin/env python
import optparse
import sys

#run like: python SFPDecode.py --sample=/Users/zmao/Downloads/dump.txt --startFrom=1

def formatOutput(input):
    hexForm = str(hex(input))
    if len(hexForm) == 3:
        hexForm = '0x0'+ hexForm[2:3]
    return hexForm[2:]

def decoder(words, bxCounter):
    E1 = int(words[0][2:4], 16)
    T1 = int(words[2][3:4], 16) & 1
    E3 = int(words[0][0:2], 16)
    T3 = int(words[2][1:2], 16) & 1
    E5 = int(words[1][2:4], 16)
    T5 = int(words[3][3:4], 16) & 1
    E7 = int(words[1][0:2], 16)
    T7 = int(words[3][1:2], 16) & 1


    E4 = int(words[2], 16) >> 9
    E4_lastBit = (int(words[4], 16) >> 8) & 1
    E4 += (E4_lastBit << 7)
    T4 = (int(words[4][1:2], 16) >> 1) & 1

    E2 = int(words[2][2:4], 16) >> 1
    E2_lastBit = int(words[4], 16) & 1
    E2 += (E2_lastBit << 7)
    T2 = (int(words[4][3:4], 16) >> 1) & 1

    E8 = int(words[3], 16) >> 9
    E8_lastBit = (int(words[5], 16) >> 8) & 1
    E8 += (E8_lastBit << 7)
    T8 = (int(words[5][1:2], 16) >> 1) & 1

    E6 = int(words[3][2:4], 16) >> 1
    E6_lastBit = int(words[5], 16) & 1
    E6 += (E6_lastBit << 7)
    T6 = (int(words[5][3:4], 16) >> 1) & 1

    BC0 = int(words[4][0:1],16)>>3
    BC0 += (int(words[5][0:1], 16)>>3)<<1
    BC0 += (int(words[4][2:3], 16)>>3)<<2
    BC0 += (int(words[5][2:3], 16)>>3)<<3

    BC0 = "{0:b}".format(BC0)
    while len(BC0) < 4:
        BC0 = "0" + BC0

    Ham1 = (int(words[4][2:4], 16)>>2) & 0x1f
    Ham2 = (int(words[4][0:2], 16)>>2) & 0x1f
    Ham3 = (int(words[5][2:4], 16)>>2) & 0x1f
    Ham4 = (int(words[5][0:2], 16)>>2) & 0x1f

    print "%i\t%s   %i%s %i%s %i%s %i%s %i%s %i%s %i%s %i%s   %s %s %s %s" %(bxCounter, BC0,
                         T1, formatOutput(E1),
                         T2, formatOutput(E2),
                         T3, formatOutput(E3),
                         T4, formatOutput(E4),
                         T5, formatOutput(E5),
                         T6, formatOutput(E6),
                         T7, formatOutput(E7),
                         T8, formatOutput(E8),
                         formatOutput(Ham1),
                         formatOutput(Ham2),
                         formatOutput(Ham3),
                         formatOutput(Ham4))


def decode(lines, pStart, pEnd, bxCounter):
    counter = 0
    words = []
    for iLine in range(pStart, pEnd):
        current_line = lines[iLine]
        #chop off prefix
        current_line = current_line.split()[1][4:8]
        words.append(current_line)
    decoder(words, bxCounter)
    
def SFPDecode(location, startFrom):
    lines = open(location, "r").readlines()
    startDecode = False
    i = 0
    bxCounter = 0
    print "------------------------------------------------------------"
    print "BX       BC0    E1  E2  E3  E4  E5  E6  E7  E8  Ham1 2  3  4"
    print "------------------------------------------------------------"

    while i < len(lines): 
        if i == startFrom:
            startDecode = True
        if startDecode:
            if i+6 >= len(lines):
                break
            decode(lines, i, i+6, bxCounter)
            bxCounter += 1
            i += 5
        i += 1

def opts():
    parser = optparse.OptionParser()
    parser.add_option("--sample", dest="location", default="", help="location for dump file")
    parser.add_option("--startFrom", dest="startFrom", default=0, help="start of decoding")
    options, args = parser.parse_args()
    if not options.location:
        parser.print_help()
        sys.exit(1)
    return options

if __name__ == "__main__":
    options = opts()
    location = options.location
    startFrom = int(options.startFrom)
    SFPDecode(location, startFrom)

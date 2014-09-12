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
    E3 = int(words[0][0:2], 16)
    E5 = int(words[1][2:4], 16)
    E7 = int(words[1][0:2], 16)

    E4 = int(words[2], 16) >> 9
    E4_lastBit = (int(words[4], 16) >> 8) & 1
    E4 += (E4_lastBit << 7)

    E2 = int(words[2][2:4], 16) >> 1
    E2_lastBit = int(words[4], 16) & 1
    E2 += (E2_lastBit << 7)

    E8 = int(words[3], 16) >> 9
    E8_lastBit = (int(words[5], 16) >> 8) & 1
    E8 += (E8_lastBit << 7)

    E6 = int(words[3][2:4], 16) >> 1
    E6_lastBit = int(words[5], 16) & 1
    E6 += (E6_lastBit << 7)

    print "BX%i\t%s %s %s %s %s %s %s %s" %(bxCounter,
                                            formatOutput(E1),
                                            formatOutput(E2),
                                            formatOutput(E3),
                                            formatOutput(E4),
                                            formatOutput(E5),
                                            formatOutput(E6),
                                            formatOutput(E7),
                                            formatOutput(E8))


def decode(lines, pStart, pEnd, preFix, bxCounter):
    counter = 0
    words = []
    for iLine in range(pStart, pEnd):
        current_line = lines[iLine]
        current_line = current_line[preFix:preFix+4]
        words.append(current_line)
    decoder(words, bxCounter)
    
def SFPDecode(location, startFrom):
    lines = open(location, "r").readlines()
    startDecode = False
    i = 0
    bxCounter = 0
    print "-------------------------------"
    print "BX\tE1 E2 E3 E4 E5 E6 E7 E8"
    print "-------------------------------"

    while i < len(lines):
        current_line = lines[i]
        #chop off prefix
        prefixEndPosition = 8
        current_line = current_line[prefixEndPosition:prefixEndPosition+4]
        if i == startFrom:
            startDecode = True
        if startDecode:
            if i+6 >= len(lines):
                break
            decode(lines, i, i+6, prefixEndPosition, bxCounter)
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

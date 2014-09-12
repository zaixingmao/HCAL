#!/usr/bin/env python
import optparse

#run like: python SFPDecode.py --sample=/Users/zmao/Downloads/dump.txt --startFrom=1

def decoder(words):
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

    print 'E1: %s' %hex(E1)
    print 'E2: %s' %hex(E2)
    print 'E3: %s' %hex(E3)
    print 'E4: %s' %hex(E4)
    print 'E5: %s' %hex(E5)
    print 'E6: %s' %hex(E6)
    print 'E7: %s' %hex(E7)
    print 'E8: %s' %hex(E8)

def decode(lines, pStart, pEnd, preFix):
    counter = 0
    words = []
    for iLine in range(pStart, pEnd):
        current_line = lines[iLine]
        current_line = current_line[preFix:preFix+4]
        words.append(current_line)
    decoder(words)
    
def opts():
    parser = optparse.OptionParser()
    parser.add_option("--sample", dest="location", default=" ", help="location for dump file")
    parser.add_option("--startFrom", dest="startFrom", default=0, help="start of decoding")
    options, args = parser.parse_args()

    return options

options = opts()
location = options.location
startFrom = int(options.startFrom)

lines = open(location, "r").readlines()
startDecode = False
i = 0

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
        print ''
        decode(lines, i, i+6, prefixEndPosition)
        i += 5
    i += 1
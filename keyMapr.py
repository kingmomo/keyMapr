#!/usr/bin/python

import sys
import re

def usageInfo():
    print ">>>>>"
    print "Map key codes to its name"
    print "Usage: "+sys.argv[0]+" <path>/<logfile>"
    print "Look for: KEY_PRESS = <key>"
    print "Output: <path>/<logfile>_changed"
    print "<<<<<"
    return

keyMap = {
            '0x30' : '0',
            '0x31' : '1',
            '0x32' : '2',
            '0x33' : '3',
            '0x34' : '4',
            '0x35' : '5',
            '0x36' : '6',
            '0x37' : '7',
            '0x38' : '8',
            '0x39' : '9',
            '0x40000001' : 'exit',
            '0x40000004' : 'select/ok',
            '0x4000000c' : 'page+',
            '0x4000000d' : 'page-',
            '0x4000000e' : 'up',
            '0x4000000f' : 'down',
            '0x40000010' : 'left',
            '0x40000011' : 'right',
            '0x40000083' : 'guide',
            '0x40000084' : 'C',
            '0x40000085' : 'D',
            '0x40000086' : 'A',
            '0x40000087' : 'B',
            '0x40000088' : 'menu',
            '0x40000089' : 'info',
            '0x4000008e' : 'standby',
            '0x40000090' : 'fav',
            '0x4000009d' : 'live',
            '0x400000a2' : 'ch+',
            '0x400000a3' : 'ch-',
            '0x400000af' : 'last',
            '0x40000100' : 'play',
            '0x40000101' : 'pause',
            '0x40000102' : 'stop',
            '0x40000103' : 'record',
            '0x40000104' : 'fwd',
            '0x40000105' : 'rew',
            '0x40000200' : '#',
            '0x40000201' : '*',
            '0x40000204' : 'skip',
            '0x40000205' : 'settings',
            '0x40000206' : 'pip on/off',
            '0x40000207' : 'pip swap',
            '0x40000208' : 'pip move',
            '0x40000209' : 'pip ch+',
            '0x4000020a' : 'pip ch-',
            '0x4000020b' : 'video source',
            '0x40000217' : 'list',
            '0x40000218' : 'day+',
            '0x40000219' : 'day-'
         }

try:
    inFile = sys.argv[1]
    f = open(inFile, "r")
except:
    print "ERR: invalid use"
    usageInfo()
    quit()

print ">>>>>"
print "Processing file: " + inFile
contents = f.readlines()
f.close()
counter = 0
keyCounter = 0
firstKeyPressInfo = "<LINE> : <TIME> : <KEY>\n\n"

keyPressPattern = re.compile("^.*\|.key.*: .*$")
firstKeyPattern = re.compile("\+key\:")
keyTimePattern = re.compile("... .. ..:..:..")

with open(sys.argv[1], 'r') as file:
    for lineCount, line in enumerate(file):
	matchKeyPress = re.search(keyPressPattern, line)
	if matchKeyPress:
	    counter = counter+1
	    keyCode = re.sub('^.*\|.key.*: ', '',matchKeyPress.group())
            keyCode = keyCode.strip()
            try:
                keyName = keyMap[keyCode];
            except:
                keyName = keyCode
            line = line.rstrip('\n')
            contents[lineCount] = line + " KEY_PRESS = " + keyName + "\n"

            matchFirstKeyPress = re.search(firstKeyPattern, line)
            if matchFirstKeyPress:
                keyCounter = keyCounter + 1
                matchKeyTime = re.search(keyTimePattern, line)
                keyTime = matchKeyTime.group()
                firstKeyPressInfo += str(lineCount+1) + " : " + keyTime + " : " + keyName + "\n"

if counter:
    outFile = inFile+"_changed"
    f = open(outFile, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()
    print inFile + " processed successfully\n"
    print "Total number of key presses = " + str(keyCounter)
    print firstKeyPressInfo
    
    print "Output file is " + outFile
    print "Look for: KEY_PRESS = <key>"
    print "\nTo compare files before use run:"
    print "vimdiff " + outFile + " " + inFile
    print "\nTo use changed file run:"
    print "mv " + outFile + " " + inFile + "\n"
print "<<<<<"

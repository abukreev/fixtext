#!/usr/bin/python3

import logging
import os
import sys
from subprocess import Popen, PIPE

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/home/sasha/fixtext.log', 'a', 'utf-8')
handler.setFormatter(logging.Formatter('%(name)s %(message)s'))
#logger.addHandler(handler)

LAT="`qwertyuiop[]asdfghjkl;'zxcvbnm,./"
CYR="ёйцукенгшщзхъфывапролджэячсмитьбю."

KEY_L_CTRL=29
KEY_V=47
KEY_CAPS=58

os.environ["YDOTOOL_SOCKET"] = "/tmp/.ydotool.socket"

assert len(LAT) == len(CYR)

LatToCyr = dict(zip(LAT, CYR))
CyrToLat = dict(zip(CYR, LAT))

def fixLayout(inp):
    conv = (LatToCyr, CyrToLat)
    output = ""
    for symbol in inp:
        if symbol in conv[0]:
            output = output + conv[0][symbol]
        elif symbol in conv[1]:
            output = output + conv[1][symbol]
            conv = (conv[1], conv[0])
        else:
            output = output + symbol
    return output

def runCommand(args, inp=None):
    logger.debug('args = %s', args)
    process = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    (output, err) = process.communicate(input=inp.encode("utf-8") if inp else None)
    logger.debug('out = %s', output)
    res = process.wait()
    return res, output.decode("utf-8"), err.decode("utf-8")

def getSelectionBuffer():
    res, output, err = runCommand(["xsel", "-o"])
    logger.debug('res = %d, output = "%s", err = "%s"', res, output, err)
    if res == 0:
        return output
    raise RuntimeError(f'xsel failed: {err}')

def getClipboardContents():
    res,output, err = runCommand(["xsel", "-b"])
    if res == 0:
        return output
    raise RuntimeError(f'xsel failed: {err}')

def copyToClipboard(string):
    res, output, err = runCommand(["xsel", "-bi"], inp=string)
    if res == 0:
        logger.debug('out = %s', output)
        return output
    raise RuntimeError(f'xsel failed: {err}')
    
def pasteFromClipboard():
    runCommand(['ydotool', 'key', f"{str(KEY_L_CTRL)}:1"])    
    runCommand(['ydotool', 'key', f"{str(KEY_V)}:1"     ])    
    runCommand(['ydotool', 'key', f"{str(KEY_V)}:0"     ])    
    runCommand(['ydotool', 'key', f"{str(KEY_L_CTRL)}:0"])    

def switchLocale():
    runCommand(['ydotool', 'key', f"{str(KEY_CAPS)}:1"])    
    runCommand(['ydotool', 'key', f"{str(KEY_CAPS)}:0"])    

def main():
    buf = getSelectionBuffer()
    logger.debug('SelectionBuffer: "%s"', buf)
    if (not buf):
        return 0
    backup = getClipboardContents()    
    logger.debug('Backup clipboard: "%s"', backup)
    fixed = fixLayout(buf)
    logger.debug('Fixed string: "%s"', fixed)
    copyToClipboard(fixed)
    logger.debug('Successfully copied fixed text to clipboard')
    pasteFromClipboard()
    logger.debug('Successfully paste fixed text from clipboard')
    if (backup):
        copyToClipboard(backup)
        logger.debug('Successfully restored clipboard contents')
    switchLocale()
    logger.debug('Successfully switched the locale')
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except RuntimeError as e:
        sys.exit(1)


#!/usr/bin/python3

import logging
import os
import sys
from subprocess import Popen, PIPE
from time import sleep

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/home/sasha/fixtext.log', 'a', 'utf-8')
handler.setFormatter(logging.Formatter('%(name)s %(message)s'))
#logger.addHandler(handler)

KEY_L_CTRL=29
KEY_V=47
KEY_CAPS=58

def fixLayout(inp):
    LAT="`qwertyuiop[]asdfghjkl;'zxcvbnm,./"
    CYR="ёйцукенгшщзхъфывапролджэячсмитьбю."
    assert len(LAT) == len(CYR)
    LatToCyr = dict(zip(LAT, CYR))
    CyrToLat = dict(zip(CYR, LAT))
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
    process = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    (output, err) = process.communicate(input=inp.encode("utf-8") if inp else None)
    res = process.wait()
    return res, output.decode("utf-8"), err.decode("utf-8")

class XSelYDoToolStrategy:
    _timeout = 0.1

    def __init__(self):
        os.environ["YDOTOOL_SOCKET"] = "/tmp/.ydotool.socket"

    @staticmethod
    def getSelectionBuffer():
        res, output, err = runCommand(["xsel", "-o"])
        logger.debug('res = %d, output = "%s", err = "%s"', res, output, err)
        if res == 0:
            return output
        raise RuntimeError(f'xsel failed: {err}')

    @staticmethod
    def getClipboardContents():
        res,output, err = runCommand(["xsel", "-b"])
        if res == 0:
            return output
        raise RuntimeError(f'xsel failed: {err}')

    @staticmethod
    def copyToClipboard(string):
        res, output, err = runCommand(["xsel", "-bi"], inp=string)
        if res == 0:
            logger.debug('out = %s', output)
            return output
        raise RuntimeError(f'xsel failed: {err}')

    @staticmethod
    def pasteFromClipboard():
        runCommand(['ydotool', 'key', f"{KEY_L_CTRL}:1"])
        runCommand(['ydotool', 'key', f"{KEY_V}:1"     ])
        runCommand(['ydotool', 'key', f"{KEY_V}:0"     ])
        runCommand(['ydotool', 'key', f"{KEY_L_CTRL}:0"])
        sleep(XSelYDoToolStrategy._timeout)

    @staticmethod
    def switchLocale():
        runCommand(['ydotool', 'key', f"{KEY_CAPS}:1"])
        runCommand(['ydotool', 'key', f"{KEY_CAPS}:0"])

def main():
    strategy = XSelYDoToolStrategy()
    
    buf = strategy.getSelectionBuffer()
    logger.debug('SelectionBuffer: "%s"', buf)
    if (not buf):
        return 0
    backup = strategy.getClipboardContents()    
    logger.debug('Backup clipboard: "%s"', backup)
    fixed = fixLayout(buf)
    logger.debug('Fixed string: "%s"', fixed)
    strategy.copyToClipboard(fixed)
    logger.debug('Successfully copied fixed text to clipboard')
    sleep(strategy._timeout)
    strategy.pasteFromClipboard()
    logger.debug('Successfully paste fixed text from clipboard')
    if (backup):
        strategy.copyToClipboard(backup)
        logger.debug('Successfully restored clipboard contents')
    strategy.switchLocale()
    logger.debug('Successfully switched the locale')
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except RuntimeError as e:
        sys.exit(1)


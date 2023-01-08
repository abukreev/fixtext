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
    LAT="`qwertyuiop[]asdfghjkl;'zxcvbnm,./~QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?"
    CYR="ёйцукенгшщзхъфывапролджэячсмитьбю.ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"
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


class YDoToolStartegy:
    def __init__(self):
        os.environ["YDOTOOL_SOCKET"] = "/tmp/.ydotool.socket"

    def keyPress(self, keyCode):
         runCommand(['ydotool', 'key', f"{keyCode}:1"])

    def keyRelease(self, keyCode):
         runCommand(['ydotool', 'key', f"{keyCode}:0"])


class XSelStrategy:
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


class XSelYDoToolStrategy:
    _timeout = 0.1
    _clipboardStrartegy = XSelStrategy()
    _keyStrategy = YDoToolStartegy()

    @staticmethod
    def getSelectionBuffer():
        return XSelYDoToolStrategy._clipboardStrartegy.getSelectionBuffer()

    @staticmethod
    def getClipboardContents():
        return XSelYDoToolStrategy._clipboardStrartegy.getClipboardContents()

    @staticmethod
    def copyToClipboard(string):
        return XSelYDoToolStrategy._clipboardStrartegy.copyToClipboard(string)

    @staticmethod
    def pasteFromClipboard():
        XSelYDoToolStrategy._keyStrategy.keyPress(KEY_L_CTRL)
        XSelYDoToolStrategy._keyStrategy.keyPress(KEY_V)
        XSelYDoToolStrategy._keyStrategy.keyRelease(KEY_V)
        XSelYDoToolStrategy._keyStrategy.keyRelease(KEY_L_CTRL)
        sleep(XSelYDoToolStrategy._timeout)

    @staticmethod
    def switchLocale():
        XSelYDoToolStrategy._keyStrategy.keyPress(KEY_CAPS)
        XSelYDoToolStrategy._keyStrategy.keyRelease(KEY_CAPS)

def main():
    _strategy = XSelYDoToolStrategy()
    
    buf = _strategy.getSelectionBuffer()
    logger.debug('SelectionBuffer: "%s"', buf)
    if (not buf):
        return 0
    backup = _strategy.getClipboardContents()    
    logger.debug('Backup clipboard: "%s"', backup)
    fixed = fixLayout(buf)
    logger.debug('Fixed string: "%s"', fixed)
    _strategy.copyToClipboard(fixed)
    logger.debug('Successfully copied fixed text to clipboard')
    sleep(_strategy._timeout)
    _strategy.pasteFromClipboard()
    logger.debug('Successfully paste fixed text from clipboard')
    if (backup):
        _strategy.copyToClipboard(backup)
        logger.debug('Successfully restored clipboard contents')
    _strategy.switchLocale()
    logger.debug('Successfully switched the locale')
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except RuntimeError as e:
        sys.exit(1)


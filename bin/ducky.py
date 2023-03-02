import struct
import getopt
import sys
from time import sleep


DEFAULT_DELAY = 0.01

KEYS = {'A': 4, 'B': 5, 'C': 6, 'D': 7, 'E': 8, 'F': 9, 'G': 10, 'H': 11, 'I': 12, 'J': 13, 'K': 14, 'L': 15, 'M': 16, 'N': 17, 'O': 18, 'P': 19, 'Q': 20, 'R': 21, 'S': 22, 'T': 23, 'U': 24, 'V': 25, 'W': 26, 'X': 27, 'Y': 28, 'Z': 29, '1': 30, '2': 31, '3': 32, '4': 33, '5': 34, '6': 35, '7': 36, '8': 37, '9': 38, '0': 39, 'ENTER': 40, 'RETURN': 40, 'ESCAPE': 41, 'ESC': 41, 'BACKSPACE': 42, 'TAB': 43, 'SPACE': 44, 'SPACEBAR': 44, ' ': 44, 'MINUS': 45, 'EQUAL': 46, 'EQUALS': 46, 'LEFT_BRACE': 47, 'LEFT_BRACKET': 47, 'RIGHT_BRACE': 48, 'RIGHT_BRACKET': 48, 'BACKSLASH': 49, 'NUMBER': 50, 'POUND': 50, 'SEMICOLON': 51, 'QUOTE': 52, 'GRAVE': 53, 'COMMA': 54, 'PERIOD': 55, 'FORWARD_SLASH': 56, 'SLASH': 56, 'CAPS_LOCK': 57, 'F1': 58, 'F2': 59, 'F3': 60, 'F4': 61, 'F5': 62, 'F6': 63, 'F7': 64, 'F8': 65, 'F9': 66, 'F10': 67, 'F11': 68, 'F12': 69, 'PRINT_SCREEN': 70, 'SCROLL_LOCK': 71, 'PAUSE': 72, 'INSERT': 73, 'HOME': 74, 'PAGE_UP': 75, 'DELETE': 76, 'END': 77, 'PAGE_DOWN': 78, 'RIGHT_ARROW': 79, 'LEFT_ARROW': 80, 'DOWN_ARROW': 81, 'UP_ARROW': 82, 'KEYPAD_NUMLOCK': 83, 'KEYPAD_FORWARD_SLASH': 84, 'KEYPAD_ASTERISK': 85, 'KEYPAD_MINUS': 86, 'KEYPAD_PLUS': 87, 'KEYPAD_ENTER': 88, 'KEYPAD_ONE': 89, 'KEYPAD_TWO': 90, 'KEYPAD_THREE': 91, 'KEYPAD_FOUR': 92, 'KEYPAD_FIVE': 93, 'KEYPAD_SIX': 94, 'KEYPAD_SEVEN': 95, 'KEYPAD_EIGHT': 96, 'KEYPAD_NINE': 97, 'KEYPAD_ZERO': 98, 'KEYPAD_PERIOD': 99, 'KEYPAD_BACKSLASH': 100, 'APPLICATION': 101, 'POWER': 102, 'KEYPAD_EQUALS': 103, 'F13': 104, 'F14': 105, 'F15': 106, 'F16': 107, 'F17': 108, 'F18': 109, 'F19': 110, 'F20': 111, 'F21': 112, 'F22': 113, 'F23': 114, 'F24': 115, 'OPEN': 116, 'HELP': 117, 'PROPS': 118, 'FRONT': 119, 'STOP': 120, 'AGAIN': 121, 'UNDO': 122, 'CUT': 123, 'COPY': 124, 'PASTE': 125, 'FIND': 126, 'MUTE': 127, 'VOLUMEUP': 128, 'VOLUMEDOWN': 129, 'KPLEFTPAREN': 182, 'KPRIGHTPAREN': 183, 'CTRL': 224, 'CONTROL': 224, 'LEFT_CONTROL': 224, 'SHIFT': 225, 'LEFT_SHIFT': 225, 'ALT': 226, 'LEFT_ALT': 226, 'OPTION': 226, 'COMMAND': 227, 'GUI': 227, 'LEFT_GUI': 227, 'WINDOWS': 227, 'RIGHT_CONTROL': 228, 'RIGHT_SHIFT': 229, 'RIGHT_ALT': 230, 'RIGHT_GUI': 231, 'MEDIAPLAYPAUSE': 232, 'MEDIASTOPCD': 233, 'MEDIAPREVIOUSSONG': 234, 'MEDIANEXTSONG': 235, 'MEDIAEJECTCD': 236, 'MEDIAVOLUMEUP': 237, 'MEDIAVOLUMEDOWN': 238, 'MEDIAMUTE': 239, 'MEDIAWWW': 240, 'MEDIABACK': 241, 'MEDIAFORWARD': 242, 'MEDIASTOP': 243, 'MEDIAFIND': 244, 'MEDIASCROLLUP': 245, 'MEDIASCROLLDOWN': 246, 'MEDIAEDIT': 247, 'MEDIASLEEP': 248, 'MEDIACOFFEE': 249, 'MEDIAREFRESH': 250, 'MEDIACALC': 251, '-': 45, '_': -45, '=': 46, '+': -46, '[': 47, '{': -47, ']': 48, '}': -48, '\\': 49, '|': -49, ';': 51, ':': -51, "'": 52, '"': -52, '`': 53, '~': -53, ',': 54, '<': -54, '.': 55, '>': -55, '/': 56, '?': -56, '!': -30, '@': -31, '#': -32, '$': -33, '%': -34, '^': -35, '&': -36, '*': -37, '(': -38, ')': -39}
MODS = {'CTRL': 1, 'LEFT_CTRL': 1, 'RIGHT_CTRL': 16, 'SHIFT': 2, 'LEFT_SHIFT': 2, 'RIGHT_SHIFT': 32, 'ALT': 4, 'LEFT_ALT': 4, 'RIGHT_ALT': 64, 'GUI': 8, 'META': 8, 'LEFT_META': 8, 'RIGHT_META': 128}

def usage():
    print("  ___  _   _  ___ _  ____   __  ___ _  _    _ ___ ___ _____ ___  ___ ")
    print(" |   \\| | | |/ __| |/ /\\ \\ / / |_ _| \\| |_ | | __/ __|_   _/ _ \\| _ \\")
    print(" | |) | |_| | (__| ' <  \\ V /   | || .` | || | _| (__  | || (_) |   /")
    print(" |___/ \\___/ \\___|_|\\_\\  |_|   |___|_|\\_|\\__/|___\\___| |_| \\___/|_|_\\")
    print("__________________________________________________________by fossfrog")
    print(f'\nUSAGE: {sys.argv[0]} [OPTION] [FILE/TEXT]\n\t-h\tHelp\n\t-f\tDucky_Script\n\t-t\tText\n')
    # sys.exit()

def send_key(key, mod=0):
    report = struct.pack('8B', mod, 0, 0, key, 0, 0, 0, 0)
    with open('/dev/hidg0', 'wb') as fd:
        fd.write(report)
        fd.write(b'\x00\x00\x00\x00\x00\x00\x00\x00')
    sleep(DEFAULT_DELAY)

def f_word(word, line):
        if(word == 'REM' or word == '#'):
          return 'COMMENT'

        elif(word == 'STRING'):
            for i in line.strip()[7:]:
                if i.isupper():
                    send_key(KEYS[i.upper()], 2)
                else:
                    if i == '\t': i = 'TAB'
                    send_key(KEYS[i.upper()]) if KEYS[i.upper()] > 0 else send_key(abs(KEYS[i.upper()]), 2)
                

        elif(word == 'DELAY'):
            sleep(DEFAULT_DELAY/1000) if len(line) == 5 else sleep(int(line[6:])/1000)

        elif(word in MODS):
            tmp = line.strip().split()
            mod = 0
            for i in tmp[:-1]:
                mod += MODS[i]
            send_key(KEYS[tmp[-1].upper()], mod)

        else:
            send_key(KEYS[line.strip().upper()])

def inject_raw(txt):
    duck = txt.split('\n')

    for line in range(len(duck)):
        if duck[line]:
            try:
                f_word(duck[line].split()[0], duck[line])
            except:
                pass

def inject_file(inp_file):
    with open(inp_file, 'r') as ducky:
        duck = ducky.read()
    inject_raw(duck)


if __name__ == '__main__':
    argv = sys.argv[1:]
    ducky = txt = ''
    try:
        opts, args = getopt.getopt(argv, 'hf:t:')
        for opt, arg in opts:
            if opt in ['-h']:
                usage()
            elif opt in ['-f']:
                ducky = arg
            elif opt in ['-t']:
                txt = arg
    except getopt.GetoptError as err:
        usage()
    if ducky:
        inject_file(ducky)
    elif txt:
        inject_raw(txt)

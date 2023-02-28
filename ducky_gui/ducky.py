import struct
import getopt
import sys
from keys import KEYS, MODS
from time import sleep


DEFAULT_DELAY = 0.01

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

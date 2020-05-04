#!/usr/bin/env python3

import getopt, sys

def usage():
    print("""
Usage : font.py [OPTIONS] <FontFile>

Options :
-o  Output file
-s  Start offset
-l  Limit tiles (number of tiles to export)
""")
    sys.exit(2)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"o:s:l:h",["output", "start", "limit", "help"])
    except getopt.GetoptError as error:
        print(error)
        usage()

    if len(args) != 1:
        usage()

    start = 0
    limit = -1
    out = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-s", "--start"):
            start = int(arg)
        elif opt in ("-l", "--limit"):
            limit = int(arg)
        elif opt in ("-o", "--output"):
            out = arg
        else:
            usage()

    if not out:
        usage()

    reader = open(args[0], "rb")
    writer = open(out, "wb")
    if start > 0:
        reader.seek(start*8)
    while True:
        if limit == 0:
            break
        fontChar = reader.read(8)
        if not fontChar or len(fontChar) < 8:
            break
        
        tileChar = b''
        for y in range(0, 8):
            tileCharCode = 0
            for x in range(0, 8):
                tileCharCode <<= 1
                if (fontChar[y]>>(7-x))&1:
                    tileCharCode |= 1
            tileChar += bytes([tileCharCode&0xFF, tileCharCode&0xFF])
        writer.write(tileChar)
        limit -= 1

    reader.close()
    writer.close()

if __name__ == "__main__":
    main()
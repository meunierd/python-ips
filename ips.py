#!/usr/bin/env python

import struct
import getopt, sys

def apply(patchname, filename):
"""
Applies the IPS patch patchname to the file filename.
"""
    patchfile = file(patchname, 'r')
    infile = file(filename, 'r+b')

    if patchfile.read(5)  != 'PATCH':
        print "Error. No IPS header."
        return False
    print "PATCH... OK!"
    
    while True:
        # Read Record 
        r = patchfile.read(3)

        if r == 'EOF':
            print "Patch complete."
            break 

        # Unpack 3-byte pointers.
        offset = struct.unpack_from('>I', '\x00' + r)[0]
        # Read size of data chunk
        r = patchfile.read(2)
        size = struct.unpack_from('>I', '\x00\x00' + r)[0]

        if size == 0: # RLE Record
            r = patchfile.read(2)
            rle_size = struct.unpack_from('>I', '\x00\x00' + r)[0]
            data = patchfile.read(1) * rle_size
        else:
            # Read Data
            data = patchfile.read(size)

        # Write to file
        infile.seek(offset)
        infile.write(data)
        
    # Cleanup
    infile.close()
    patchfile.close()
    
    return True

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:p:")
    except getopt.GetoptError, err:
        print err
        sys.exit(2)
    for o, a in opts:
        if o == "-f": topatch = a
        elif o == "-p": ipspatch = a

    apply(ipspatch, topatch)

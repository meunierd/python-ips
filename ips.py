#!/usr/bin/env python

"""
Copyright (C) 2011 by Devon Meunier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import struct
import getopt, sys

usage = \
"""usage: %s -f [file] -p [patch.ips]
""" % sys.argv[0]

def apply(patchname, filename):
    """
        Applies the IPS patch patchname to the file filename.
    """
    patchfile = file(patchname, 'r')
    infile = file(filename, 'r+b')

    if patchfile.read(5)  != 'PATCH':
        sys.stderr.write("Error. No IPS header.\n")
        sys.exit(2)
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

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:p:")
    except getopt.GetoptError, err:
        sys.stderr.write("%s\n" % str(err))
        sys.stderr.write(usage); sys.exit(2)
    if len(opts) == 0:
        sys.stderr.write(usage); sys.exit(2)
    for o, a in opts:
        if o == "-f": topatch = a
        elif o == "-p": ipspatch = a

    apply(ipspatch, topatch)

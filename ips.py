#!/usr/bin/env python

"""
Copyright (C) 2011 by Devon Meunier <devon.meunier@utoronto.ca>

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

import getopt, sys, shutil, struct, logging
from os import path

usage = \
"""usage: %s [-l] [-b] -f TARGET -p PATCH.ips [--fake-header]
""" % sys.argv[0]

def apply(patchname, filename, fake = False):
    """
        Applies the IPS patch patchname to the file filename.
    """
    logging.info('Applying to "%s"' % filename)
    logging.info("Record   | Size | Range Patched     | RLE")
    logging.info("---------+------+-------------------+----")
    patchfile = file(patchname, 'rb')
    infile = file(filename, 'r+b')

    if patchfile.read(5)  != 'PATCH':
        sys.stderr.write("Error. No IPS header.\n")
        sys.exit(2)
    
    while True:
        pt = patchfile.tell()
        rle_size = None

        # Read Record 
        r = patchfile.read(3)

        if r == 'EOF' and path.getsize(patchname) == patchfile.tell():
            print 'Patching "%s" successful.' % filename
            break 

        # Unpack 3-byte pointers.
        offset = struct.unpack_from('>I', '\x00' + r)[0]
        # Read size of data chunk
        r = patchfile.read(2)
        if  len(r) == 0: break
        size = struct.unpack_from('>I', '\x00\x00' + r)[0]

        if size == 0: # RLE Record
            r = patchfile.read(2)
            rle_size = struct.unpack_from('>I', '\x00\x00' + r)[0]
            data = patchfile.read(1) * rle_size
        else:
            # Read Data
            data = patchfile.read(size)

        # Write to file
        if fake: infile.seek(offset - 512)
        else: infile.seek(offset)
        infile.write(data)
       
        # Write to log
        rle = "No"
        if rle_size: size = rle_size; rle = "Yes"
        logging.info("%08X | %04X | %08X-%08X | %s"
            % (pt, size, offset, offset + size, rle))
    # Cleanup
    infile.close()
    patchfile.close()

if __name__ == "__main__":
    LOG, BACKUP, FAKEHEADER = False, False, False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:p:lb", ['fake-header'])
    except getopt.GetoptError, err:
        sys.stderr.write("%s\n" % err)
        sys.stderr.write(usage); sys.exit(2)
    if len(opts) == 0:
        sys.stderr.write(usage); sys.exit(2)
    for o, a in opts:
        if o == "-f": topatch = a
        elif o == "-p": ipspatch = a
        elif o == "-l": LOG = True
        elif o == "-b": BACKUP = True
        elif o == "--fake-header": FAKEHEADER = True

    if BACKUP: shutil.copyfile(topatch, topatch + ".bak")
    if LOG: logging.basicConfig(filename = ipspatch[:-3] + 'log', level=logging.INFO)

    apply(ipspatch, topatch, FAKEHEADER)

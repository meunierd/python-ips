#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
...is a simple ips patching utility and has been tested to work on python2.7, 
python3, and IronPython 2.7. 
The latest version of this script can always be downloaded from
[Bitbucket](https://bitbucket.org/meunierd/python-ips/raw/tip/ips.py).
"""

"""
## Usage

Run by typing the following:

python ips.py -f target -p patch [-b] [-l] [--fake-header]

### Options

*-b:* creates a backup of the target.

*-l*: creates a log in the patch directory.

*--fake-header:* corrects for patches expecting a 512-byte header.
"""

"""
## License

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

import getopt
import sys
import shutil
import struct
import logging
import os


### API Documentation
def apply(patchname, filename, **kwargs):
    """
    ###apply:
    
    *patchname:* the path to the ips patch.

    *filename:* the patch the ips file.

    ***kwargs:* accepted keys; `logging` enables logging, `backup` creates a 
    backup of the target, `fake` spoof a 512-byte header.
    """
    if 'backup' in kwargs:
        shutil.copyfile(filename, filename + ".bak")

    if 'logging' in kwargs:
        logging.basicConfig(filename=patchname[:-3] + 'log', level=logging.INFO)
    
    logging.info('Applying to "%s"' % filename)
    logging.info("Record   | Size | Range Patched     | RLE")
    logging.info("---------+------+-------------------+----")

    patchfile = open(patchname, 'rb')
    infile = open(filename, 'r+b')

    header = patchfile.read(5)
    if header  != b'PATCH':
        sys.stderr.write("Error. No IPS header. READ: %s\n" % header)
        sys.exit(2)
    
    while True:
        pt = patchfile.tell()
        rle_size = None

        # Read Record 
        r = patchfile.read(3)

        # Are we at the end?
        if r == b'EOF' and os.path.getsize(patchname) == patchfile.tell():
            sys.stdout.write('Patching "%s" successful.\n' % filename)
            break 

        # Unpack 3-byte pointers.
        offset = struct.unpack_from('>I', b'\x00' + r)[0]
        # Read size of data chunk
        r = patchfile.read(2)
        if  len(r) == 0: break
        size = struct.unpack_from('>I', b'\x00\x00' + r)[0]

        if size == 0: # RLE Record
            r = patchfile.read(2)
            rle_size = struct.unpack_from('>I', b'\x00\x00' + r)[0]
            data = patchfile.read(1) * rle_size
        else:
            # Read Data
            data = patchfile.read(size)

        # Write to file
        if 'fake' in kwargs and kwargs['fake']: infile.seek(offset - 512)
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

def main():
    """
    **main:** process args and run.
    """
    usage = "usage: %s [-l] [-b] -f TARGET -p PATCH.ips [--fake-header]\n" % sys.argv[0]

    kwargs = {}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:p:lb", ['fake-header'])
    except getopt.GetoptError:
        sys.stderr.write(usage)
        sys.exit(2)
    if len(opts) == 0:
        sys.stderr.write(usage)
        sys.exit(2)
    for o, a in opts:
        if o == "-f":
            topatch = a
        elif o == "-p":
            ips = a
        elif o == "-l":
            kwargs['logging'] = True
        elif o == "-b":
            kwargs['backup'] = True 
        elif o == "--fake-header":
            kwargs['fake'] = True 

    apply(ips, topatch, **kwargs)

if __name__ == "__main__":
    main()

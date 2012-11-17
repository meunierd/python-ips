#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import sys
import shutil
import struct
import logging
import os


### API Documentation
def apply(patchname, filename, **kwargs):
    if 'backup' in kwargs:
        shutil.copyfile(filename, filename + ".bak")

    if 'logging' in kwargs:
        logging.basicConfig(filename=patchname[:-3] + 'log',
                            level=logging.INFO)

    logging.info('Applying to "%s"' % filename)
    logging.info("Record   | Size | Range Patched     | RLE")
    logging.info("---------+------+-------------------+----")

    patchfile = open(patchname, 'rb')
    infile = open(filename, 'r+b')

    header = patchfile.read(5)
    if header != b'PATCH':
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
        if len(r) == 0:
            break
        size = struct.unpack_from('>I', b'\x00\x00' + r)[0]

        if size == 0:  # RLE Record
            r = patchfile.read(2)
            rle_size = struct.unpack_from('>I', b'\x00\x00' + r)[0]
            data = patchfile.read(1) * rle_size
        else:
            # Read Data
            data = patchfile.read(size)

        # Write to file
        if 'fake' in kwargs and kwargs['fake']:
            infile.seek(offset - 512)
        else:
            infile.seek(offset)
        infile.write(data)
        # Write to log
        rle = "No"
        if rle_size:
            size = rle_size
            rle = "Yes"
        logging.info("%08X | %04X | %08X-%08X | %s"
                     % (pt, size, offset, offset + size, rle))

    # Cleanup
    infile.close()
    patchfile.close()


def main():
    kwargs = {}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:p:lb", ['fake-header'])
    except getopt.GetoptError:
        sys.stderr.write("usage")
        sys.exit(2)
    if len(opts) == 0:
        sys.stderr.write("usage")
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

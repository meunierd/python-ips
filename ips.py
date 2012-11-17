#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Usage:
    ips [options] PATCH TARGET

Options:
    -h --help         Display this message.
    -v --verbose      View logging output
    -b --backup       Create a backup of target named TARGET.bak
    -f --fake-header  Fake a SNES header
"""


import sys
import shutil
import struct
import logging
import os

from docopt import docopt


def apply(patchname, filename, **kwargs):
    if kwargs["--backup"]:
        shutil.copyfile(filename, filename + ".bak")

    if kwargs["--verbose"]:
        logging.basicConfig(filename=filename + '.log',
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
        if kwargs['--fake-header']:
            if offset - 512 < 0:
                sys.stdout.write("Skipping record.\n")
                continue
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
    kwargs = docopt(__doc__)
    apply(kwargs['PATCH'], kwargs['TARGET'], **kwargs)

if __name__ == "__main__":
    main()

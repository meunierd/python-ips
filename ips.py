#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Usage:
    python-ips [options] PATCH TARGET

Options:
    --fake-header  Fake a SNES header.
    -h --help      Display this message.
    -b --backup    Create a backup of target named TARGET.bak
"""


import shutil
import struct

from os.path import getsize
from docopt import docopt


def unpack_int(string):
    """Read an n-byte big-endian integer from a byte string."""
    (ret,) = struct.unpack_from('>I', b'\x00' * (4 - len(string)) + string)
    return ret

def apply(patchpath, filepath, fake_header=False):
    patch_size = getsize(patchpath)
    patchfile = open(patchpath, 'rb')
    target = open(filepath, 'r+b')

    if patchfile.read(5) != b'PATCH':
        raise Exception('Invalid patch header.')

    # Read First Record
    r = patchfile.read(3)
    while patchfile.tell() not in [patch_size, patch_size - 3]:
        # Unpack 3-byte pointers.
        offset = unpack_int(r)
        if fake_header:
            offset -= 512
        # Read size of data chunk
        r = patchfile.read(2)
        size = unpack_int(r)

        if size == 0:  # RLE Record
            r = patchfile.read(2)
            rle_size = unpack_int(r)
            data = patchfile.read(1) * rle_size
        else:
            data = patchfile.read(size)

        if offset >= 0:
            # Write to file
            target.seek(offset)
            target.write(data)
        # Read Next Record
        r = patchfile.read(3)

    if patch_size - 3 == patchfile.tell():
        trim_size = unpack_int(patchfile.read(3))
        target.truncate(trim_size)

    # Cleanup
    target.close()
    patchfile.close()


def main():
    kwargs = docopt(__doc__)
    if kwargs['--backup']:
        shutil.copyfile(kwargs['TARGET'], kwargs['TARGET'] + ".bak")
    apply(kwargs['PATCH'], kwargs['TARGET'], kwargs['--fake-header'])

if __name__ == "__main__":
    main()

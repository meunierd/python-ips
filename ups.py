#!/usr/bin/env python

from os import path

class UPS:
    magic = "UPS1" #4-byte UPS 1.0 header
    
    def __init__(self, filea, patch, fileb = None):
        if fileb:
            self.filea = open(filea, 'rb')
            self.patch = open(patch, 'r+b')
            self.fileb = open(fileb, 'rb')
        else:
            self.target = open(filea, 'r+b')
            self.patch = open(patch, 'rb')

        if self.patch is not None:
            self.patch = open(self.patch, 'rb')

    def decode(self):
        """
            Reads and returns a variable length pointer from the patch.
        """
        offset, shift = 0, 1
        while True:
            b = ord(self.patch.read(1))
            offset = (x & 0b01111111) * shift + offset
            if b & 0b10000000: break
            shift = shift << 7
            offset = offset + shift
        return offset

    def encode(self, offset):
        while True: 
            b = offset & 0b01111111
            offset = offset >> 7
            if offset == 0:
                self.write(self.patch, b | 0b10000000)
                break
            self.write(self.patch, b)
            offset = offset - 1

    def apply(self):
        if self.patch.read(4) != self.magic: return False
        src_len = self.decode()
        tar_len = self.decode()

        # assert filesizes
         

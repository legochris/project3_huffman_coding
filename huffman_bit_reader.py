"""Bit-packing reader and writer for Huffman encoder and decoder
"""

import struct

class HuffmanBitReader:
    """HuffmanBitReader is a HuffmanBitReader(string)
    Attributes:
        file (file): a file object
        n_bits (int): the number of bits
        byte (int): the current byte
        mask (int): bit mask
    """
    def __init__(self, fname):
        """open a file with file name 'fname' for reading in binary mode
        Args:
            fname (str): file name
        """
        self.file = open(fname, 'rb')
        self.n_bits = 0
        self.byte = 0
        self.mask = 0

    def close(self):
        """closes opened file"""
        self.file.close()

    def read_str(self): # str is a string
        """ Use this method to read the header from the compressed file.
        Returns:
            str: the header line
        """
        return self.file.readline()

    def read_bit(self):
        """ reads bit.
        Use this method to read a single bit from opened file
        Returns:
            bool: False if a 0 was read, 1 otherwise
        Raises:
            Error: if the end of file is reached
        """
        if self.mask == 0:   # all bits consumed, need to read in the next byte
            self.byte = self.read_byte()
            self.mask = 1 << 7
        bit = self.byte & self.mask
        self.mask = self.mask >> 1
        if bit == 0:
            return False
        return True

    def read_byte(self):
        """Reads a 1 byte from opened file and returns as unsigned int
        You should not need to call this method

        Returns:
            int: 1 byte unsigned int
        """
        return struct.unpack('B', self.file.read(1))[0]  # 1 byte unsigned int

"""Huffman bit writer module
"""

import struct

class HuffmanBitWriter:
    """Bit-packing writer for Huffman encoder

    Attributes:
        file (file): a file object
        n_bits (int): the number of bits
        byte (int): a byte as int
    """
    def __init__(self, fname):
        """open a file with file name 'fname' for writing in binary mode
        Args:
            fname (str): a file name of the output file
        """
        self.file = open(fname, 'wb') # open a file with file name fname
        self.n_bits = 0               # Number of accumulated bits so far
        self.byte = 0                 # accumulated bits represented as byte

    def close(self):
        """ Closes the compressed file.
        Use this method to close the compressed file.
        """
        # need to pad remaining bits in byte with 0s and write them to file
        if self.n_bits > 0:
            self.byte = self.byte << (7-self.n_bits)
            self.file.write(struct.pack('B', self.byte))
        self.file.close()

    def write_str(self, string):
        """Writes a string as a text in the file.
        Use this method to write the header to the compressed file.

        Args:
            string (str): a string
        """
        self.file.write(string.encode('utf-8'))

    def write_code(self, code):
        """Write code as bits
        Use this method to write individual 0 and 1 bits to the compressed file
        Args:
            code (str): a string of '0's and '1's
        """
        for bit in code:
            if bit == '1':
                self.byte += 1
            if self.n_bits == 7:
                self.file.write(struct.pack('B', self.byte))
                self.byte = 0
                self.n_bits = 0
            else:
                self.byte = self.byte << 1
                self.n_bits += 1

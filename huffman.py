"""Huffman Node Implementation for Project 3
Course: CPE202
Quarter: Spring 2020
Author: Chris Linthacum
"""

class HuffmanNode:
    """ Node object for Huffman encoding
        Fields:
            char
            freq
            left
            right
    """

    def __init__(self, frequency, char=None, left=None, right=None):
        """ Initialization implementation of object"""

        self.freq = frequency
        self.char = char
        self.left = left
        self.right = right

    def __eq__(self, other):
        """ Compare the object to an other"""

        return self.freq == other.freq and self.char == other.char and \
            self.left == other.left and self.right == other.right

    def __repr__(self):
        """ How the node represents itself"""
        freq = repr(self.freq)
        char = repr(self.char)
        left = repr(self.left)
        right = repr(self.right)

        output = 'Huffman Node(freq: {}, char: {}, left: {}, right: ' \
                 '{})'.format(freq, char, left, right)

        return output

    def __lt__(self, other):
        """Implementing this function let you compare two HuffmanNode objects
         with < in your program
        Args:
            other (HuffmanNode): other HuffmanNode object to be compared with
                                 self
        Returns:
            True if self <= other, else return False
        """
        if self.freq < other.freq:
            return True
        if other.freq < self.freq:
            return False

        return ord(self.char) < ord(other.char)


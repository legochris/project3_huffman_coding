"""Test Method Implementations for Project 3
Course: CPE202
Quarter: Spring 2020
Author: Chris Linthacum
"""

import unittest as ut
import filecmp

from min_pq import MinPQ

from huffman_coding import cnt_freq
from huffman_coding import create_huff_tree
from huffman_coding import create_code
from huffman_coding import create_header
from huffman_coding import huffman_encode
from huffman_coding import huffman_decode

from huffman import HuffmanNode

class TestHuffmanNode(ut.TestCase):
    """ Tests the HuffmanNode class"""

    def test_eq(self):
        """ Tests whether two nodes are equal"""
        node1 = HuffmanNode(4)
        node2 = HuffmanNode(1)
        node3 = HuffmanNode(4)

        self.assertFalse(node1 == node2)
        self.assertTrue(node1 == node3)

    def test_repr(self):
        """ Tests how the class represents itself"""
        node1 = HuffmanNode(1)
        node2 = HuffmanNode(4)
        node3 = HuffmanNode(12, None, node1, node2)
        expected = "Huffman Node(freq: 12, char: None, left: " \
                   "Huffman Node(freq: 1, char: None, left: None, right: " \
                   "None), right: Huffman Node(freq: 4, char: None, " \
                   "left: None, right: None))"
        self.assertEqual(expected, repr(node3))

class TestList(ut.TestCase):
    def test_cnt_freq(self):
        freqlist = cnt_freq("file1.txt")
        anslist = [0]*256
        anslist[97:104] = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist[97:104])

    def test_create_huff_tree(self):
        freqlist = cnt_freq("file1.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 33)
        self.assertEqual(hufftree.left.char, 'd')
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 'd')
        right = hufftree.right
        self.assertEqual(right.freq, 17)
        self.assertEqual(ord(right.char), 0)

    def test_create_code(self):
        freqlist = cnt_freq("file1.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        print('d', codes[ord('d')])
        print('a', codes[ord('a')])
        print('f', codes[ord('f')])
        self.assertEqual(codes[ord('d')], '0')
        self.assertEqual(codes[ord('a')], '11111')
        self.assertEqual(codes[ord('f')], '1110')

    def test_create_code2(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        print('g', codes[ord('g')])
        print('o', codes[ord('o')])
        print(' ', codes[ord(' ')])
        self.assertEqual(codes[ord('g')], '00')
        self.assertEqual(codes[ord('o')], '01')
        self.assertEqual(codes[ord(' ')], '101')

    def test_create_code3(self):
        freqlist = cnt_freq("file3.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        print('s', codes[ord('s')])
        print('t', codes[ord('t')])
        print('a', codes[ord('a')])
        self.assertEqual(codes[ord('s')], '111')
        self.assertEqual(codes[ord('t')], '00')
        self.assertEqual(codes[ord('a')], '010')

    def test_create_header(self):
        """ Tests the create header function"""
        freq_list = cnt_freq("test_letters.txt")
        expected_header = "0 1 97 3 98 4 99 2"
        self.assertEqual(expected_header, create_header(freq_list))

    def test_01_encodefile(self):
        huffman_encode("file1.txt", "encodetest1.txt")
        # capture errors by running 'filecmp' on your encoded file
        # with a *known* solution file
        self.assertTrue(filecmp.cmp("encodetest1.txt", "file1_soln.txt"))

    def test_02_encodefile(self):
        huffman_encode("file2.txt", "encodetest2.txt")
        # capture errors by running 'filecmp' on your encoded file
        # with a *known* solution file
        self.assertTrue(filecmp.cmp("encodetest2.txt", "file2_soln.txt"))

    def test_03_encodefile(self):
        huffman_encode("file3.txt", "encodetest3.txt")
        # capture errors by running 'filecmp' on your encoded file
        # with a *known* solution file
        self.assertTrue(filecmp.cmp("encodetest3.txt", "file3_soln.txt"))

    def test_create_huff_tree(self):
        """ Tests behavior of size 0 PQ"""
        self.assertIsNone(create_huff_tree([]))

    def test_01_decodefile(self):
        huffman_decode("file1_soln_compressed.txt", "decodetest1.txt")
        # capture errors by running 'filecmp' on your encoded file
        # with a *known* solution file
        self.assertTrue(filecmp.cmp("decodetest1.txt", "file1.txt"))

    def test_02_decodefile(self):
        huffman_decode("file2_soln_compressed.txt", "decodetest2.txt")
        # capture errors by running 'filecmp' on your encoded file
        # with a *known* solution file
        self.assertTrue(filecmp.cmp("decodetest2.txt", "file2.txt"))

    def test_03_decodefile(self):
        huffman_decode("file3_soln_compressed.txt", "decodetest3.txt")
        # capture errors by running 'filecmp' on your encoded file
        # with a *known* solution file
        self.assertTrue(filecmp.cmp("decodetest3.txt", "file3.txt"))

class ClassUseCaseTests(ut.TestCase):
    """ Test cases outlined in the lab manual"""

    def test_use_case_one(self):
        """ Implementation of use case 1 as outlined in lab instructions"""
        pq_test = MinPQ()
        pq_test.insert(5)
        pq_test.insert(3)
        self.assertTrue(pq_test.capacity == 2)
        pq_test.insert(6)
        self.assertEqual(3, pq_test.size())
        self.assertEqual(3, pq_test.min())
        self.assertEqual(3, pq_test.del_min())
        self.assertEqual(5, pq_test.del_min())
        self.assertEqual(6, pq_test.del_min())
        self.assertEqual(0, pq_test.size())
        self.assertTrue(pq_test.is_empty())
        self.assertEqual(2, pq_test.capacity)

    def test_use_case_two(self):
        """ Implementation of use case 2 as outlined in lab instructions"""
        pq_test = MinPQ([5, 4, 3, 2, 1])
        self.assertEqual(5, pq_test.size())
        self.assertEqual(5, pq_test.capacity)
        self.assertEqual(pq_test.num_items, pq_test.capacity)
        self.assertTrue(pq_test.arr == [1, 2, 3, 5, 4])
        self.assertEqual(1, pq_test.min())
        self.assertEqual(1, pq_test.del_min())
        self.assertEqual(2, pq_test.del_min())
        self.assertFalse(pq_test.is_empty())
        self.assertEqual(3, pq_test.del_min())
        self.assertEqual(4, pq_test.del_min())
        self.assertEqual(5, pq_test.del_min())
        self.assertEqual(2, pq_test.capacity)
        self.assertEqual(0, pq_test.size())
        self.assertTrue(pq_test.is_empty())

class MinPQSelfTests(ut.TestCase):
    """ Test cases to montitor the functionality of Min PQ"""

    def test_full_functionality(self):
        """ Tests the bulk functionality of the MinPQ class"""
        pq_test = MinPQ()
        pq_test.insert(6)
        self.assertEqual(2, pq_test.capacity)
        self.assertEqual(pq_test.size(), pq_test.num_items)
        pq_test.insert(7)
        self.assertEqual([6, 7], pq_test.arr)
        pq_test.insert(2)
        self.assertEqual(3, pq_test.size())
        self.assertEqual([2, 7, 6, None], pq_test.arr)
        self.assertFalse(pq_test.is_empty())
        self.assertEqual(2, pq_test.del_min())
        self.assertEqual(6, pq_test.del_min())
        self.assertEqual(7, pq_test.del_min())
        self.assertTrue(pq_test.is_empty())

    def test_repr(self):
        """ Tests the repr function"""
        pq_test = MinPQ()
        pq_test.insert(3)
        pq_test.insert(4)
        expected = '[3, 4]'
        self.assertEqual(expected, repr(pq_test))


if __name__ == '__main__':
    ut.main()

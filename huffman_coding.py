"""Huffman Encoding Implementation for Project 3
Course: CPE202
Quarter: Spring 2020
Author: Chris Linthacum
"""

from huffman import HuffmanNode
from min_pq import MinPQ
from huffman_bit_writer import HuffmanBitWriter
from huffman_bit_reader import HuffmanBitReader

def cnt_freq(filename):
    """ Opens text file and counts the frequency of occurrences of all
        characters within the file.
        Args:
            filename(str): the name of file to be opened
        Returns:
            arr: 256 item list with count of every character occurrences
    """

    file = open(filename, 'r')
    out_list = [0] * 256

    for line in file:
        for char in line:
            ascii_val = ord(char)
            out_list[ascii_val] += 1

    file.close()

    out_list[0] = 1

    return out_list


def create_huff_tree(list_of_freqs):
    """ Create a Huffman Tree from list of character frequencies
        Args:
            list_of_freqs(list): list with length of 256 characters
        Returns:
            MinPQ: the root node of the Min Priority Queue constructed from
                   the Huffman Nodes
    """

    priority_queue_list = []
    for each in range(len(list_of_freqs)):
        if list_of_freqs[each] > 0:
            char = chr(each)
            freq = list_of_freqs[each]
            node = HuffmanNode(freq, char)
            priority_queue_list.append(node)

    priority_queue = MinPQ(priority_queue_list)

    if priority_queue.size() == 0:
        return None

    while priority_queue.size() > 1:
        # Retrieves the two smallest occurring Nodes from the queue
        node_1 = priority_queue.del_min()
        node_2 = priority_queue.del_min()

        # Determine the representation of the min chr representation
        min_chr = min(node_1.char, node_2.char)

        # Sum the different frequencies, create new Node, and add to queue
        sum_freq = node_1.freq + node_2.freq
        new_node = HuffmanNode(sum_freq, min_chr, node_1, node_2)
        priority_queue.insert(new_node)

    return priority_queue.del_min()

def create_code(root_node):
    """ Creates Huffman code for a given tree representation
        Args:
            root_node(HuffmanNode): the root of the tree being converted to
                                    code
        Returns:
            list: list of 256 strings representing the code for each char
    """

    out_list = [''] * 256
    current_path = ''
    create_code_helper(root_node, out_list, current_path)

    return out_list


def create_code_helper(root_node, out_list, current_path):
    """ Recursive helper function for creating Huffman Code
        Args:
            root_node(HuffmanNode): the root node being traversed
            out_list(list): list of code outputs
            current_path(str): the current HuffmanCode for the current path
                               through the tree
        Returns:
            None
    """

    if root_node.left is not None:
        current_path_left = current_path + '0'
        current_path_right = current_path + '1'
        create_code_helper(root_node.left, out_list, current_path_left)
        create_code_helper(root_node.right, out_list, current_path_right)
    else:
        out_list[ord(root_node.char)] = current_path

def huffman_encode(in_file, out_file):
    """ Reads a text input file and writes to an output file the encoded
        version
        Args:
            in_file(str): the name of file being read into
            out_file(str): the desired output name of the file
        Returns:
              None
    """

    freq_list = cnt_freq(in_file)
    hufftree = create_huff_tree(freq_list)
    codes = create_code(hufftree)
    header = create_header(freq_list)
    encoded_text = encode_text(in_file, codes)

    # Write the uncompressed output file
    file_output = open(out_file, 'w')
    file_output.write(header)
    file_output.write(' ')
    file_output.write('\n')
    file_output.write(encoded_text)
    file_output.close()

    # Write the compressed output file
    compressed_filename = out_file[:-4] + '_compressed.txt'
    comp_file = HuffmanBitWriter(compressed_filename)
    encoded_text += codes[0]
    comp_file.write_str(header)
    comp_file.write_str('\n')
    comp_file.write_code(encoded_text)
    comp_file.close()

def create_header(list_of_freqs):
    """ Creates the header for huffman_encode based off of a list of freqs
        Args:
            list_of_freqs(list): the list of freqs created by cnt_freq
        Returns:
            str: string of correct header for encoded file
    """
    out_str = ''
    for each in range(len(list_of_freqs)):
        if list_of_freqs[each] > 0:
            out_str += '{} {} '.format(each, list_of_freqs[each])

    out_str = out_str[:-1]
    return out_str

def encode_text(in_file, codes):
    """ Encode a given file from a code list
        Args:
            in_file(str): the file name of the file to be encoded
            codes(list): codes list generated by create_code function
        Returns:
            str: string of encoded file
    """
    encoded_str = ''
    file = open(in_file, 'r')
    for line in file:
        for char in line:
            encoded_str += codes[ord(char)]

    file.close()

    return encoded_str

def huffman_decode(encoded_file, decode_file):
    """ Decode the encoded file and output
        Args:
            encoded_file(str): name of the encoded file
            decode_file(str): desired name of output file
        Returns:
            None
    """

    try:
        file = open(encoded_file, 'r')
        file.close()
    except FileNotFoundError:
        raise FileNotFoundError

    encode_file = HuffmanBitReader(encoded_file)
    decoded_file = open(decode_file, 'w')
    header = str(encode_file.read_str())
    header = header[2:]
    header = header[:-3]
    freq_list = parse_header(header)
    huff_tree = create_huff_tree(freq_list)
    code = create_code(huff_tree)
    found_null = False
    out_str = ''
    node = huff_tree
    while not found_null:
        if node.left is None and node.right is None and node.char == chr(0):
            found_null = True
        else:
            if node.left is None and node.right is None:
                out_str += node.char
                node = huff_tree
            val = encode_file.read_bit()
            if not val:
                node = node.left
            if val:
                node = node.right

    decoded_file.write(out_str)
    encode_file.close()
    decoded_file.close()

def parse_header(header_string):
    """ Parse the header into a list of freqs
        Args:
            header_string(str): string of header
        Returns:
            list: list of 265 frequencies of the characters
    """

    split_header = header_string.split()
    list_of_freqs = [0] * 256

    for each in range(0, len(split_header), 2):
        ascii_char = split_header[each]
        freq = split_header[each + 1]
        list_of_freqs[int(ascii_char)] = int(freq)

    return list_of_freqs

""" Implementation of Min Heap for Lab 7
    Course: CPE202
    Quarter: Spring 2020
    Author: Chris Linthacum
"""


class MinPQ:
    """ Implementation of Minimum Priority Queue Class
        Attributes:
            capacity (int): The capacity of the queue. The default capacity is
                            2, but will be increased automatically.
            num_items(int): The number of items in the queue.This also points
                            to the position where a new item will be added.
            arr (list): an array which contains the items in the queue.
    """

    def __init__(self, arr=None):
        """ Initializes the MinPQ object
            Args:
                arr (list): If the arr is None (default), it initializes
                            capacity as 2.
        """

        if arr is None:
            self.capacity = 2
            self.arr = [None] * self.capacity
            self.num_items = 0
        else:
            self.arr = arr
            self.capacity = len(arr)
            self.num_items = len(arr)
            self.heapify()

    # # Insert __eq__ and __repr__

    def __repr__(self):
        """ How the min queue represents itself"""

        out_str = '['
        for each in self.arr:
            out_str += (repr(each))
            out_str += ', '
        out_str = out_str[:-2]
        out_str += ']'

        return out_str

    def heapify(self):
        """ Convert the array, self.arr into a min heap
        """

        idx = (self.num_items - 2) // 2
        while idx >= 0:
            self.shift_down(idx)
            idx = idx - 1

    def insert(self, item):
        """ insert an item to the queue. Before inserting an item it checks
            if the array is full. If so, it enlarges the array by doubling
            the capacity.
            Args:
                item(int): an integer value to be inserted to the min heap
        """
        self.enlarge()
        self.arr[self.num_items] = item
        self.num_items += 1
        self.shift_up(self.num_items - 1)

    def del_min(self):
        """ Pop the min valued item from the min heap
            Returns:
                any: the minimum item in the min heap; just deleted
            Raises:
                IndexError: Raises IndexError when the queue is empty
        """

        min_item = self.arr[0]
        self.arr[0] = self.arr[self.num_items - 1]
        self.arr[self.num_items - 1] = None
        self.num_items -= 1
        self.shift_down(0)
        self.shrink()
        return min_item

    def min(self):
        """ Returns the minimum item in the queue without deleting the item
            Returns:
                any: it returns the minimum item
            Raises:
                IndexError: Raises IndexError when min queue is empty
        """

        return self.arr[0]

    def is_empty(self):
        """ Checks if the queue is empty
            Returns:
                bool: True if Empty, False otherwise.
        """

        if self.num_items == 0:
            return True
        return False

    def size(self):
        """ Returns the number of items in the queue.
            Returns:
                int: returns the number of items, self.num_items
        """

        return self.num_items

    def shift_up(self, idx):
        """ Shifts up an item in the queue using tail recursion
            Args:
                idx(int): the index of the item to be shifted up in the array
        """

        if idx == 1:
            idx_parent = 0
        else:
            idx_parent = (idx - 2) // 2
        if idx_parent < 0 or self.arr[idx_parent] < self.arr[idx]:
            return
        self.arr[idx], self.arr[idx_parent] = \
            self.arr[idx_parent], self.arr[idx]
        self.shift_up(idx_parent)

    def shift_down(self, idx):
        """ Shift down an item in the list to keep the min heap order
            Args:
                idx (int): the index of the item to be shifted down in array
        """
        if idx >= self.num_items - 1:
            return

        idx_left = 2 * idx + 1
        idx_right = 2 * idx + 2

        if idx_left > self.num_items - 1:
            left_val = None
        else:
            left_val = self.arr[idx_left]
        if idx_right > self.num_items - 1:
            right_val = None
        else:
            right_val = self.arr[idx_right]

        # Find the lowest value between the two children
        if left_val is not None and right_val is not None and \
                right_val < left_val:
            idx_min = idx_right
        elif left_val is not None:
            idx_min = idx_left
        else:
            idx_min = None

        if idx_min is None or idx_min < 0 or self.arr[idx] < self.arr[idx_min]:
            return

        self.arr[idx], self.arr[idx_min] = self.arr[idx_min], self.arr[idx]

        self.shift_down(idx_min)

    def enlarge(self):
        """ Enlarges the array.
        """
        if self.num_items == self.capacity:
            new_arr = [None] * (self.capacity * 2)
            for i in range(self.num_items):
                new_arr[i] = self.arr[i]
            self.arr = new_arr
            self.capacity = self.capacity * 2

    def shrink(self):
        """ Shrinks the array.
        """

        if self.capacity > 2 and \
                (self.num_items and self.capacity >= self.num_items * 4):
            new_cap = self.capacity // 2
            new_arr = [None] * new_cap
            for i in range(self.num_items):
                new_arr[i] = self.arr[i]
            self.arr = new_arr
            self.capacity = new_cap

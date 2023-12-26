"""
Project 5: Deque
CSE 331 FS23
Authored by Gabriel Sotelo
starter.py
"""

import gc
from typing import TypeVar, List
from random import randint, shuffle
from timeit import default_timer
# COMMENT OUT THIS LINE (and `plot_speed`) if you don't want matplotlib
from matplotlib import pyplot as plt

T = TypeVar('T')
CDLLNode = type('CDLLNode')


class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            # front will get set to 0 by front_enqueue if the initial data is empty
            data = ['Start']
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = None if not data else self.size + front - 1
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[index + front] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = [f"CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#

    def __len__(self) -> int:
        """
        Returns the number of elements currently in the deque.
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Return true if the circular deque is currently empty or has no elements.
        """
        return self.size == 0

    def front_element(self) -> T:
        """
        Returns the first element in the circular deque.
        """
        return self.queue[self.front] if self.queue and \
                                         self.front is not None else None

    def back_element(self) -> T:
        """
        Returns the last element in the circular deque.
        """
        return self.queue[self.back] if self.queue and \
                                        self.back is not None else None

    def grow(self) -> None:
        Doubles the capacity of the circular deque by creating a new
        base python list with twice the capacity of the old one and
        copies the values over from the current list
        czz
        new = CircularDeque(capacity=2 * self.capacity)

        walk = self.front

        for k in range(self.size):
            new.queue[k] = self.queue[walk]
            walk = (1 + walk) % self.size

        self.front = 0
        self.capacity *= 2
        self.queue = new.queue
        self.back = self.size - 1

    def shrink(self) -> None:
        """
        Shrinks a circular deque to half its original capacity
        """
        shrunk_capacity = self.capacity // 2

        if shrunk_capacity < 4:
            return

        new = CircularDeque(capacity=shrunk_capacity)

        walk = self.front

        for k in range(self.size):
            new.queue[k] = self.queue[walk]
            walk = (1 + walk) % self.capacity  # capacity is used so that walk can extend
                                               # as far as the current queue goes

        self.front = 0
        self.queue = new.queue
        self.back = self.size - 1
        self.capacity = shrunk_capacity


    def enqueue(self, value: T, front: bool = True) -> None:
        """
        Append or prepend a value to the Circular Deque.
        :param value: The value to be added to the circular deque.
        :param front: Prepend (Add to front) if true, else append (add to end).
        """
        self.back = 0 if self.back is None else self.back
        self.front = 0 if self.front is None else self.front

        if front:
            avail = (self.back - self.size) % self.capacity

            # To ensure that self.back never changes, we start at 1 less than the
            # rear index & work our way backwards until we arrive at 1 more than avail
            for i in range(self.back - 1, avail, -1):
                self.queue[i] = self.queue[i - 1]
            self.queue[avail] = value
            self.size += 1
            self.front = avail
        else:
            avail = (self.front + self.size) % self.capacity

            for i in range(self.back - 1, avail, -1):
                self.queue[i] = self.queue[i - 1]
            self.queue[avail] = value
            self.size += 1
            self.back = avail

        if self.size >= self.capacity:
            self.grow()

    def dequeue(self, front: bool = True) -> T:
        """
        Remove the front or back item from the Circular Deque.
        :param front: If True, remove the first element else remove the last element.
        """
        if self.size == 0:
            return None

        if front:
            popped_item = self.queue[self.front]
            self.front = (1 + self.front) % self.capacity
        else:
            popped_item = self.queue[self.back]
            self.back = (self.back - 1) % self.capacity

        self.size -= 1

        if self.size <= ((1/4) * self.capacity):
            self.shrink()

        return popped_item


class CDLLNode:
    """
    Node for the CDLL
    """

    __slots__ = ['val', 'next', 'prev']

    def __init__(self, val: T, next: CDLLNode = None, prev: CDLLNode = None) -> None:
        """
        Creates a CDLL node
        :param val: value stored by the next
        :param next: the next node in the list
        :param prev: the previous node in the list
        :return: None
        """
        self.val = val
        self.next = next
        self.prev = prev

    def __eq__(self, other: CDLLNode) -> bool:
        """
        Compares two CDLLNodes by value
        :param other: The other node
        :return: true if comparison is true, else false
        """
        return self.val == other.val

    def __str__(self) -> str:
        """
        Returns a string representation of the node
        :return: string
        """
        return "<= (" + str(self.val) + ") =>"

    __repr__ = __str__


class CDLL:
    """
    A (C)ircular (D)oubly (L)inked (L)ist
    """

    __slots__ = ['head', 'size']

    def __init__(self) -> None:
        """
        Creates a CDLL
        :return: None
        """
        self.size = 0
        self.head = None

    def __len__(self) -> int:
        """
        :return: the size of the CDLL
        """
        return self.size

    def __eq__(self, other: 'CDLL') -> bool:
        """
        Compares two CDLLs by value
        :param other: the other CDLL
        :return: true if comparison is true, else false
        """
        n1: CDLLNode = self.head
        n2: CDLLNode = other.head
        for _ in range(self.size):
            if n1 != n2:
                return False
            n1, n2 = n1.next, n2.next
        return True

    def __str__(self) -> str:
        """
        :return: a string representation of the CDLL
        """
        n1: CDLLNode = self.head
        joinable: List[str] = []
        while n1 is not self.head:
            joinable.append(str(n1))
            n1 = n1.next
        return ''.join(joinable)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#

    def insert(self, val: T, front: bool = True) -> None:
        """
        Inserts a node with value `val` in the front or back of the CDLL
        :param val: the value to be inserted
        :param front: insert at the front of the CDLL if true, else pop back
        """
        new = CDLLNode(val)

        # Account for an empty CDLLCD: The head's next and previous
        # should wrap around and point to itself
        if self.size == 0:
            self.head = new
            self.head.next = self.head.prev = self.head
        else:
            tail = self.head.prev
            head = self.head

            # ---- 4 UPDATES -----
            # For tight pointer reassignment

            new.next = head  # Point the new node's next to the old_head
            new.prev = tail  # Point the new node's prev to the tail
            head.prev = new  # Point the old head's prev to the new node
            tail.next = new  # Point the tail's next to the new node

            if front:
                self.head = new  # reassign the head node

        self.size += 1

    def remove(self, front: bool = True) -> None:
        """
        Removes a node from the CDLL
        :param front: Remove from the front of the CDLL if true, else pop back
        """
        # Account for an empty CDLLCD: If empty, there's nothing to remove
        if self.size == 0:
            return

        elif self.size == 1:
            self.head = None

        # For CDLLs with 2 or more elements
        else:
            tail = self.head.prev
            head = self.head

            if front:
                tail.next = head.next
                head.next.prev = tail
                self.head = head.next
            else:
                head.prev = tail.prev
                tail.prev.next = head
        self.size -= 1


class CDLLCD:
    """
    (C)ircular (D)oubly (L)inked (L)ist (C)ircular (D)equeue
    This is essentially just an interface for the above
    """

    def __init__(self) -> None:
        """
        Initializes the CDLLCD to an empty CDLL
        :return: None
        """
        self.CDLL: CDLL = CDLL()

    def __eq__(self, other: 'CDLLCD') -> bool:
        """
        Compares two CDLLCDs by value
        :param other: the other CDLLCD
        :return: true if equal, else false
        """
        return self.CDLL == other.CDLL

    def __str__(self) -> str:
        """
        :return: string representation of the CDLLCD
        """
        return str(self.CDLL)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#
    def __len__(self) -> int:
        """
        Returns the number of elements currently in the CDLLCD
        """
        return self.CDLL.size

    def is_empty(self) -> bool:
        """
        Indicates whether the CDLLCD is currently empty
        """
        return self.CDLL.size == 0

    def front_element(self) -> T:
        """
        Returns the first element in the CDLLCD
        """
        return None if self.is_empty() else self.CDLL.head.val

    def back_element(self) -> T:
        """
        Returns the last element in the CDLLCD
        """
        return None if self.is_empty() else self.CDLL.head.prev.val

    def enqueue(self, val: T, front: bool = True) -> None:
        """
        Adds a node containing `val` to the end or beginning of the CDLLCD
        :param val: the value to be enqueued
        :param front: if true, add the node to the front of the CDLLCD, else append the node
        """
        self.CDLL.insert(val, front)

    def dequeue(self, front: bool = True) -> T:
        """
        Removes the node at the end or beginning of the CDLLCD.
        :param front: if true, remove the front node of the CDLLCD, else remove the back node
        """
        # Account for an empty CDLLCD: If empty, there's nothing to remove
        if self.is_empty():
            return None

        # Based on `front` we assign a local temp to store the value
        # of the node that we are about to delete
        if front:
            removed_value = self.CDLL.head.val
        else:
            removed_value = self.CDLL.head.prev.val

        # Then, calling remove on the base CDLL of our CDLLCD removes
        # the appropriate node according to the given `front` boolean
        self.CDLL.remove(front)

        # Finally: We return the removed value
        return removed_value


def plot_speed():
    """
    Compares performance of the CDLLCD and the standard array based deque
    """

    # First we'll test sequences of basic operations

    sizes = [100 * i for i in range(0, 200, 5)]

    # (1) Grow large
    grow_avgs_array = []
    grow_avgs_CDLL = []

    for size in sizes:
        grow_avgs_array.append(0)
        grow_avgs_CDLL.append(0)
        data = list(range(size))
        for trial in range(3):

            gc.collect()  # What happens if you remove this? Hint: memory fragmention
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            # randomize data
            shuffle(data)

            start = default_timer()
            for item in data:
                cd_array.enqueue(item, item % 2)
            grow_avgs_array[-1] += (default_timer() - start) / 3

            start = default_timer()
            for item in data:
                cd_DLL.enqueue(item, item % 2)
            grow_avgs_CDLL[-1] += (default_timer() - start) / 3

    plt.plot(sizes, grow_avgs_array, color='blue', label='Array')
    plt.plot(sizes, grow_avgs_CDLL, color='red', label='CDLL')
    plt.title("Enqueue and Grow")
    plt.legend(loc='best')
    plt.show()

    # (2) Grow Large then Shrink to zero

    shrink_avgs_array = []
    shrink_avgs_CDLL = []

    for size in sizes:
        shrink_avgs_array.append(0)
        shrink_avgs_CDLL.append(0)
        data = list(range(size))

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            # randomize data
            shuffle(data)

            start = default_timer()
            for item in data:
                cd_array.enqueue(item, item % 2)
            for item in data:
                cd_array.dequeue(not item % 2)
            shrink_avgs_array[-1] += (default_timer() - start) / 3

            start = default_timer()
            for item in data:
                cd_DLL.enqueue(item, item % 2)
            for item in data:
                cd_DLL.dequeue(not item % 2)
            shrink_avgs_CDLL[-1] += (default_timer() - start) / 3

    plt.plot(sizes, shrink_avgs_array, color='blue', label='Array')
    plt.plot(sizes, shrink_avgs_CDLL, color='red', label='CDLL')
    plt.title("Enqueue, Grow, Dequeue, Shrink")
    plt.legend(loc='best')
    plt.show()

    # (3) Test with random operations

    random_avgs_array = []
    random_avgs_CDLL = []

    for size in sizes:
        random_avgs_array.append(0)
        random_avgs_CDLL.append(0)
        data = list(range(size))

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            shuffle(data)

            start = default_timer()
            for item in data:
                if randint(0, 3) <= 2:
                    cd_array.enqueue(item, item % 2)
                else:
                    cd_array.dequeue(item % 2)
            random_avgs_array[-1] += (default_timer() - start) / 3

            start = default_timer()
            for item in data:
                if randint(0, 3) <= 2:
                    cd_DLL.enqueue(item, item % 2)
                else:
                    cd_DLL.dequeue(item % 2)
            random_avgs_CDLL[-1] += (default_timer() - start) / 3

    plt.plot(sizes, random_avgs_array, color='blue', label='Array')
    plt.plot(sizes, random_avgs_CDLL, color='red', label='CDLL')
    plt.title("Operations in Random Order")
    plt.legend(loc='best')
    plt.show()

    def max_len_subarray(data, bound, structure):
        """
        returns the length of the largest subarray of `data` with sum less or eq to than `bound`
        :param data: list of integers to operate on
        :param bound: largest allowable sum
        :param structure: either a CircularDeque or a CDLLCD
        :return: the length
        """
        index, max_len, subarray_sum = 0, 0, 0
        while index < len(data):

            while subarray_sum <= bound and index < len(data):
                structure.enqueue(data[index])
                subarray_sum += data[index]
                index += 1
            max_len = max(max_len, subarray_sum)

            while subarray_sum > bound:
                subarray_sum -= structure.dequeue(False)

        return max_len

    # (4) A common application

    application_avgs_array = []
    application_avgs_CDLL = []

    data = [randint(0, 1) for i in range(5000)]
    window_lengths = list(range(0, 200, 5))

    for length in window_lengths:
        application_avgs_array.append(0)
        application_avgs_CDLL.append(0)

        for trial in range(3):
            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            start = default_timer()
            max_len_subarray(data, length, cd_array)
            application_avgs_array[-1] += (default_timer() - start) / 3

            start = default_timer()
            max_len_subarray(data, length, cd_DLL)
            application_avgs_CDLL[-1] += (default_timer() - start) / 3

    plt.plot(window_lengths, application_avgs_array,
             color='blue', label='Array')
    plt.plot(window_lengths, application_avgs_CDLL, color='red', label='CDLL')
    plt.title("Sliding Window Application")
    plt.legend(loc='best')
    plt.show()

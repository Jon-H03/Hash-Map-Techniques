# Name: Jonathan Hirsch
# OSU Email: hirschjo@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 5/9/2023
# Description: This file contains a HashMap class that uses open addressing with quadratic probing to
# handle collisions. This means that it will quadratically probe the array until it finds an empty index.
# It contains methods such as put, table_load, empty_buckets, resize_table, get, contains_key,
# remove, clear, get_keys_and_values, as well as an iterators __iter__ and __next__.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #
    def put(self, key: str, value: object) -> None:
        """
        Puts values into a hashmap given a specified key. If a node is already at
        the calculated index, this method will quadratically probe until it finds an
        empty one. Lastly, entries are entered in self._buckets as a HashEntry object.
        """
        # Check table load and resize if necessary
        if self.table_load() >= .5:
            self.resize_table(self._capacity * 2)

        # Calculate the index and save the initial index
        index = self._hash_function(key) % self._capacity
        initial_index = index

        # If the index is empty, simply place the HashEntry at that index.
        if self._buckets[index] is None:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
            return

        probe = 1
        # As long as the bucket at this index isn't empty
        while self._buckets[index]:
            # We check if the keys match
            if self._buckets[index].key == key:
                # If the value is a tombstone, we can just overwrite it.
                if self._buckets[index].is_tombstone is True:
                    self._buckets[index] = HashEntry(key, value)
                    self._size += 1
                    return
                else:
                    # Otherwise, just swap the values.
                    self._buckets[index].value = value
                    return
            # Calculate the next index and increment probe number.
            index = (initial_index + probe**2) % self._capacity
            probe += 1

        # Once broken out of the loop, it means we found an empty index,
        # set the bucket equal to the new HashEntry and increase the size.
        self._buckets[index] = HashEntry(key, value)
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the current load factor of the hash table.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the amount of empty buckets in the hash table.
        """
        return self.get_capacity() - self.get_size()

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes table as necessary given a new_capacity. New capacity can be smaller than
        current size, in which case, resize table utilizes the put function so that it can resize
        as necessary.
        """
        # New capacity cannot be less than or equal to current size.
        if new_capacity <= self._size:
            return
        # New capacity also has to be prime.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Initialize a new hash map
        new_hash = HashMap(new_capacity, self._hash_function)

        # Make sure that new capacity doesn't get changed to next prime if it's equal to 2.
        # This is because 2 is the only even prime number.
        if new_capacity == 2:
            new_hash._capacity = 2

        # Iterate through all the buckets, checking if each bucket is not empty.
        for i in range(self._capacity):
            node = self._buckets[i]
            if node:
                # If not None, put its key and value in the new hash map.
                new_hash.put(node.key, node.value)

        # Update the capacity and buckets to the new hash map.
        self._capacity = new_hash.get_capacity()
        self._buckets = new_hash._buckets

    def get(self, key: str) -> object:
        """
        Returns a key's value given a key. Returns None if no matches are found.
        """
        for i in range(self._capacity):
            if self._buckets[i] and self._buckets[i].key == key and not self._buckets[i].is_tombstone:
                return self._buckets.get_at_index(i).value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if a key is found in the hash table, otherwise False.
        """
        for i in range(self._capacity):
            if self._buckets[i] and self._buckets[i].key == key and not self._buckets[i].is_tombstone:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a node given a key. In this method, the node.is_tombstone is switched to True,
        effectively making it an empty bucket.
        Uses the iterator created below to iterate through each bucket in the array, and
        compares the specified key to each node's.
        """
        # Get the index and bucket at that index.
        for node in self:
            if node.key == key:
                node.is_tombstone = True
                self._size -= 1

    def clear(self) -> None:
        """
        Clears hash table and sets size to 0.
        """
        for i in range(self.get_capacity()):
            self._buckets[i] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a new DynamicArray object that contains all the hash table's
        key-value pairs.
        """
        new_arr = DynamicArray()
        i = 0

        # Iterate through each bucket, appending any key, value pairs to the new array.
        while i < self._capacity:
            if self._buckets[i] and not self._buckets[i].is_tombstone:
                new_arr.append((self._buckets[i].key, self._buckets[i].value))
            i += 1
        return new_arr

    def __iter__(self):
        """
        Creates iterator for loop
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtains next value and increment iterator
        """
        try:
            value = None
            while not value or value.is_tombstone:
                value = self._buckets[self._index]
                self._index += 1
        except DynamicArrayException:
            raise StopIteration
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

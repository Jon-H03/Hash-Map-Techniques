# Name: Jonathan Hirsch
# OSU Email: hirschjo@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 5/9/2023
# Description: This file contains a HashMap class that uses chaining to handle collisions.
# Every bucket in the class is initialized to an empty Linked List, and has methods such as:
# put (to add new key-values to the HashMap), empty_buckets, table_load (which returns the current
# load factor of the table, clear, resize_table (which modifies the capacity and rehashes the elements),
# get, contains, remove, get_keys_and_values, and lastly, an external method in find_mode.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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

    def get_index(self, key: str, hash_function) -> int:
        """Returns index for hash function"""
        return hash_function(key) % self._capacity

    def put(self, key: str, value: object) -> None:
        """
        Puts values into a hashmap given a specified key.
        """
        # Check if load factor >= 1, if so resize table.
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # Get the index and respective bucket at that index
        index = self.get_index(key, self._hash_function)
        bucket = self._buckets[index]

        # If bucket is empty, we can just insert the key, value pair
        if bucket.length() == 0:
            bucket.insert(key, value)
            self._size += 1
        # Otherwise, iterate through each node in the bucket,
        # and if we find a key that matches ours, we can effectively update it.
        # If there's no nodes in the bucket or no matching keys, we can simply insert the key-value pair into the bucket.
        else:
            for node in bucket:
                if node.key == key:
                    bucket.remove(key)
                    bucket.insert(key, value)
                    return
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets.
        """
        # Initialize counter to 0
        empty = 0
        # Iterate through all buckets, and if their length == 0,
        # increment the counter.
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empty += 1
        return empty

    def table_load(self) -> float:
        """
        Returns the current load factor of the hash table.
        """
        # Load factor = # of elements in table / # of buckets in table
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the hash table out.
        """
        # Iterate through every bucket, initializing it to a new linked list.
        for i in range(self.get_capacity()):
            self._buckets[i] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table based on a given new capacity. New capacity can be smaller than
        current size, in which case, resize table utilizes the put function so that it can resize
        as necessary.
        """
        # New capacity cannot be less than 1.
        if new_capacity < 1:
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
            if self._buckets[i].length() > 0:
                # If not empty, iterate through each node in bucket
                # and put its key and value in the new hash map.
                for node in self._buckets[i]:
                    new_hash.put(node.key, node.value)

        # Update the capacity and buckets to the new hash map.
        self._capacity = new_hash.get_capacity()
        self._buckets = new_hash._buckets

    def get(self, key: str):
        """
        Gets a value from the hashmap.
        """
        # Iterate through all the buckets and check if they contain the given key.
        # If so, return that key's value.
        for i in range(self._capacity):
            if self._buckets[i].contains(key):
                return self._buckets[i].contains(key).value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns a bool depending on if a key is present in the hash map.
        """
        # Iterate through all the buckets, checking if any of them contain the key.
        for i in range(self._capacity):
            if self._buckets[i].contains(key):
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a node using a given key from the hashmap.
        """
        # Get the index and bucket at that index.
        index = self.get_index(key, self._hash_function)
        bucket = self._buckets[index]

        # Check if bucket is filled
        if bucket and bucket.length() != 0:
            # If the node is the only one in the bucket,
            # we can just remove it
            if bucket.length() <= 1:
                removed = bucket.remove(key)
                if removed:
                    self._size -= 1
                return

            # Otherwise, iterate through each node in bucket,
            # If a matching key is found, remove it.
            for node in bucket:
                if node.key == key:
                    removed = bucket.remove(node.key)
                    if removed:
                        self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a new array containing all the key, value pairs.
        """
        # Initialize a new dynamic array and counter.
        new_arr = DynamicArray()
        i = 0

        # Iterate through each bucket, appending any key, value pairs to the new array.
        while i < self._capacity:
            curr_bucket = self._buckets[i]
            for node in curr_bucket:
                new_arr.append((node.key, node.value))
            i += 1
        return new_arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a new dynamic array, with the value(s) that had the highest occurrence as well as
    the number of times it/they occurred.
    """
    # Initialize a new hashmap and dynamic array.
    map = HashMap()
    new_arr = DynamicArray()

    # Iterate through the dynamic array, checking if they key is already in the new map
    for i in range(da.length()):
        if map.contains_key(da[i]):
            map.put(da[i], map.get(da[i])+1)
        else:
            map.put(da[i], 1)

    # Get all the key and value pairs and initialize cur max to 0.
    keys_and_values = map.get_keys_and_values()
    curr_max = 0
    # iterate through all the key-value pairs
    for k in range(keys_and_values.length()):
        # If the value of appearances is greater than cur max
        if keys_and_values[k][1] > curr_max:
            # Set the curr max equal to the new highest value
            curr_max = keys_and_values[k][1]
            # Initialize a new array and append the new high to it.
            new_arr = DynamicArray()
            new_arr.append(keys_and_values[k][0])
        # If the value of appearances is equal to curr max,
        # just append to the current array
        elif keys_and_values[k][1] == curr_max:
            new_arr.append(keys_and_values[k][0])

    # Return the new array, with the values number of occurrences.
    return new_arr, curr_max

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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")

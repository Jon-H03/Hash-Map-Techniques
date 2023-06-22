## Hash Map with Separate Chaining
### Description: 
`hash_map_sc.py` contains an implementation of a hash map using the separate chaining technique. Separate chaining is a collision resolution method in hash tables where each bucket in the table contains a linked list of elements that hash to the same index. This implementation provides efficient key-value storage and retrieval operations, with collision resolution handled through linked lists.

### Key Features
* Efficient storage and retrieval of key-value pairs.
* Collision resolution using separate chaining with linked lists.
* Supports dynamic resizing for optimal space utilization.
* Simple and intuitive API for insertion, deletion, and retrieval operations.
* Well-documented code with detailed explanations of the algorithm and data structures used.

## Quadratic Probing Hash Map
### Description:
`hash_map_oa.py`  contains an implementation of a hash map using the quadratic probing technique. Quadratic probing is a collision resolution method in hash tables where the key's hash function is modified using a quadratic polynomial to find the next available slot. This implementation provides efficient key-value storage and retrieval operations, with collision resolution handled through quadratic probing.

### Key Features
* Efficient storage and retrieval of key-value pairs.
* Collision resolution using quadratic probing for handling collisions.
* Supports dynamic resizing for optimal space utilization.
* Simple and intuitive API for insertion, deletion, and retrieval operations.
* Well-documented code with detailed explanations of the algorithm and data structures used.

## Comparision
Both implementations provide efficient storage and retrieval of key-value pairs and offer dynamic resizing for optimal space utilization. However, they differ in their collision resolution strategies.
* Separate Chaining: This approach uses linked lists to handle collisions. When multiple elements hash to the same index, they are stored in a linked list within the corresponding bucket. This allows for efficient handling of collisions but requires additional memory to store the linked lists.
* Quadratic Probing: This approach modifies the key's hash function by using a quadratic polynomial to find the next available slot when a collision occurs. It traverses the hash table by quadratic increments until an empty slot is found. Quadratic probing minimizes clustering and can provide better cache performance compared to separate chaining. However, it may suffer from secondary clustering, and when the hash table is full, it can be slower to insert new elements.

The choice between separate chaining and quadratic probing depends on factors such as the expected number of collisions, the desired memory usage, and the specific use case. Understanding these trade-offs is crucial in selecting the most appropriate collision resolution method for a given scenario.

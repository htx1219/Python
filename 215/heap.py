# modified to be able to store ids and values in heap.

# Heap shortcuts
def left(i): return i*2+1
def right(i): return i*2+2
def parent(i): return (i-1)/2
def root(i): return i==0
def leaf(L, i): return right(i) >= len(L) and left(i) >= len(L)
def one_child(L, i): return right(i) == len(L)
def val_(pair): return pair[0]

def swap(heap, old, new, location):
    location[heap[old]] = new
    location[heap[new]] = old
    (heap[old], heap[new]) = (heap[new], heap[old])

# Call this routine if the heap rooted at i satisfies the heap property
# *except* perhaps i to its children immediate children
#
#
# location is a dictionary mapping an object to its location
# in the heap
def down_heapify(heap, i, location):
    # If i is a leaf, heap property holds
    while True:
        l = left(i)
        r = right(i)

        # see if we don't have any children
        if l >= len(heap): 
            break

        v = heap[i][0]
        lv = heap[l][0]

        # If i has one child...                 
        if r == len(heap):
            # check heap property
            if v > lv:
                # If it fails, swap, fixing i and its child (a leaf)
                swap(heap, i, l, location)
            break

        rv = heap[r][0]
        # If i has two children...
        # check heap property
        if min(lv, rv) >= v: 
            break
        # If it fails, see which child is the smaller
        # and swap i's value into that child
        # Afterwards, recurse into that child, which might violate
        if lv < rv:
            # Swap into left child
            swap(heap, i, l, location)
            i = l
        else:
            # swap into right child
            swap(heap, i, r, location)
            i = r

# Call this routine if whole heap satisfies the heap property
# *except* perhaps i to its parent
def up_heapify(heap, i, location):
    # If i is root, all is well
    while i > 0: 
        # check heap property
        p = (i - 1) / 2
        if heap[i][0] < heap[p][0]:
            swap(heap, i, p, location)
            i = p
        else:
            break

# put a pair in the heap
def insert_heap(heap, v, location):
    heap.append(v)
    location[v] = len(heap) - 1
    up_heapify(heap, len(heap) - 1, location)

# build_heap
def build_heap(heap):
    location = dict([(n, i) for i, n in enumerate(heap)])
    for i in range(len(heap)-1, -1, -1):
        down_heapify(heap, i, location)
    return location

# remove min
def heappopmin(heap, location):
    # small = heap[0]
    val = heap[0]
    new_top = heap.pop()
    del location[val]
    if len(heap) == 0:
        return val
    location[new_top] = 0
    heap[0] = new_top
    down_heapify(heap, 0, location)
    return val

def decrease_val(heap, location, old_val, new_val):
    i = location[old_val]
    heap[i] = new_val
    # is this the best way?
    del location[old_val]
    location[new_val] = i
    up_heapify(heap, i, location)


def _test_location(heap, location):
    for n, i in location.items():
        assert heap[i] == n

def _test_heap():
    h = [(1, 'a'), (4, 'b'), (6, 'c'), (8, 'd'), 
         (9, 'e'), (1, 'f'), (4, 'g'), (5, 'h'),
         (7, 'i'), (8, 'j')]
    location = build_heap(h)
    _test_location(h, location)
    old_min = (-float('inf'), None)
    while len(h) > 0:
        new_min = remove_min_heap(h, location)
        _test_location(h, location)
        assert val_(old_min) <= val_(new_min)
        old_min = new_min    

def _test_add_and_modify():
    h = [(1, 'a'), (4, 'b'), (6, 'c'), (8, 'd'), 
         (9, 'e'), (1, 'f'), (4, 'g'), (5, 'h'),
         (7, 'i'), (8, 'j')]
    location = build_heap(h)
    insert_heap(h, (-1, 'k'), location)
    assert (-1, 'k') == remove_min_heap(h, location)
    decrease_val(h, location, (6, 'c'), (-1, 'c'))
    assert (-1, 'c') == remove_min_heap(h, location)
    _test_location(h, location)

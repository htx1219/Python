def insert(tree, element):
    if tree == None:
        return (None, element, None)
    else:
        left_child = tree[0]
        this_element = tree[1]
        right_child = tree[2]
        if element <= this_element:
            new_left_child = insert(left_child, element)
            return (new_left_child, this_element, right_child)
        else:
            new_right_child = insert(right_child, element)
            return (left_child, this_element, new_right_child)

def print_tree(tree):
    if tree == None:
        return
    else:
        left_child = tree[0]
        this_element = tree[1]
        right_child = tree[2]
        print_tree(left_child)
        print this_element
        print_tree(right_child)

def contains(tree, element):
    if tree == None:
        return False
    else:
        left_child = tree[0]
        this_element = tree[1]
        right_child = tree[2]
        if this_element == element:
            return True
        elif this_element >= element:
            return contains(left_child, element)
        else:
            return contains(right_child, element)

my_tree = (None, 'midpoint', None)
t1 = insert(my_tree, 'zuma, jacob')
t2 = insert(t1, 'atwood, margaret')
print_tree(t2)
print contains(t2, 'zuma, jacob')
t1 = None
for i in [8,6,7,5,3,0,9,3,1,4,1,5,9,2,6,5,3,5,]:
    t1 = insert(t1,i)

print_tree(t1)

# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    lst = [n for i, n in enumerate(lst) if i==0 or n != lst[i-1]]
    return lst


# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    lst = []
    i = 0
    while len(lst1) > 0 and len(lst2) > 0:
        if lst1[0] < lst2[0]:
            lst.append(lst1[0])
            lst1 = lst1[1:]
        else:
            lst.append(lst2[0])
            lst2 = lst2[1:]

    lst.extend(lst1)
    lst.extend(lst2)
       
    return lst

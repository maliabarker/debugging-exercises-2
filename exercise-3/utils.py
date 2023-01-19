"""Utility functions."""

def merge_sort(arr):
    """Sort the list in-place using the merge sort algorithm."""
    if len(arr) <= 1:
        return # already sorted
 
    # Finding the midpoint of the array
    mid = len(arr) // 2
    print(f'Mid index is: {mid}')

    # Dividing the array elements into 2 halves
    left_side = arr[:mid]
    right_side = arr[mid:]
    print(f'Left side of list: {left_side}, Right side of list: {right_side}')

    # Sorting the first and second half
    merge_sort(left_side)
    merge_sort(right_side)

    print('START SORT')
    i = j = k = 0
    print(f'i={i}, j={j}, k={k}')

    # Copy data to temp arrays L[] and R[]
    while i < len(left_side) and j < len(right_side):
        print(i, j)
        if left_side[i] > right_side[j]:
            print(f'Left side: {left_side[i]} is greater than right side: {right_side[j]}')
            arr[k] = left_side[i]
            print(f'New array: {arr}')
            # only increases i
            i += 1
        else:
            print(f'Right side: {right_side[j]} is greater than left side: {left_side[i]}')
            arr[k] = right_side[j]
            print(f'New array: {arr}')
            # only increases j
            j += 1
        # increases k no matter what
        k += 1

    # Checking if any element was left
    while i < len(left_side):
        print(f'i: {i} is less than length of left side: {len(left_side)}')
        arr[k] = left_side[i]
        print(f'New array: {arr}')
        i += 1

    while j < len(right_side):
        print(f'j: {j} is less than length of right side: {len(right_side)}')
        arr[k] = right_side[j]
        print(f'New array: {arr}')
        j += 1




def binary_search(arr, elem):
    """Return the index of the given element within a sorted array."""
    low = 0
    high = len(arr) - 1
    mid = 0
    print('STARTING BINARY SEARCH')
    while low < high: 
        
        mid = (high + low) // 2
        print(mid)
  
        # If elem is greater, ignore left half 
        if arr[mid] < elem: 
            low = mid + 1
  
        # If elem is smaller, ignore right half
        elif arr[mid] > elem: 
            high = mid - 1
  
        # Check if elem is present at mid 
        else:
            return mid

    # If we reach here, then the element was not present 
    return -1

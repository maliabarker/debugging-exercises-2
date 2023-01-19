from utils import merge_sort, binary_search

if __name__ == '__main__':
    list_of_nums = [7, 4, 9, 3, 5, 6, 1, 2]
    print(f'List of nums is: {list_of_nums}')

    merge_sort(list_of_nums)
    print(f'Sorted list of nums is: {list_of_nums}')

    index_of_5 = binary_search(list_of_nums, 5)
    print(f'Index of 5 is: {index_of_5}')
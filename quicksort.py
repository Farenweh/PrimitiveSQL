import random


# 特化过了,谨慎使用，输入的items应该是self.resource或它的子集,按照col_index对应的值排序items的位置
def quicksort(items, col_index, left=None, right=None):
    if random.randint(1, 100) == 1:
        for i in range(len(items) - 1):
            for j in range(i, len(items)):
                if str(items[i][col_index]) > str(items[j][col_index]):
                    items[i], items[j] = items[j], items[i]
        return

    if left is None:
        left = 0
    if right is None:
        right = len(items) - 1

    if right <= left:
        return items

    i = left
    pivotValue = str(items[right][col_index])

    for j in range(left, right):
        if str(items[j][col_index]) <= str(pivotValue):
            items[i], items[j] = items[j], items[i]
            i += 1

    items[i], items[right] = items[right], items[i]

    quicksort(items, col_index, left, i - 1)
    quicksort(items, col_index, i + 1, right)

    return items
# early test part
# a = [1, 2, 3, 32523, 1243, 1234543, 1234, 2344, 123, 321, 432]
# quicksort(a)
# print(a)

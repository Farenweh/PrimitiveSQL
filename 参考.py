import os
import pickle
import re

type_of_obj = ''  # 序列化
prop_list = []  # 序列化
object_list = []  # 序列化
storage_list = [0, 0, 0]  # 0:clas,1:prop_list,2:object_list
default = active_db = open('参考.py')  # 打开自己作为默认活动对象


def initialize():
    if 'datasheet' in os.listdir():  # 检查存不存在数据表目录
        os.chdir('datasheet')
        if os.listdir() != 0:  # 检查目录下有没有已经存在的数据表
            return 0  # 有就不执行初始化
        else:
            return -1  # 返回-1，代表表内没有任何数据表
    else:
        os.mkdir('datasheet')  # 在工作空间下新建一个datasheet目录，方便隔离数据和程序
        os.chdir(os.getcwd() + '/datasheet')  # 切换到datasheet
        return 1


def new(name, sample):  # 新建(覆盖）表 sample导入一个该数据表将要储存的对象实例（用来规范数据表格式，该实例不会被储存）
    global type_of_obj
    global active_db
    global storage_list
    name = name + '.db'

    storage_list[0] = getattr(sample, '__class__')  # 写入sl[0]

    with open(name, 'wb+') as active_db:
        # pickle.dump(clas, active_db)  # 把将要存储的对象类型写进第0行
        # pickle.dump('\n', active_db)  # 换行符1
        global prop_list
        prop_list = []

        for prop in dir(sample)[26:]:  # 从第26个元素开始，遍历对象实例的所有属性名称组成的列表
            if re.search('[0-9.]', str(getattr(sample, prop))):  # 判断每个prop里是不是可以排序的纯数字
                sortable = 0  # 找到任何一个非数字和“.”的符号都写0
            else:
                sortable = 1  # 否则写1
            prop_list.append([prop, sortable])
        storage_list[1], storage_list[2] = prop_list, object_list  # 把prop_list写入sl[1],object_list写入sl[2]
        # pickle.dump(prop_list, active_db)  # 把prop_list序列化写进第1行
        # pickle.dump('\n', active_db)  # 给第1行添加换行符
        # pickle.dump(object_list, active_db)  # 把object_list序列化写进第2行
        pickle.dump(storage_list, active_db)  # 将storage_list序列化并写入
    print('新建数据表{}成功！'.format(name))
    return 1


def load(name, mode='0'):  # 挂载输入的数据表，并准备进行操作，缺省挂载为读模式
    global active_db
    global object_list
    global storage_list
    global prop_list
    global type_of_obj
    active_db.close()
    if os.path.isfile(name) == 1:  # 判断文件名存不存在
        active_db = open(name, 'rb')
        """global clas
        temp_list = active_db.readlines()
        clas = temp_list[0]
        prop_list = pickle.load(temp_list[1])  # 反序列化prop_list
        object_list = pickle.load(temp_list[2])  # 反序列化object_list
        """
        storage_list = pickle.load(active_db)  # 反序列化回storage_list
        clas, prop_list, object_list = storage_list[0], storage_list[1], storage_list[2]  # 将数据挂到内存
        if mode != '0':  # 非0就挂载为wb+
            active_db.close()
            active_db = open(name, 'wb+')
        return 1
    else:
        return 0


def add(add_obj):
    if active_db != default and (
            active_db.mode == 'rb+' or 'wb+'):  # 检查挂表没有/有没有挂成可写，值得注意的是，由于feature，rb+在作用上等价wb+，但模式名称不同
        global object_list
        object_list.append(add_obj)
        return 1
    else:
        return 0  # 没挂载或者没有挂载为可写


def pop(pop_index):  # 考虑到可能出现重叠数据的情况，所以使用索引执行删除 避免歧义
    if active_db != default and active_db.mode == 'rb+' or 'wb+':  # 检查挂表没有/有没有挂成a+
        global object_list
        object_list.pop(pop_index)
        return 1
    else:
        return 0  # 没挂载或者没有挂载为可写


def find(by_what, key):
    for index_0 in range(0, len(prop_list)):
        if prop_list[index_0][0] != by_what:  # 找一下属性表里有没有对应的属性
            return 0
        elif prop_list[index_0][1] == 0:  # 不可排序时，遍历
            res_list = []
            for index_1 in range(0, len(object_list)):
                if key in getattr(object_list[index_1], by_what):  # 如果对象列表中第index_1个对象的by_what属性对上了key值
                    res_list.append(index_1)
            return res_list  # 返回该对象所在的索引组成的列表

        else:  # 可排序时，先排序，再二分（值得注意的是，存进来的是字符串，要先类型转换）
            object_list_in_order = quick_sort(object_list, 0, len(object_list) - 1, by_what)  # 快排——改
            # 此时，object_list_in_order已经按照by_what正序排好
            return binarysearch(object_list_in_order, 0, len(object_list) - 1, key, by_what)
            # 返回index或者-1（失败）


def rewrite(index, new_obj):
    object_list[index] = new_obj
    return 1


def helper():
    # 这里还要写点操作参数指南，但鉴于这是一个Samples，所以我没写，只做了已有数据表显示
    print('本系统中已经存有如下数据表')
    print(os.listdir())  # 显示当前目录下（应该就是datasheet）所有的文件


def remove(name):
    os.remove(name)
    print('抹除数据表{}成功'.format(name))
    return 1


def dis():
    pass


def unload():
    """
    active_db.write(clas)
    pickle.dump(prop_list, active_db)
    active_db.write('\n')
    pickle.dump(object_list, active_db)
    active_db.close()
"""
    storage_list[0], storage_list[1], storage_list[2] = type_of_obj, prop_list, object_list  # 将数据在内存中归一
    pickle.dump(storage_list, active_db)  # 序列化写入
    active_db.close()
    return 1


def get_obj(index):
    return object_list[index]


def quick_sort(lists, left, right, by_what):  # 这是一个特化耦合的快排！！不要乱用！！
    # 跳出递归判断
    if left >= right:
        return lists

    # 选择参考点，该调整范围的第1个值
    key = float(getattr(lists[left], by_what))  # lists[left]
    key_obj = lists[left]
    low = left
    high = right

    # 循环判断直到遍历全部
    while left < right:
        # 从右边开始查找大于参考点的值
        while left < right and float(getattr(lists[right], by_what)) >= key:
            #                   lists[right]
            right -= 1
        lists[left] = lists[right]  # 这个位置的对象先挪到左边

        # 从左边开始查找小于参考点的值
        while left < right and float(getattr(lists[left], by_what)) <= key:
            #                  lists[left]
            left += 1
        lists[right] = lists[left]  # 这个位置的对象挪到右边

    # 写回对象到对应位置
    lists[left] = key_obj

    # 递归，并返回结果
    quick_sort(lists, low, left - 1, by_what)  # 递归左边部分
    quick_sort(lists, left + 1, high, by_what)  # 递归右边部分
    return lists


# 返回 x 在 arr 中的索引，如果不存在返回 -1
def binarysearch(arr, length, r, x, by_what):  # 找不到返回-1.找到会返回包含全部结果的对象的列表
    res_list = []
    # 基本判断
    if r >= length:

        mid = int(length + (r - length) / 2)

        # 元素整好的中间位置
        if float(getattr(arr[mid], by_what)) == x:
            # arr[mid]
            res_list.append(mid)  # 直接把该对象的索引放进结果列表里
            restore = mid  # 保存初始结果
            while 1:
                if float(getattr(arr[mid + 1], by_what)) == x:  # 向右找其他解
                    mid += 1
                    res_list.append(mid)
                else:
                    break
            mid = restore  # 重置指针到初始结果
            while 1:
                if float(getattr(arr[mid + 1], by_what)) == x:  # 向左找其他解
                    mid += 1
                    res_list.append(mid)
                else:
                    return res_list  # 返回结果列表

        # 元素小于中间位置的元素，只需要再比较左边的元素
        elif float(getattr(arr[mid], by_what)) > x:
            return binarysearch(arr, length, mid - 1, x, by_what)

            # 元素大于中间位置的元素，只需要再比较右边的元素
        else:
            return binarysearch(arr, mid + 1, r, x, by_what)

    else:
        # 不存在
        return -1

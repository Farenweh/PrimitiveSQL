import avl_func
import quicksort
import cfg


# global active_database


class Table:
    # global active_database

    def __init__(self, tab_name: str, names_types: tuple):
        self.name = tab_name

        # {'属性名':[列号,类型]}
        self.column = {}
        # ['col_name_a':col_index,col_name_b':col_index]
        self.primary_key = {}
        # {'属性名':['not null','unique','check']}
        # 名称中间是空格而不是_，检查的时候会自动处理空格为_
        self.constrain = {}
        # {'属性名':'row[self.column[col_name][0]] expression'}
        # 例如: 1<a<3 应当记作 '1 < row[self.column['a'][0]] <3'
        self.check_expression = {}
        # {'属性名':缺省值}
        self.default_value = {}
        # {'属性名':['表名','属性名']}
        self.foreign_reference = {}
        # {'属性名':'索引类型'}
        self.index = {}
        # {'属性名':Avl tree}
        # Node: key:self.key | index:self.index
        self.trees = {}
        # {'name':[]}
        # [],m=2*i
        self.hash_table = {}
        self.bunk_capa = 0
        self.resource = []
        """
            [
                 0[   ]
                 1[   ]
                 2[   ]
                       ]
        """

        for i in range(0, len(names_types), 2):
            self.column[names_types[i]] = [int(i / 2), names_types[i + 1]]

    @staticmethod
    # 在inter_func层处理names_types
    def create(tab_name: str, names_types: tuple):
        # 一种新的实现方式，使得可以通过名称直接访问对应的对象，相较于字典访问更加方便，
        # 但共享的名字空间可能因为冲突而不鲁棒
        # eval('%s = Table(tab_name, names_types)' % tab_name)
        # eval('active_database.insert_table(%s)' % tab_name)
        # print('数据表已创建')

        now_table = Table(tab_name, names_types)
        cfg.active_database.insert_table(now_table)
        print('数据表已创建')

    def delete(self):
        cfg.active_database.delete_table(self.name)

    def add_index(self, col_name: str, index_type: str) -> bool:
        def clustered_index(column_name: str):
            # 更改聚簇列
            for key in self.index.keys():
                if self.index[key] == 'clustered index':
                    print('原聚簇索引已删除')
                    self.index.pop(key)
                    break
            self.index[column_name] = 'clustered index'
            return True

        # avl-TREE to restore index
        def normal_index(column_name: str):
            now_tree = avl_func.AVLTree()
            col = self.column[column_name][0]
            i = 0
            for row in self.resource:
                # 前一个是key，后一个是行号，
                # 分别对应node的val和index属性
                now_tree.insert(row[col], i)
                i += 1
            self.trees[column_name] = now_tree
            self.index[column_name] = 'normal index'
            return True

        def hash_index(column_name: str) -> bool:
            # 适配hash索引
            flag = 0
            col_index = self.column[column_name]
            # 理论上2*i就够了，但我懒得扩桶
            # m = 2 * len(self.resource)
            self.bunk_capa = 1000
            now_hash = [-1] * self.bunk_capa
            for row in self.resource:
                val = hash(row[col_index]) % self.bunk_capa
                while now_hash[val] != -1:
                    val = hash(val) % self.bunk_capa
                # 再散列
                now_hash[val] = flag
                flag += 1
            self.hash_table[column_name] = now_hash
            self.index[column_name] = 'hash index'
            return True

        if col_name not in self.column.keys():
            print('指定列不存在')
            return False
        if not index_type.isalpha():
            # 把空格换成下划线，全换成小写
            index_type = '_'.join(index_type.split(' ')).lower()
        if eval(index_type)(col_name) is False:
            return False
        return True

    def show_index(self):
        print(self.index)

    def delete_index(self, column: str):
        self.index.pop(column)

    def show_struct(self):
        print(self.column)

    # not null
    # unique
    # primary key
    # foreign key
    # check
    # default
    # grouped primary key
    # 一次约束一列，在inter层复用
    def add_constrain(self, col_name: str or tuple, constrain_type: list, check_expression=None):
        # 先校验表中数据符合要求否
        if type(col_name) is str:
            if self.check_table_constrain(col_name, constrain_type):
                # 记录约束
                self.constrain[col_name] = constrain_type
                if 'primary_key' in constrain_type:
                    self.primary_key[col_name] = self.column[col_name][0]
                    # 设主键为聚簇索引
                    self.add_index(col_name, 'clustered index')
                    print(col_name + '已设为主键并建立聚簇索引')
                print('约束已添加')
                # self.refresh()
            else:
                print('约束添加失败')
        if col_name is tuple:
            # 专门处理复合主键的分支
            if self.check_table_constrain(col_name, constrain_type):
                for col in col_name:
                    self.primary_key[col] = self.column[col][0]
                    self.constrain[col].append('grouped primary key')
                else:
                    print('复合主键添加失败')

    # 为空则全部删除
    def delete_constrain(self, col_name: str, types_to_del=None):
        if types_to_del is None:
            types_to_del = []
        if not types_to_del:
            self.constrain.pop(col_name)
        else:
            for type_to_del in types_to_del:
                if type_to_del != 'grouped primary key':
                    for i in range(len(self.constrain[col_name])):
                        if self.constrain[col_name][i] == type_to_del:
                            self.constrain[col_name] = self.constrain[col_name].pop(i)
                            print(col_name + '的' + type_to_del + '已删除')
                            continue
                    print('指定要删除的约束类型' + type_to_del + '不存在于此列')
                else:
                    self.primary_key.pop(col_name)
                    for i in range(len(self.constrain[col_name])):
                        if self.constrain[col_name][i] == type_to_del:
                            self.constrain[col_name] = self.constrain[col_name].pop(i)
                            print(col_name + '的' + type_to_del + '已删除')
                    if len(self.primary_key) == 1:
                        self.constrain[self.primary_key[0]] = 'primary key'
                        print('复合主键已退化为主键')

    # 用来在添加新约束前，检验现有表是否满足新加约束，一次校验一列
    # expression:例如: 1<a<3 应当传入为 '1 < row[self.column['a'][0]] <3'
    def check_table_constrain(self, column_name: str or tuple, constrain_type: list, reference_table='',
                              reference_key='', expression='') -> bool:

        def not_null(col_name: str) -> bool:
            for row in self.resource:
                if row[self.column.get(col_name)[0]] is not None:
                    continue
                else:
                    print('选中列存在空值')
                    return False
            return True

        def unique(col_name: str) -> bool:
            check_list = []
            for row in self.resource:
                if row[self.column.get(col_name)[0]] not in check_list:
                    check_list.append(row[self.column.get(col_name)][0])
                else:
                    print('选中列存在重复数据')
                    return False
            return True

        # 组合主键的性能会非常烂，组合的越多越烂
        def primary_key(col_name: str) -> bool:
            return not_null(col_name) and unique(col_name)

        def grouped_primary_key(col_name: tuple) -> bool:
            for i in range(len(self.resource)):
                a = []
                for col in col_name:
                    a.append(self.resource[i][self.column[col][0]])
                for j in range(i, len(self.resource)):
                    b = []
                    for col in col_name:
                        b.append(self.resource[i][self.column[col][0]])
                    if a == b:
                        print('选中列存在重复组合')
                        return False
            return True

        def foreign_key(col_name: str) -> bool:
            ref_tab = cfg.active_database.resource[cfg.active_database.table[reference_table]]
            ref_index = ref_tab.column[reference_key][0]
            # {'属性名':['表名','属性名']}
            if reference_table not in cfg.active_database.table:
                print('参考表不存在')
                return False

            if reference_key not in ref_tab.column:
                print('参考表中不存在此属性')
                return False

            if ref_tab.primary_key != reference_key:
                print('参考列不是主键')
                return False

            ref_list = []
            for row in ref_tab.resource:
                ref_list.append(row[ref_index])
            for row in self.resource:
                if row[self.column.get(col_name)[0]] not in ref_list:
                    print('选中列中存在参考列不存在的数据')
                    return False

            return True

        def check(col_name: str) -> bool:
            for row in self.resource:
                if eval(expression):
                    continue
                else:
                    print('选中列存在不符合表达式的数据')
                    return False
            return True

        def default(col_name: str, default_value) -> bool:
            if not_null(col_name) is True:
                return True
            else:
                if input('要将表内所有的空值都设为现在设置的缺省值吗？\nY/N') == 'Y' or 'y':
                    for i in range(len(self.resource)):
                        if self.resource[i][self.column.get(col_name)[0]] is None:
                            # 浅复制而非指向导致的bug已修正
                            self.resource[i][self.column.get(col_name)[0]] = default_value
                else:
                    return False

        # 按照constrain_type迭代执行校验
        if column_name not in self.column.keys():
            print('指定列不存在')
            return False
        for constrain in constrain_type:
            if not constrain.isalpha():
                # 把空格换成下划线
                constrain = '_'.join(constrain.split(' '))
            if eval(constrain)(column_name) is False:
                return False
        return True

    # 用来校验新加数据是否满足现有表校验的函数
    def check_data_constrain(self, values: list, column_names: tuple) -> bool:
        # check
        def check(value, col_name: str) -> bool:
            return eval(self.check_expression[col_name])

        def not_null(value, col_name: str) -> bool:  # 这个未使用的形参不要删除，因为eval()会传来此参数
            if value is not None:
                return True
            print('非空列的输入数据为空')
            return False

        def unique(value, col_name: str) -> bool:
            check_list = []
            for row in self.resource:
                check_list.append(row[self.column.get(col_name)[0]])
            if value not in check_list:
                return True
            print('具备唯一约束列的输入数据与现有数据重复')
            return False

        def primary_key(value, col_name: str) -> bool:
            return not_null(value, col_name) and unique(value, col_name)

        def grouped_primary_key(val, col) -> bool:
            primary_key_i = []
            check_list = []
            for i in range(len(col)):
                if 'grouped primary key' in self.constrain[col[i]] and val:
                    primary_key_i.append(i)
            # breakpoint
            return True

        def foreign_key(value, col_name: str) -> bool:
            # foreign_reference:{'属性名':['表名','属性名']}
            ref_tab = cfg.active_database.resource[cfg.active_database.table[self.foreign_reference[col_name][0]]]
            ref_column_index = ref_tab.column[self.foreign_reference[col_name][1]]
            ref_list = []
            # 把参考列的数据全读出来放到ref_list里
            for row in ref_tab.resource:
                ref_list.append(row[ref_column_index])
            if value in ref_list:
                return True
            print('外键列的输入数据在参考列中不存在')
            return False

        def default(value, col_name: str) -> bool:
            # 不需要 MS会在维护的时候自动填上缺省值
            return True

        # 先检验非空列有没有出现在输入列名单
        not_null_column = []
        for column in self.constrain:
            if 'not null' in self.constrain[column]:
                not_null_column.append(column)
        for column in not_null_column:
            if column not in column_names:
                print('输入列名单中缺少约束非空的列')
                return False

        # 一次校验一个数据
        for _value in values:
            # 一次校验一列
            for column_name in column_names:
                # 一次校验一个约束
                if column_name not in self.column.keys():
                    print('指定列不存在')
                    return False
                if self.constrain.get(column_name) is None:
                    return True
                for constrain in self.constrain.get(column_name):
                    if not constrain.isalpha():
                        # 把空格换成下划线
                        constrain = '_'.join(constrain.split(' '))
                    if eval(constrain)(_value, column_name) is False:
                        return False
        return True

    # 传入的column_names得是元组，在inter层处理
    def insert_data(self, values: list, column_names=()) -> bool:
        if column_names != ():
            if len(values) != len(column_names):
                print('输入数据个数与输入列个数不一致')
                return False
            for column_name in column_names:
                if column_name not in self.column.keys():
                    print('指定列不存在')
                    return False
            # data_constrain检验
            if not self.check_data_constrain(values, column_names):
                return False
            # 维护values的顺序，对规模n只需交换n-1次位置
            for i in range(0, len(column_names) - 1):
                values[i], values[self.column.get(column_names[i])[0]] = values[self.column[column_names[i]][0]], \
                                                                         values[i]
            # 执行插入
            self.resource.append(values)
        else:
            if len(values) != len(self.column):
                print('输入数据个数与表中所含列个数不一致')
                return False
            # data_constrain检验
            column_names = [0] * len(self.column)
            for col in self.column.keys():
                column_names[self.column.get(col)[0]] = col
            column_names = tuple(column_names)
            # 以上是为了解决column_names在这里是空的的workaround
            # dict.key()的遍历顺序和存储顺序一致
            if not self.check_data_constrain(values, column_names):
                return False
            self.resource.append(values)
        self.refresh()
        return True

    # 删除数据,在inter层在select中完成结果裁剪和处理逻辑运算查询
    def delete_data(self, col_name: str, value) -> bool:
        if col_name not in self.column.keys():
            print('指定列不存在')
            return False
        col_index = self.column.get(col_name)[0]
        flag = 0
        for row in self.resource:
            if row[col_index] == value:
                self.resource.pop(flag)
                flag += 1
        self.refresh()
        return True

    # 单表查询，返回所有满足条件的，冠以行号的根据res_range裁切后的单行 组成的二维数组
    # 每一行的行首加入行号,是为了方便update等函数找到对象其位置，如不需要，在select时循环pop掉row[0]即可
    # 在inter层在select中处理多表查询，下面同理
    # 单次查找只支持单次范围，默认认为表达式左右两侧的顺序形同a>1

    def find_data(self, col_selected: list, col_name: str,
                  symbol: str, key: str) -> list:

        # result_trimmer，将返回的数据按照col_selected分好
        # 注意！此时的result第一列被冠以行号！
        def result_trimmer(result_: list):
            index_selected_ = []
            now_result = []
            for name_ in col_selected:
                # 注意！此时的result第一列被冠以行号，所以列的实际位置+1
                index_selected_.append(self.column[name_][0] + 1)
            for row_ in result_:
                now_row = [row_[0]]  # 加入数据实际所在行号,方便update等函数找到对象其位置，在select时删掉
                for i in index_selected_:
                    now_row.append(row_[i])
                now_result.append(now_row)
            # 在第0行插入表头
            workaround = ['Row ID'] + col_selected
            now_result.insert(0, workaround)
            return now_result

        # 排除列名不存在
        if col_name not in self.column.keys():
            print('指定查找的列不存在')
            return []
        if col_selected[0] != '*':
            for name in col_selected:
                if name not in self.column:
                    print('指定显示的列不存在')
                    return []
        else:
            col_selected = []
            for col in self.column.keys():
                col_selected.append(col)

        # # 排除字符串范围查找
        # if col_name is str and r_symbol != '=':
        #     print('字符串类型不支持范围查找')
        #     return []

        col_index = self.column.get(col_name)[0]
        # 列未被索引时
        if col_name not in self.index:  # or (self.index[col_name] == 'hash index'):
            result = []
            flag = 0
            # 遍历
            for row in self.resource:
                # 重构表达式，默认认为表达式左右两侧的顺序形同a>1
                a = str(row[col_index])
                b = key  # .replace("\'", "")
                if symbol == '=':
                    symbol = '=='
                if "\'" in b:
                    a = "\'" + a + "\'"
                to_eval = a + symbol + b
                if eval(to_eval):
                    # 在这里已经为第一列添加过行号
                    result.append([flag] + row)
                flag += 1
            # 裁切
            result = result_trimmer(result)
            return result

        # 列被聚簇索引时
        if self.index[col_name] == 'clustered index':
            # 二分查找
            def binarySearch(reso, l_p: int, r_p: int, targ):
                if r_p >= l_p:
                    mid = int(l_p + (r_p - l_p) / 2)
                    if str(reso[mid][col_index]) == str(targ):
                        return mid
                    elif str(reso[mid][col_index]) > str(targ):
                        return binarySearch(reso, l_p, mid - 1, targ)
                    else:
                        return binarySearch(reso, mid + 1, r_p, targ)
                else:
                    # 不存在
                    return None

            low_index = high_index = binarySearch(self.resource, 0, len(self.resource), key)
            # 确保low_index和high_index为边界
            while low_index > 0:
                if self.resource[low_index - 1][col_index] != self.resource[low_index][col_index]:
                    break
                else:
                    low_index -= 1
            while high_index < len(self.resource):
                if self.resource[high_index + 1][col_index] != self.resource[high_index][col_index]:
                    break
                else:
                    high_index += 1
            result = []
            flag = [low_index]
            for row in self.resource[low_index:high_index + 1]:
                result.append(flag + row)
                flag[0] += 1
            # 裁切
            result = result_trimmer(result)
            return result

        # 列被次级索引时
        if self.index[col_name] == 'normal index':
            # DFS node.insert时会把相同值放在现有节点右边
            def dfs(root: avl_func.AVLNode, key_, result_pool=None):
                if result_pool is None:
                    result_pool = []
                if root is None:
                    return
                to_eval_ = 'root.key' + symbol + 'key_'
                if eval(to_eval_):
                    result_pool.append(self.resource[root.index])
                    if symbol == '>' or '>=':
                        res_node_list = avl_func.inOrder(root.right)
                        for node in res_node_list:
                            result_pool.append(self.resource[node.index])
                        dfs(root.left, key_)
                    elif symbol == '=':
                        dfs(root.right, key_)
                    elif symbol == '<' or '<=':
                        res_node_list = avl_func.inOrder(root.left)
                        for node in res_node_list:
                            result_pool.append(self.resource[node.index])
                        dfs(root.right, key_)
                else:
                    if symbol == '>' or '>=':
                        dfs(root.right, key_)
                    elif symbol == '=':
                        if root.key > key_:
                            dfs(root.left, key_)
                        else:
                            dfs(root.right, key_)
                    elif symbol == '<' or '<=':
                        dfs(root.left, key_)
                return result_pool

            result = dfs(self.trees[col_name].root, key)
            # 裁切
            result = result_trimmer(result)
            return result

        # 列被哈希索引时 hash查找
        if self.index[col_name] == 'hash index':
            result_pool_ = []
            hash_pool = []

            val = hash(key) % self.bunk_capa
            while val not in hash_pool and self.hash_table[col_name][val] is not None:
                hash_pool.append(val)
                result_pool_.append(
                    [self.hash_table[col_name][val]] + self.resource[self.hash_table[col_name][val]])
                val = hash(key) % self.bunk_capa

            return result_trimmer(result_pool_)

    # 改数据，在inter层搭配find_data函数使用
    # done 更新时会添加行号字段 需修改
    def update_data(self, row_index: int, col_name: str, value) -> bool:
        col_index = self.column.get(col_name)[0]
        if col_index is None:
            print('指定了不存在的列')
            return False
        self.resource[row_index][col_index] = value
        self.refresh()
        return True

    # 维护数据表及其索引,只在本模块的1级函数中使用
    def refresh(self):
        def sort_by_primary_key(key_list: list, start=0, end=len(self.resource) - 1, time=0):
            now_sort_index = self.column[key_list[time]][0]
            quicksort.quicksort(self.resource[start:end], now_sort_index)
            next_start, next_end, record = 0, 0, False
            for i in range(start, end):
                if self.resource[i][now_sort_index] == self.resource[i + 1][now_sort_index]:
                    next_start = i
                    record = True
                elif record is True:
                    record = False
                    next_end = i
                    time += 1
                    sort_by_primary_key(key_list, next_start, next_end, time)
            return True

        # 1 按照主键值对resource中的所有行进行快速排序
        if self.primary_key != {}:
            keys = []
            for key in self.primary_key.keys():
                keys.append(key)
            sort_by_primary_key(keys)

        # 2 依次重建索引并储存
        for key in self.index.keys():
            if self.index[key] != "clustered index":
                self.add_index(key, self.index[key])

        # 3
        # 维护default列，给None填上缺省值
        for key in self.constrain:
            if self.constrain[key] != 'default':
                continue
            col_index = self.column[key][0]
            for i in range(len(self.resource)):
                if self.resource[i][col_index] is None:
                    self.resource[i][col_index] = self.default_value[key]

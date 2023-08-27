# 用户交互界面
import copy
import os
import re

import db_func
import quicksort
import tab_func
import cfg


# sql_word[2] = test

# global active_database


def init():
    if 'data' not in os.listdir():  # 检查存不存在数据目录
        os.mkdir('data')  # 在工作空间下新建一个data目录，方便隔离数据和程序
    print('初始化成功')


def create_database(db_name: str):
    if db_func.Database.create(db_name):
        return True
    else:
        return False


# 选库函数直接把选中的db文件打开成全局变量active_database并暴露给其他函数进行操作。
def choose_database(db_name: str):
    # global active_database
    if db_func.Database.load(db_name):
        return True
    else:
        return False


def delete_database():
    if cfg.active_database.delete_databese():
        return True


def query(sql: str, tag=''):
    sql = sql.replace("\n", "")
    sql_word = sql.split(" ")
    if len(sql_word) < 2:
        print("[!] Wrong query!")
        return
    operate = sql_word[0].lower()

    # if operate == 'use':
    #     if sql_word[1] == 'database':
    #         try:
    #             use_db(sql_word[2])
    #         except:
    #             print("[!]Error")
    #     else:
    #         print("[!]Syntax Error.\neg:>use database dbname")

    # 条件解析 = != > < >= <=
    def condition_parse(condition: str):
        symbol = None
        if '=' in condition:
            symbol = '='
        elif '!=' in condition:
            symbol = '!='
        elif '>' in condition:
            symbol = '>'
        elif '>=' in condition:
            symbol = '>'
        elif '<' in condition:
            symbol = '<'
        elif '<=' in condition:
            symbol = '<='
        col_condition = condition.split(symbol)[0]
        key = condition.split(symbol)[1]
        return col_condition, key, symbol

    def selecting(symbol: str, res_range: list, col_columns: str, key):
        # if symbol == '<' or symbol == '<=':
        result = cfg.active_database.resource[cfg.active_database.table[table_name]].find_data(
            col_selected=res_range, col_name=col_columns, symbol=symbol, key=key)
        # elif symbol == '>' or symbol == '>=':
        #     result = cfg.active_database.resource[cfg.active_database.table[table_name]].find_data(
        #         col_selected=res_range, col_name=col_columns,
        #         l_symbol=symbol,
        #         low=key)
        # else:
        #     result = cfg.active_database.resource[cfg.active_database.table[table_name]].find_data(
        #         col_selected=res_range, col_name=col_columns, low=key,
        #         high=key)
        return result

    # 新建表格
    if operate == 'create':
        if sql_word[1] == 'database':
            try:
                db_func.Database.create(sql_word[2])
            # 创建数据库 数据库名称：sql_word[2]
            except:
                print("[!]Create Error")
        elif sql_word[1] == 'table':
            #  提取括号中内容（列名 主键）
            # 表名:tab_name
            tab_name = sql_word[2].split('(')[0]
            # 列名+类型：names_types, 主码:primary_key
            if "Primary_key" in sql:
                # 输出names_types
                a = re.findall(r'\((.*)\)', sql)[0]
                b = a.split('Primary_key')
                names_ls = (b[0]).split(',')
                # 删去最后的空格
                del names_ls[-1]
                first = [names.split()[0] for names in names_ls]
                last = [names.split()[1].lower() for names in names_ls]
                names_ls1 = []
                # i = len(first)
                for i in range(0, len(first)):
                    # name_list = first_names[i] + last_name[i]
                    names_ls1.append(first[i])
                    names_ls1.append(last[i])
                names_types = tuple(names_ls1)
                # 输出primary_key
                key = re.findall(r'\((.*)\)', b[1])[0].split(',')
                primary_key = []
                for i in key:
                    primary_key.append(i.replace(" ", ""))
                if len(primary_key) > 1:
                    primary_key = tuple(primary_key)
                else:
                    primary_key = primary_key[0]
                constrain_type = ['primary_key']
                # 建表
                tab_func.Table.create(tab_name, names_types)
                cfg.active_database.resource[cfg.active_database.table[tab_name]].add_constrain(primary_key,
                                                                                                constrain_type)
            else:
                result_list = re.findall(r'\((.*)\)', sql)[0].split(',')
                first = [result.split()[0] for result in result_list]
                last = [result.split()[1].lower() for result in result_list]
                names_ls = []
                # i = len(first)
                for i in range(0, len(first)):
                    names_ls.append(first[i])
                    names_ls.append(last[i])
                names_types = tuple(names_ls)
                # 建表
                tab_func.Table.create(tab_name, names_types)
        # except:
        #     print("[!]Error")
        #  创建视图
        elif sql_word[1] == 'view':  # create view test1 as select * from user
            view_name = sql_word[2]
            sql = ' '.join(sql_word[4:])
            search_result = query(sql)
            col_selected = sql_word[5].split(",")
            view = create_view(view_name=view_name,
                               # col_selected=col_selected,
                               search_result=search_result)
            cfg.active_database.view[view_name] = view
            print("创建视图%s成功！" % (view_name))
            print(view)
            return view
            # print(view) for debug
        # 创建索引
        elif sql_word[1] == 'index':
            return
        else:
            print("[!]Syntax Error.")
    # 查询
    elif operate == 'select':
        # 列名 res_range，表名 table_name
        # select * from Stu where Sno='95001'；
        # select Stu.Sno,SC.grade from Stu,SC where Stu.Sno=SC.Sno
        res_range = sql_word[1].split(",")
        table_name = sql_word[3]
        if len(sql_word) > 4:
            # try:
            condition = sql.split('where')[1].replace(' ', '')
            # 单条件查询 = != > < >= <=
            if len(sql_word) <= 6:
                if '.' in sql_word[5]:
                    condition_expression = sql_word[5]
                    multiple_search(selected_col=res_range, condition_expression=condition_expression)
                else:
                    res = list(condition_parse(condition))
                    col_columns = res[0]
                    key = res[1]
                    symbol = res[2]
                    # result 结果
                    result = selecting(symbol=symbol, res_range=res_range, col_columns=col_columns, key=key)
            # 多条件 and or
            elif len(sql_word) > 6:
                if sql_word[6] == 'and':
                    predicate = 'and'
                elif sql_word[6] == 'or':
                    predicate = 'or'
                condition_ls = condition.split(predicate)
                num = None
                for i in range(len(condition_ls)):
                    if '.' in condition_ls[i]:
                        num = i
                        condition_expression_1 = condition_ls[num]
                        result_1 = multiple_search(selected_col=res_range, condition_expression=condition_expression_1)
                        condition_expression_2 = condition_ls[1 - num]
                        symbol_2 = list(condition_parse(condition_expression_2))[2]
                        result = find_result(search_result=result_1, condition_expression=condition_expression_2,
                                             symbol=symbol_2, predicate=predicate)
                        # col_columns_2 = list(condition_parse(condition_ls[1-num]))[0]
                        # key_2 = list(condition_parse(condition_ls[1-num]))[1]
                        # symbol_2 = list(condition_parse(condition_ls[num]))[2]
                        # result_2 = selecting(symbol=symbol_2, res_range=res_range, col_columns=col_columns_2, key=key_2)
                if num is None:
                    col_columns_1 = list(condition_parse(condition_ls[0]))[0]
                    key_1 = list(condition_parse(condition_ls[0]))[1]
                    symbol_1 = list(condition_parse(condition_ls[0]))[2]
                    col_columns_2 = list(condition_parse(condition_ls[1]))[0]
                    key_2 = list(condition_parse(condition_ls[1]))[1]
                    symbol_2 = list(condition_parse(condition_ls[1]))[2]
                    # 分别传入两条件查询
                    result_1 = selecting(symbol=symbol_1, res_range=res_range, col_columns=col_columns_1, key=key_1)
                    result_2 = selecting(symbol=symbol_2, res_range=res_range, col_columns=col_columns_2, key=key_2)
                    # 将两结果进行处理
                    result = []
                    if predicate == 'and':
                        for row_1 in result_1:
                            for row_2 in result_2:
                                if row_1 == row_2:
                                    result.append(row_1)
                    elif predicate == 'or':
                        for row_1 in result_1:
                            for row_2 in result_2:
                                if row_1 == row_2:
                                    result.append(row_1)
                                else:
                                    result.append(row_1)
                                    result.append(row_2)
                    else:
                        print("[!]Syntax Error.")
                workaround = result.pop(0)
                result = quicksort.quicksort(items=result, col_index=num)
                result.insert(0, workaround)
            print(result)
            return result
            # 查询列名：res_range 条件列名:columns 表名:table_name 值：key 操作符：predicate 符号：symbol
        else:
            # 获取table_name表格，添加result_trimmer进行裁剪 已完成
            # 没where的情况
            # 表名：table_name  列名：columns
            # cfg.active_database.table[tab_name].add_constrain(primary_key, constrain_type)
            # result = cfg.active_database.resource[cfg.active_database.table[table_name]].find_data(
            #     col_selected=res_range)
            # return result

            # result_trimmer，将返回的数据按照col_selected分好
            # 注意！此时的result第一列被冠以行号！
            # 无where情况存在问题
            def result_trimmer(result_: list, col_selected_):
                index_selected_ = []
                now_result = []
                table_index = cfg.active_database.table[table_name]
                if col_selected_ != ['*']:
                    for name_ in col_selected_:
                        # 注意！由于传入的result第一列被冠以行号，因此列的实际位置+1
                        index_selected_.append(cfg.active_database.resource[table_index].column[name_][0] + 1)
                else:
                    col_selected_ = []
                    for name in cfg.active_database.resource[table_index].column.keys():
                        val = cfg.active_database.resource[table_index].column[name][0] + 1
                        index_selected_.append(val)
                        col_selected_.append(name)
                for row_ in result_:  # 需要加入行号,方便update等函数找到对象其位置，在select时删掉
                    now_row = [row_[0]]
                    for i in index_selected_:
                        now_row.append(row_[i])
                    now_result.append(now_row)
                # 在第0行插入表头
                workaround = col_selected_
                workaround.insert(0, 'Row ID')
                now_result.insert(0, workaround)
                return now_result

            workaround = copy.deepcopy(cfg.active_database.resource[cfg.active_database.table[table_name]].resource)
            for i in range(len(workaround)):  # 这里的行号没问题
                workaround[i].insert(0, i)
            print(result_trimmer(workaround, res_range))
            return result_trimmer(workaround, res_range)
    # values后需加空格
    elif operate == 'insert':  # INSERT INTO table_name col1=val1,col2=val2&col3=val3,col4=val4
        table_name = sql_word[2]
        """  
        #INSERT INTO table_name (select x from xx)  
        sql2 = re.findall('\((.*)\)')[0]  
        query(sql2,tag='insert')  
        """
        # 5 insert into Student1  values (8,'小红','女',20,'经济学院')
        if len(sql_word) == 5:
            values = re.findall(r'\((.*)\)', sql_word[-1])[0]
            values = values.split(',')
            values_ls = []
            for value in values:
                if "'" in value:
                    value = value.replace("'", "")
                    values_ls.append(value)
                else:
                    if '.' in value:
                        value = float(value)
                        values_ls.append(value)
                    else:
                        value = int(value)
                        values_ls.append(value)
            cfg.active_database.resource[cfg.active_database.table[table_name]].insert_data(values=values_ls)
            print("已插入一行记录")
        # 6 insert into Student1 (Sno,Sname,Ssex,Sage,Sdept) values (8,'小红','女',20,'经济学院')
        elif len(sql_word) == 6:
            values = re.findall(r'\((.*)\)', sql_word[-1])[0]
            values = values.split(',')
            values_ls = []
            for value in values:
                if "'" in value:
                    value = value.replace("'", "")
                    values_ls.append(value)
                else:
                    if '.' in value:
                        value = float(value)
                        values_ls.append(value)
                    else:
                        value = int(value)
                        values_ls.append(value)
            column_names = re.findall(r'\((.*)\)', sql_word[3])[0].split(',')
            column_names = tuple(column_names)
            cfg.active_database.resource[cfg.active_database.table[table_name]].insert_data(values=values_ls,
                                                                                            column_names=column_names)
            print("已插入一行记录")
        else:
            print("[!]Syntax Error.")
    elif operate == 'update':
        sql_splity = sql.split("'")
        table_name = sql_word[1]
        count = 0
        for i in range(1, len(sql_splity), 2):
            if ' ' in sql_splity[i]:
                count += 1

        if count > 0:
            if count > 0:
                for i in range(1, len(sql_splity), 2):
                    if ' ' in sql_splity[i]:
                        sql_splity[i] = sql_splity[i].replace(" ", "_")
                print(sql_splity)
                b = ""
                for i in sql_splity:
                    b = b + i
                sql_word = b.split(" ")
                col_name_ls = []
                value_ls = []
                set_ls = sql_word[3].split(',')
                for set in set_ls:
                    col_name_ls.append(set.split("=")[0])
                    value_ls.append(set.split("=")[1])
                # print(col_name_ls)
                # print(value_ls)
                values_ls = []
                for value in value_ls:
                    if "'" in value:
                        value = value.replace("'", "")
                        values_ls.append(value)
                    else:
                        if '.' in value:
                            value = float(value)
                            values_ls.append(value)
                        else:
                            value = int(value)
                            values_ls.append(value)
                condition = sql.split("where")[1].replace(";", "")
                select_sql = "select * from " + table_name + " where" + condition
                result = query(select_sql)
                for row in result:
                    for i in range(len(values_ls)):
                        if "_" in values_ls[i]:
                            values_ls[i] = values_ls[i].replace("_", " ")
                        cfg.active_database.resource[cfg.active_database.table[table_name]].update(row_index=row[0],
                                                                                                   col_name=col_name_ls[
                                                                                                       i],
                                                                                                   value=values_ls[i])
        else:
            col_name_ls = []
            value_ls = []
            set_ls = sql_word[3].split(',')
            for set in set_ls:
                col_name_ls.append(set.split("=")[0])
                value_ls.append(set.split("=")[1])
            # print(col_name_ls)
            # print(value_ls)
            values_ls = []
            for value in value_ls:
                if "'" in value:
                    value = value.replace("'", "")
                    values_ls.append(value)
                else:
                    if '.' in value:
                        value = float(value)
                        values_ls.append(value)
                    else:
                        value = int(value)
                        values_ls.append(value)
            condition = sql.split("where")[1].replace(";", "")
            select_sql = "select * from " + table_name + " where" + condition
            result = query(select_sql)
            result.pop(0)
            for j in range(0, len(result)):
                row = result[j]
                for i in range(len(values_ls)):
                    cfg.active_database.resource[cfg.active_database.table[table_name]].update_data(row_index=row[0],
                                                                                                    col_name=
                                                                                                    col_name_ls[i],
                                                                                                    value=values_ls[i])
    elif operate == 'delete':
        # 传索引
        table_name = sql_word[2]
        condition = sql.split("where")[1].replace(";", "")
        select_sql = "select * from " + table_name + " where" + condition
        result = query(select_sql)
        result.pop(0)
        result.pop(0)  # workaround
        for row in result:
            cfg.active_database.resource[cfg.active_database.table[table_name]].resource.pop(row[0])
    elif operate == 'drop':
        table_name = sql_word[2]
        cfg.active_database.resource[cfg.active_database.table[table_name]].delete_table()
    else:
        print("[!]Syntax Error.")

    # 在创建表时，用户需要指定以下参数：表名、（列名 数据类型，列名 数据类型）


def inited(sql: str):
    sql_ls = sql.split(";")
    sql_ls.pop(-1)
    for sql_1 in sql_ls:
        query(sql_1)


def create_table(table_name: str, names_types):
    tab_func.Table.create(table_name, names_types)


def delete_table(table_name: str):
    cfg.active_database.delete_table(table_name)


def multiple_search(selected_col: list, condition_expression: str):
    def result_trimmer(table: tab_func.Table, selected_name: list, result_: list):
        index_selected_ = []
        now_result = []
        for name_ in selected_name:
            # 注意！此时的result第一列无行号
            index_selected_.append(table.column[name_][0])
        # for row_ in result_:
        now_row = []
        for i in index_selected_:
            now_row.append(result_[i])
        print(now_row)
        return now_row

    # selected_col as ['a.col3', 'b.col4']
    # condition_expression as 'a.col1>=b.col2'
    exp_temp = condition_expression
    sym = ''
    result_pool = []
    if '<' in exp_temp:
        exp_temp.replace('<', '.')
        sym = '<'
    elif '>' in exp_temp:
        exp_temp.replace('>', '.')
        sym = '>'
    elif '<=' in exp_temp:
        exp_temp.replace('<=', '.')
        sym = '<='
    elif '>=' in exp_temp:
        exp_temp.replace('>=', '.')
        sym = '>='
    elif '=' in exp_temp:
        exp_temp.replace('>=', '.')
        sym = '=='

    # as ['a', 'col1', 'b', 'col2'] and sym='>=' from condition_expression
    if sym != '==':
        exp_temp = exp_temp.split(sym)
    else:
        exp_temp = exp_temp.split('=')
    workaround = []
    for i in range(len(exp_temp)):
        workaround += exp_temp[i].split('.')
    exp_temp = workaround
    # done exp_temp=["Ped","Pno=Stall","Pno"]，表名未成功获取
    table_a, table_b = cfg.active_database.resource[cfg.active_database.table[exp_temp[0]]], \
                       cfg.active_database.resource[cfg.active_database.table[exp_temp[2]]]
    compare_col_index_a, compare_col_index_b = table_a.column[exp_temp[1]][0], table_b.column[exp_temp[3]][0]

    # selected_col as ['a.col3', 'b.col4', 'a.col5']
    selected_temp = []
    selected_from_a, selected_from_b = [], []
    if selected_col != ['*']:
        for i in selected_col:
            # as ['a','col3','b','col4','a','col5']
            selected_temp += i.split('.')
        for i in range(0, len(selected_temp), 2):
            if selected_temp[i] == exp_temp[0]:
                # as ['col3','col5']
                selected_from_a.append(selected_temp[i + 1])
            elif selected_temp[i] == exp_temp[2]:
                # as ['col4']
                selected_from_b.append(selected_temp[i + 1])
    else:
        for col_name in table_a.column.keys():
            selected_from_a.append(col_name)
        for col_name in table_b.column.keys():
            selected_from_b.append(col_name)

    for row_a in table_a.resource:
        for row_b in table_b.resource:
            if eval('row_a[compare_col_index_a]' + sym + 'row_b[compare_col_index_b]'):
                result_pool.append(
                    result_trimmer(table_a, selected_from_a, row_a) + result_trimmer(table_b, selected_from_b, row_b))
    # 在第0行插入表头
    result_pool.insert(0, selected_from_a + selected_from_b)
    print(result_pool)
    return result_pool


# 除了前俩，后面的参和find_data其实一样
def create_view(view_name: str,
                # col_selected: list,
                search_result: list) -> list:
    # search_result.insert(0, col_selected.insert(0, 'Row ID'))  # 在开头插入表头 之前已经插入过
    search_result.insert(0, view_name)  # 在第0行插入表名,
    print(search_result)
    return search_result


def find_result(search_result: list, condition_expression: str, symbol: str, predicate: str) -> list:
    if predicate == 'and':
        condition = condition_expression.split(symbol)
        col_selected = condition[0]
        key = condition[1]
        col_name_ls = search_result[0]
        result = [col_name_ls]
        for col_name in col_name_ls:
            if col_name == col_selected:
                col_num = col_name_ls.index(col_name)
        for i in range(1, len(search_result)):
            if symbol == '>':
                if str(search_result[i][col_num]) > str(key):
                    result.append(search_result[i])
            elif symbol == '>=':
                if str(search_result[i][col_num]) >= str(key):
                    result.append(search_result[i])
            elif symbol == '<':
                if str(search_result[i][col_num]) >= str(key):
                    result.append(search_result[i])
            elif symbol == '<=':
                if str(search_result[i][col_num]) <= str(key):
                    result.append(search_result[i])
            elif symbol == '==':
                if str(search_result[i][col_num]) <= str(key):
                    result.append(search_result[i])
    elif predicate == 'or':
        # or的情况没写
        pass
    return result


def refresh():
    for table in cfg.active_database.resource:
        table.refresh()


# 将二维数组的查询结果转化为表格的形式显示
def resultStr(result: list) -> str:
    result_str = '------------------------*****------------------------\n'
    for i in result:
        for j in i:
            result_str += str(j).center(10)
        if j == i[-1]:
            result_str += '\n'
    return result_str

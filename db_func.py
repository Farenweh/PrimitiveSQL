import os
import pickle

import tab_func
import cfg


# global active_database


class Database:
    def __init__(self, db_name: str):
        self.name = db_name
        # {'表名':存放标号}
        self.table = {}
        self.view = {}
        # [表1对象,表2对象,表3对象,表4对象]
        self.resource = []
        self.path = 'data/' + db_name + '.db'
        self.view = {}

    @staticmethod
    def create(db_name: str):
        if db_name[-3:] != '.db':
            f_name = db_name + '.db'
        else:
            f_name = db_name
        if f_name not in os.listdir('data'):
            # 在data文件夹创建数据库文件，存储在其中的数据库对象为cfg.active_database
            with open('data/' + f_name, 'wb'):
                pass
                # print('数据库文件' + f_name + '已创建')
            # 创建空数据库对象并设为当前活动的数据库
            cfg.active_database = Database(db_name)
            # 把这个空数据库对象写到刚刚创建的数据库文件里
            cfg.active_database.dump()
            return True
            # print('已将' + db_name + '设为当前活动数据库')
        else:
            return False
            # print('已存在同名数据库')

    @staticmethod
    def load(db_name: str):
        if db_name[-3:] != '.db':
            f_name = db_name + '.db'
        else:
            f_name = db_name
        if f_name in os.listdir('data'):
            with open('data/' + f_name, 'rb') as active_database_file:
                cfg.active_database = pickle.load(active_database_file)
            # print('已将' + db_name + '设为当前活动数据库')
            return True
        else:
            return False
            # print('数据库' + db_name + '不存在，请检查拼写')

    # 提交更改
    def dump(self):
        with open(self.path, 'wb') as active_database_file:
            pickle.dump(self, active_database_file)
            # print('更改已提交')

    def delete_database(self):
        # global active_database
        cfg.active_database = None
        os.remove(self.path)
        return True
        # print('当前数据库已移除')

    def insert_table(self, table: tab_func.Table):
        self.table[table.name] = len(self.resource)
        # 直接把table对象放进resource末尾
        self.resource.append(table)
        print('数据表已插入')

    def delete_table(self, table_name: str):
        self.resource.pop(self.table.pop(table_name))
        print('数据表已删除')

"""
这个项目是一个简易数据库核心，应该具备遵守ORACLE SQL语法的增、查、删、改、多表连接查询、聚簇索引、散列索引、视图功能，并具备一个用户交互界面

"""
import inter_func
import cfg

if __name__ == '__main__':
    inter_func.init()
    inter_func.create_database('')
    inter_func.choose_database('debug1')
    print(cfg.active_database.name)
    print('create table debug(col1 int)')

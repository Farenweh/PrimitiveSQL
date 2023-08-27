"""
这个项目是一个简易数据库核心，应该具备遵守ORACLE SQL语法的增、查、删、改、多表连接查询、聚簇索引、散列索引、视图功能，并具备一个用户交互界面

"""
import inter_func
import cfg

if __name__ == '__main__':
    inter_func.init()
    inter_func.choose_database('debug1')

    inter_func.query("create table Ped(Pno INT,Pname CHAR,Pnum CHAR,Primary_key(Pno));")
    inter_func.query("create table Stall(Sno INT,Sprice INT,Pno INT,Primary_key(Sno));")
    inter_func.query("create table Commodity(Cno INT,Cname CHAR,Ctype CHAR,Primary_key(Cno));")
    inter_func.query("create table SC(Sno INT,Cno INT,Cprice FLOAT,Primary_key(Sno,Cno));")
    inter_func.query("insert into Ped values (1,'张三','1111');")
    inter_func.query("insert into Ped values (2,'李四','2222');")
    inter_func.query("insert into Ped values (3,'王五','3333');")
    inter_func.query("insert into Ped values (4,'张超','4444');")

    inter_func.query("insert into Stall values (1,100,1);")
    inter_func.query("insert into Stall values (2,120,2);")
    inter_func.query("insert into Stall values (3,90,3);")
    inter_func.query("insert into Stall values (4,150,4);")
    inter_func.query("insert into Stall values (5,110,4);")

    inter_func.query("insert into Commodity values (1,'白菜','叶菜类');")
    inter_func.query("insert into Commodity values (2,'生菜','叶菜类');")
    inter_func.query("insert into Commodity values (3,'韭菜','叶菜类');")
    inter_func.query("insert into Commodity values (4,'胡萝卜','根茎类');")
    inter_func.query("insert into Commodity values (5,'土豆','根茎类');")
    inter_func.query("insert into Commodity values (6,'洋葱','根茎类');")
    inter_func.query("insert into Commodity values (7,'金针菇','菌类');")
    inter_func.query("insert into Commodity values (8,'香菇','菌类');")
    inter_func.query("insert into Commodity values (9,'猪肉','肉类');")
    inter_func.query("insert into Commodity values (10,'牛肉','肉类');")

    inter_func.query("insert into SC values (1,1,1.4);")
    inter_func.query("insert into SC values (1,2,3.6);")
    inter_func.query("insert into SC values (1,3,4);")
    inter_func.query("insert into SC values (2,4,2.3);")
    inter_func.query("insert into SC values (2,5,1);")
    inter_func.query("insert into SC values (3,2,4);")
    inter_func.query("insert into SC values (3,6,0.8);")
    inter_func.query("insert into SC values (3,9,25);")
    inter_func.query("insert into SC values (4,7,8.5);")
    inter_func.query("insert into SC values (4,8,9);")
    inter_func.query("insert into SC values (4,4,2.5);")
    inter_func.query("insert into SC values (5,10,64);")
    print(cfg.active_database.resource[0].resource)
    print(cfg.active_database.resource[1].resource)
    print(cfg.active_database.resource[2].resource)
    print(cfg.active_database.resource[3].resource)

    # done 以下查询语显示多个表名或者无法显示表名
    print(inter_func.query("select * from SC"))
    print("========")
    # done 两次查询结果不一致，上次的查询会影响下一查询，疑似是查询时修改了self.resource
    inter_func.query("select * from Ped")
    inter_func.query("select * from Ped")
    print(inter_func.query("select * from Ped where Pno=1"))
    print("=======")
    print(inter_func.query("select * from SC where Cprice>4"))
    print(inter_func.query("select * from Commodity where Ctype='根茎类'"))
    # done 下一行报错：存在语法错误！，疑似在inter层的解译逻辑不对劲
    print(inter_func.query("create view view1 as select * from Ped,Stall where Sno>4 and Ped.Pno=Stall.Pno"))
    # done 下行更新多出了行号，并少了名字
    inter_func.query("update Ped set Pnum='123456' where Pname='张三'")
    inter_func.query("delete from SC where Cno=2")
    print(inter_func.query("select * from Ped"))
    print(inter_func.query("select * from SC"))
    print(cfg.active_database.resource[0].resource)
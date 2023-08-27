import re

# test = 'SC(Sno CHAR(5) ,Cno CHAR(3) , Grade int,Primary key(Sno, Cno));'
# tab_name = test.split('(')[0]
# tab = test.split()
# print(tab)
# if "Primary key" in test:
#     # 输出names_types
#     a = re.findall(r'\((.*)\)', test)[0]
#     b = a.split('Primary key')
#     names_ls = (b[0]).split(',')
#     # 删去最后的空格
#     del names_ls[-1]
#     first = [names.split()[0] for names in names_ls]
#     last = [names.split()[1].lower() for names in names_ls]
#     names_ls1 = []
#     i = len(first)
#     for i in range(0, len(first) - 1):
#         # name_list = first_names[i] + last_name[i]
#         names_ls1.append(first[i])
#         names_ls1.append(last[i])
#     names_types = tuple(names_ls1)
#
#     # 输出primary_key
#     key = re.findall(r'\((.*)\)', b[1])[0].split(',')
#     primary_key = []
#     for i in key:
#         primary_key.append(i.replace(" ", ""))
#     primary_key = tuple(primary_key)
#     # print("Found")
#
# else:
#     result_list = re.findall(r'\((.*)\)', test)[0].split(',')
#     # table_type = tuple(result_list)
#     # test1 = result_list.split(' ')
#     # print("Not Found")
#     first = [result.split()[0] for result in result_list]
#     last = [result.split()[1].lower() for result in result_list]
#     names_ls = []
#     i = len(first)
#     for i in range(0, len(first) - 1):
#         # name_list = first_names[i] + last_name[i]
#         names_ls.append(first[i])
#         names_ls.append(last[i])
#     names_types = tuple(names_ls)
# print(names_types)
# if primary_key:
#     print(primary_key)
# print(tab_name)
# i = ['sno', 'cno']
# 输出names_types
# a = result_list = re.findall(r'\((.*)\)', test)[0]
# b = a.split('Primary key')
# names_ls = (b[0]).split(',')
# # 删去最后的空格
# del names_ls[-1]
#
# # 输出primary_key
# key = re.findall(r'\((.*)\)', b[1])[0].split(',')
# primary_key = []
# for i in key:
#     primary_key.append(i.replace(" ",""))
# primary_key = tuple(primary_key)
# print(primary_key)
# print(table_type)
# print(b[0])

# sql = 'select Cno,Sno from Student where Sno=95001 and Cno=10'
# pre = 'where'
# limit = sql.split(pre)
# l = limit[1].split()
# print(l)
# print(limit)

a=1
a=str(a)
b='h'
c='='
print(a+b+c)
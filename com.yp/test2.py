# str = input("请输入：")
# print("你输入的内容是：", str)

import os

class Employee:
    empCount = 0
    __empSex = 0

    # self表示的是类的示例 不是类
    def __init__(self, name, salary):
        self.__empSex = 0
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print("total employee is ", Employee.empCount)

    def displayEmployee(self):
        print("name is %s, salary is %d" % (self.name, self.salary))

emp1 = Employee("Yinpeng", 20000)
emp1.displayCount()
emp1.displayEmployee()
emp2 = Employee("Other", 10000)
emp2.displayCount()
emp2.displayEmployee()


import re

print(re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest'))
print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配
print(re.match('com', 'www.runoob.com'))         # 不在起始位置匹配
# class Test:
#     def prt(self):
#         print(self)
#         print(self.__class__)
#
# t = Test()
# t.prt()

line = "Cats are smarter than dogs"

matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)

if matchObj:
    print("matchObj.group() : ", matchObj.group(0))
    # 返回匹配到的字符串的第一个元组
    print("matchObj.group(1) : ", matchObj.group(1))
    print("matchObj.group(2) : ", matchObj.group(2))
    # 返回匹配到的字符串的组合的元组
    print("matchObj.group(2) : ", matchObj.groups())
else:
    print("No match!!")

phone = "2004-959-559 # 这是一个电话号码"

# 删除注释
num = re.sub(r'#.*$', "", phone)
print("电话号码 : ", num)

# 移除非数字的内容
num = re.sub(r'\D', "", phone)
print("电话号码 : ", num)

def double(matched):
    value = int(matched.group('value'))
    return str(value * 2)

s = 'ABDC123456'
print(re.sub('(?P<value>\d+)', double, s))
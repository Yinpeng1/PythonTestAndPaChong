print("你好")


if True:
    print("it is true")
else:
    print("it is false")

t = 100
s = "yinpeng"
x = 103.00
print(t)
print(s[0:2])
print(x)

list = ['runoob', 786, 2.23, 'john', 70.2]
tinyList = [123, 'john']
print(list)
print(list[0:3])
print(tinyList * 2)
print(list + tinyList)
# list可以重新赋值
list.append(tinyList)
print(list)

dict = {}
dict['one'] = "This is one"
dict[2] = "This is two"

tinydict = {'name': 'john', 'code': 6734, 'dept': 'sales'}

print(dict['one'])  # 输出键为'one' 的值
print(dict[2])  # 输出键为 2 的值
print(tinydict)  # 输出完整的字典
print(tinydict.keys())  # 输出所有键
print(tinydict.values())  # 输出所有值

for key in tinydict.keys():
    if key.__eq__("code"):
        print(tinydict.get(key))

fruits = ['banana', 'apple',  'mango']
for index in range(len(tinyList)):
    print("当前值是", tinyList[index])


for num in range(10, 20):
    for i in range(2, num):
        if num % i == 0:
            j = num/i
            print("%d 等于 %d * %d" % (num, i, j))
            break
        else:
            print(num, "是一整个质数")

numbers = [12, 37, 5, 42, 8, 3]
odd = []
even = []
while len(numbers) > 0:
    number = numbers.pop()
    if number % 2 == 0:
        even.append(number)
    else:
        odd.append(number)
print(even)
print(odd)

import time;
print(time.localtime(time.time()))
print(time.asctime(time.localtime(time.time())))
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(time.time())
print(time.tzname)

import calendar

cal = calendar.month(2018, 5)
print("以下输出2016年1月份的日历:")
print(cal)

def getdate():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()));

getdate();


def change_args( str ):
    str = 20

b = 10
change_args(10)
print(b)


def printinfo(name, age):
    # "打印任何传入的字符串"
    print("Name: ", name)
    print("Age ", age)
    return;

# 调用printinfo函数
printinfo(age=50, name="miki");

def printinfo(arg1, *vartuple):
    print(arg1)
    for var in vartuple:
        print(var)
    return
printinfo(10)
printinfo(10, 20, 30, 40, 50, "nihao")

t = lambda arg1, arg2: arg1 + arg2;
print(t(10, 20))

print(globals())





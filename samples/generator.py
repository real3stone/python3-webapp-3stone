# 【高级特性-生成器】 练习

# generator生成器：一遍循环一遍计算的机制，保存的是算法
# 由于内存有限，当list太大时放不下
# 把list元素通过某种算法逐个推算出来，就不必创建完整的list，节省大量的空间

# 最难理解的就是generator和函数的执行流程不一样。
# 函数是顺序执行，遇到return语句或者最后一行函数语句就返回。
# 而generator的函数，在每次调用next()的时候执行，遇到yield语句返回，
# 再次执行时从上次返回的yield语句处继续执行

# 要理解generator的工作原理：
# 它是在for循环的过程中不断计算出下一个元素，并在适当的条件结束for循环。
# 对于函数改成的generator来说，遇到return语句或者执行到函数体最后一行语句，
# 就是结束generator的指令，for循环随之结束

# 普通函数条用直接返回结果，generator函数返回的是一个generator对象


# 杨辉三角的算法
def triangles():
    L = [1]
    i = 0
    while i < 10:
        yield L   # 使用生成器
        L = [1] + [L[i] + L[i + 1] for i in range(len(L) - 1)] + [1]
        i += 1


n = 0
results = []
for t in triangles():  # 输出生成器的前10项
    print(t)
    results.append(t)  # 拼成完整的杨辉三角
    n += 1
    if n == 10:
        break

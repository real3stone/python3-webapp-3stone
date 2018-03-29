# 【高级特性】 练习


# 寻找最大最小值
def find_min_and_max(L):
    if len(L) == 0:
        return None, None
    min_l = L[0]
    max_l = L[0]
    for x in L:
        if min_l > x:
            min_l = x
        if max_l < x:
            max_l = x
    return min_l, max_l

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
    results.append(t)
    n += 1
    if n == 10:
        break

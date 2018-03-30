# 【内建模块】
# 时间模块(datetime)
# Base64(二进制模块)
# struct(处理进制转换)
# hashlib&hmac(加密模块)
# 迭代器模块(itertools, chain, groupby)
# contexlib(简化读写文件)
# urllib(操作URL模块)--内建
# requests(同上)--第三方库
# XML(数据模块)
# HTMLParser(解析HTML网页)
# 【第三方库】
# Pillow(图像处理模块)
# chardet(字符串编码检测)
# psutil(获取系统信息--监控日志)
# virtualenv(为应用创建独立的Python运行环境)


# 集合模块
# OrderedDict在dict基础上，key值有了顺序(插入的顺序)
from collections import OrderedDict


class LastUpdatedOrderedDict(OrderedDict):

    def __init__(self, capacity):
        super(LastUpdatedOrderedDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False)
            print('remove:', last)
        if containsKey:
            del self[key]
            print('set:', (key, value))
        else:
            print('add:', (key, value))
        OrderedDict.__setitem__(self, key, value)


new_dict = LastUpdatedOrderedDict(20)

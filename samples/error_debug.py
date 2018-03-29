# 【错误\调试\测试】


try:
	print('try...')
	r = 10
	print('result:', r)
except ZeroDivisionError as e:
	print('except:', e)
except ValueError as e:
	print('ValueError', e)
else:
	print('no error')
finally:
	print('finally')

print('END')

# Python的错误其实也是class，所有的错误类型都继承自BaseException，
# 所以在使用except时需要注意的是，
# 它不但捕获该类型的错误，还把其子类也“一网打尽”


try:
	r = 10 / 0
except ValueError as e:
	print('ValueError')
except UnicodeError as e:  # 第二个except永远也捕获不到UnicodeError
	print('UnicodeError')


# 使用try...except捕获错误还有一个巨大的好处，就是可以跨越多层调用，
# 比如函数main()调用foo()，foo()调用bar()，结果bar()出错了，
# 这时，只要main()捕获到了，就可以处理


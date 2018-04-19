# 【面向对象 Object Oriented programming】笔记


# 在Python中，实例的变量名如果以__开头，就变成了一个私有变量(private),
# 只有内部可以访问，外部不能访问
# self.__name = name

# 有些时候，你会看到以一个下划线开头的实例变量名，比如_name，这样的实例变量外部是可以访问的，
# 但是，按照约定俗成的规定，当你看到这样的变量时，意思就是，“虽然我可以被访问，
# 但是，请把我视为私有变量，不要随意访问”。

# 在Python中，变量名类似__xxx__的，也就是以双下划线开头，并且以双下划线结尾的，是特殊变量，
# 特殊变量是可以直接访问的，不是private变量，所以，不能用__name__、__score__这样的变量名

# 双下划线开头的实例变量是不是一定不能从外部访问呢？其实也不是。不能直接访问__name
# 是因为Python解释器对外把__name变量改成了_Student__name，
# 所以，仍然可以通过_Student__name来访问__name变量
# 但是强烈建议你不要这么干，因为不同版本的Python解释器可能会把__name改成不同的变量名


# 学生对象
class Student(object):
	# __init__方法的第一个参数永远是self，表示创建实例本身
	# 有了__init__方法，在创建实例的时候，就不能传入空的参数了，
	# 必须传入与__init__方法匹配的参数
	def __init__(self, name, score):
		self.name = name
		self.score = score
		# self.__privateName  # private
	
	def get_grade(self):
		if self.score >= 90:
			return 'A'
		elif self.score >= 60:
			return 'B'
		else:
			return 'C'
	
	# set & check
	def set_score(self, score):
		if 0 <= score <= 100:
			self.score = score
		else:
			raise ValueError('bad score')
	
	# print
	def print_score(self):
		print('%s: %s' % (self.name, self.score))
			
bart = Student('Bart Simpson', 59)
lisa = Student('Lisa Simpson', 87)
bart.print_score()
lisa.print_score()
print(lisa.name, lisa.get_grade())
print(bart.name, bart.get_grade())


# 访问限制-作业
class Student_ex(object):

	def __init__(self, name, gender):
		self.name = name
		self.__gender = gender

	def get_gender(self):
		return self.__gender

	def set_gender(self, gender):
		if gender in ['male', 'female']:
			self.__gender = gender
		else:
			raise TypeError('bad gender')


# -----------------------多态------------------------

# 【静态语言 vs 动态语言】
# 对于静态语言（例如Java）来说，如果需要传入Animal类型，则传入的对象必须是Animal类型或者它的子类，
# 否则，将无法调用run()方法。
# 对于Python这样的动态语言来说，则不一定需要传入Animal类型。
# 我们只需要保证传入的对象有一个 run()方法 就可以了

# -----------------------判断对象类型-----------------
# type()

# isinstance()   # 能判断class的继承关系

# getattr(), setattr(), hasattr() 判断对象属性

# ------------------------------------------------------

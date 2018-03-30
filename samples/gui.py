# 【GUI编程】练习

from tkinter import *
import tkinter.messagebox as messagebox


# 实现一个简单的窗口，带有可输入的文本框


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        # 打招呼 & 退出
        self.helloLabel = Label(self, text='Hello, world!')
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()
        # 文本框输入
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alterButton = Button(self, text='Hello', command=self.hello)
        self.alterButton.pack()

    def hello(self):
        name = self.nameInput.get() or 'world'
        messagebox.showinfo('Message', 'Hello, %s' % name)

app = Application()
# 设置窗口标题
app.master.title('Hello World')
# 主消息循环
app.mainloop()


# Python内置的Tkinter可以满足基本的GUI程序的要求，
# 如果是非常复杂的GUI程序，建议用操作系统原生支持的语言和库来编写。

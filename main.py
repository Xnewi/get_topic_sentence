from DataProcessing import init_data
from Stopwords import init_Stopwords
from Stopwords import db_search_Stopwords
import tkinter
from tkinter import scrolledtext,filedialog

def process(article):
    init_data(article)
    init_Stopwords()

def from_input():
    process(textbox.get('0.0','end'))
def from_file():
    with filedialog.askopenfile(title="上传文件", filetypes=[("文本文件", ".txt")]) as f:
        process(f.read())

# 主窗口
window = tkinter.Tk()
window.title('文章中心句提取程序')
window.geometry('800x600')
window.resizable(width=False,height=False)
window.iconbitmap('icon.ico')

tkinter.Label(window,text='请输入文章：',font=('微软雅黑',14)).place(x=10,y=10,anchor='nw')
textbox = scrolledtext.ScrolledText(window,font=('微软雅黑',14))
textbox.place(x=10,y=40,anchor='nw',width = 780,height = 500)

button1 = tkinter.Button(window,text='提交',font=('微软雅黑',14),command=from_input)
button1.place(x=340,y = 550, anchor='nw',width = 120, height = 40)

button2 = tkinter.Button(window,text='上传',font=('微软雅黑',10),command=from_file)
button2.place(x=675,y = 555, anchor='nw',width = 90, height = 30)

tkinter.mainloop()

from DataProcessing import init_data
from Stopwords import init_Stopwords
from Stopwords import db_search_Stopwords
from TF_IDF import db_insert_TFIDF_WaE
import re
import sqlite3
import tkinter
from tkinter import scrolledtext,filedialog,messagebox

def get_result():
    fopen = open("article_sentences.txt", "r")
    contents = fopen.readline()

    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    max = 0
    now = 0
    result = ''
    while contents:
        now += 1
        #删除换行符
        words = re.sub("\n", "", contents)
        #将所有标点替换为空格
        words = re.sub("[\.,\?]", " ", words)
        #提取单个单词
        words = re.findall(".*?\s", words, re.S)
        sum = 0
        for item in words:
            sql = 'SELECT*FROM WaE WHERE WORD LIKE "%s";' % (item.strip())

            cur.execute(sql)
            try:
                result = cur.fetchone()[2]
            except:
                result = 0
            sum += result

        #print(contents, sum / len(words))
        try:
            if max < sum / len(words):
                max = now
        except: pass
        contents = fopen.readline()

    #print(max)
    fopenagain = open("article_sentences.txt", "r")
    for i in range(0, max):
        result = fopenagain.readline()
    return result

def process(article):
    textvar=tkinter.StringVar()
    textvar.initialize('处理中......')

    try:
        init_data(article)
        init_Stopwords()
        db_insert_TFIDF_WaE()
        result=get_result()
    except Exception as err:
        messagebox.showwarning(title='处理错误', message='处理过程有出错，检查一下文章是否符合规范！\n错误信息：' + str(err))
    else:
        messagebox.showinfo(title='找到中心句',message=result)
    var.set('😜')
    button1.config(state='active')
    button2.config(state='active')

def from_input():
    var.set('拼命处理中，客官稍等😚')
    button1.config(state='disabled')
    button2.config(state='disabled')
    process(textbox.get('0.0','end'))

def from_file():
    with filedialog.askopenfile('r',title="上传文件", filetypes=[("文本文件", ".txt")]) as f:
        textbox.delete(1.0, 'end')
        textbox.insert(1.0, f.read())

# 主窗口
window = tkinter.Tk()
window.title('文章中心句提取程序')
window.geometry('800x600')
window.resizable(width=False,height=False)
window.iconbitmap('icon.ico')

tkinter.Label(window,text='请输入文章（英文）：',font=('微软雅黑',14)).place(x=10,y=10,anchor='nw')
textbox = scrolledtext.ScrolledText(window,font=('微软雅黑',14))
textbox.place(x=10,y=40,anchor='nw',width = 780,height = 500)

var = tkinter.StringVar()
var.set('😜')
tkinter.Label(window, textvariable = var,font=('微软雅黑', 12)).place(x = 50,y = 560)

button1 = tkinter.Button(window,text='提交',font=('微软雅黑',14),command=from_input)
button1.place(x=340,y = 550, anchor='nw',width = 120, height = 40)

button2 = tkinter.Button(window,text='上传',font=('微软雅黑',10),command=from_file)
button2.place(x=675,y = 555, anchor='nw',width = 90, height = 30)

tkinter.mainloop()
from PdfScan import PdfScan
import tkinter
from tkinter import scrolledtext, filedialog, messagebox, Menu
from sentences_vec import Process
from AP import AP
from if_idf_remastered import TF_IDF

def process(article):
    try:
        if alvar.get() == 'AP':
            deal = Process(article)
            deal.init()
            ap = AP(deal)
            msg = '可能的中心句：\n'
            for i in ap.centers:
                msg += deal.sentences[i] + '\n'
            ap.reset()
        else:
            deal = TF_IDF(article)
            deal.init()
            msg = '可能的中心句：\n'
            for e in deal.sorted_sentences_scores[:3]:
                msg += e + '\n'
    except Exception as err:
        messagebox.showwarning(
            title='处理错误', message='处理过程有出错，检查一下文章是否符合规范！\n错误信息：' + str(err))
    else:
        messagebox.showinfo(title='找到中心句', message=msg)
    button1.config(state='active')
    button2.config(state='active')


def from_input():
    button1.config(state='disabled')
    button2.config(state='disabled')
    process(textbox.get('0.0', 'end'))


def from_file():
    textbox.delete(1.0, 'end')
    filepath = filedialog.askopenfilename()
    if filepath[-4:] == ".pdf":
        pdf = PdfScan()
        pdf.load(filepath)
        for i in range(0, pdf.get_total_pages()):
            textbox.insert('end', pdf.get_optimized_content(i))
    elif filepath[-4:] == ".txt":
        f = open(filepath, 'r', encoding='utf-8')
        textbox.insert('end', f.read())
        f.close()
    else:
        messagebox.showwarning(title='文件格式错误', message='请上传txt或pdf文件')


# 主窗口
window = tkinter.Tk()

window.title('文章中心句提取程序')
window.geometry('800x600')
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
x = (screenwidth - 800) / 2
y = (screenheight - 600) / 2
window.geometry("%dx%d+%d+%d" % (800, 600, x, y))
window.minsize(800, 600)
window.maxsize(screenwidth, screenheight)
window.resizable(width=True, height=True)
window.iconbitmap('icon.ico')
window.update()

label1 = tkinter.Label(window, text='请输入文章（英文）：', font=('微软雅黑', 14)).place(x=10, y=10, anchor='nw')
textbox = scrolledtext.ScrolledText(window, font=('微软雅黑', 14))
textbox.place(relx=0.0125, rely=0.0667, anchor='nw', relwidth=0.975, relheight=0.8)

button1 = tkinter.Button(window, text='提交', font=('微软雅黑', 14), command=from_input)
button1.place(relx=0.5, rely=0.935, anchor='center', width=120, height=40)

button2 = tkinter.Button(window, text='上传', font=('微软雅黑', 10), command=from_file)
button2.place(relx=0.915, rely=0.935, anchor='center', width=90, height=30)

alvar = tkinter.StringVar()
alvar.set('AP')
def changeal():
    if alvar.get() == 'AP':
        alvar.set('TF-IDF')
    else:
        alvar.set('AP')

button3 = tkinter.Button(window, textvar=alvar, font=('微软雅黑', 10), command=changeal)
button3.place(relx=0.085, rely=0.935, anchor='center', width=90, height=30)

tkinter.mainloop()

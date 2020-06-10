from PdfScan import PdfScan
import tkinter
from tkinter import scrolledtext, filedialog, messagebox
from NLTKProcessing import Process
from AP import AP

def process(article):
    textvar = tkinter.StringVar()
    textvar.initialize('处理中......')

    try:
        deal = Process(article)
        deal.init()
        ap = AP(deal)
        msg = '可能的中心句：\n'
        for i in ap.centers:
            msg += deal.sentences[i] + '\n'
        ap.reset()
    except Exception as err:
        messagebox.showwarning(
            title='处理错误', message='处理过程有出错，检查一下文章是否符合规范！\n错误信息：' + str(err))
    else:
        messagebox.showinfo(title='找到中心句', message=msg)
    var.set('')
    button1.config(state='active')
    button2.config(state='active')


def from_input():
    var.set('拼命处理中，客官稍等')
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
window.resizable(width=False, height=False)
window.iconbitmap('icon.ico')

tkinter.Label(window, text='请输入文章（英文）：', font=(
    '微软雅黑', 14)).place(x=10, y=10, anchor='nw')
textbox = scrolledtext.ScrolledText(window, font=('微软雅黑', 14))
textbox.place(x=10, y=40, anchor='nw', width=780, height=500)

var = tkinter.StringVar()
var.set('')
tkinter.Label(window, textvariable=var, font=('微软雅黑', 12)).place(x=50, y=560)

button1 = tkinter.Button(window, text='提交', font=(
    '微软雅黑', 14), command=from_input)
button1.place(x=340, y=550, anchor='nw', width=120, height=40)

button2 = tkinter.Button(
    window, text='上传', font=('微软雅黑', 10), command=from_file)
button2.place(x=675, y=555, anchor='nw', width=90, height=30)

tkinter.mainloop()

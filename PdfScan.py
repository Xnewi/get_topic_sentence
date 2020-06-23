import PyPDF2
import re


class PdfScan():
    def __init__(self):
        pass

    def load(self, filename):
        '''初始化：提供pdf文件名称'''
        # 以二进制的方式打开指定pdf文件
        pdfFile = open(filename, 'rb')
        self.pdfReader = PyPDF2.PdfFileReader(pdfFile)

    def get_total_pages(self):
        '''获取pdf总页数'''
        return self.pdfReader.numPages

    def get_page_content(self, page_number):
        '''获取指定页内容'''
        return self.pdfReader.getPage(page_number).extractText()

    def get_optimized_content(self, page_number):
        '''获取指定页经过优化的内容'''
        contents = self.get_page_content(page_number)
        # 将单词的多个空格替换为单个空格
        contents = re.sub("\s+", " ", contents)
        # 将断掉的连字符接起来
        # eg: happy- birthday! -> happy-birthday!
        contents = re.sub("- ", "-", contents)
        contents = re.sub(" -", "-", contents)

        return contents

    def page_number_return_SEfunction(self, stri):
        def analyze(exp):
            data = []
            if '-' in exp:
                first = re.findall('\d-', exp)
                last = re.findall('-\d', exp)
                first = int(first[0][:-1])
                last = int(last[0][1:])
                step = -1 if first > last else 1
                for i in range(first, last + step, step):
                    data.append(i - 1)
            else:
                data.append(int(exp) - 1)
            return data
        result = []
        stri = re.sub(' ', '', stri)
        stri = re.sub('，', ',', stri)
        if stri == '':
            result = range(self.get_total_pages())
        else:
            last = 0
            for i in range(len(stri)):
                if stri[i] == ',':
                    substr = stri[last:i]
                    result.extend(analyze(substr))
                    last = i + 1
                elif i == len(stri) - 1:
                    substr = stri[last:]
                    result.extend(analyze(substr))
        for e in result:
            if e >= self.get_total_pages() or e < 0:
                raise IndexError("页码下标越界")
        return result

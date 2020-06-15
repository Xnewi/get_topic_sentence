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

    def page_number_return_SEfunction(self, command):
        if command == '':
            result = range(self.get_total_pages())
        else:
            com = re.sub('-', ' ', command)
            first = re.findall('\d ', com)
            last = re.findall(' \d', com)
            first = str(first[0]).strip()
            last = str(last[0]).strip()

            result = []
            for i in range(int(first), int(last)+1):
                result.append(i - 1)
        return result

import PyPDF2


class PdfScan():
    def __init__(self, filename):
        '''初始化：提供pdf文件名称'''
        # 以二进制的方式打开指定pdf文件
        pdfFile = open(filename, 'rb')
        self.pdfReader = PyPDF2.PdfFileReader(pdfFile)

    def get_total_pages(self):
        '''获取pdf总页数'''
        return self.pdfReader.numPages

    def get_page_content(self, page_number):
        '''获取指定页内容'''
        page = self.pdfReader.getPage(page_number)
        return page.extractText()


test = PdfScan("(1958)Luhn.pdf")
print(test.get_page_content(0))

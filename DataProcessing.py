import re
import sqlite3
from Stopwords import remove_stopwords_from_words

def article_init(contents):
    '''文献原文预处理'''
    fwrite = open("article_processed.txt", "w")

    #全文转化为小写
    contents = contents.lower()
    #删除"
    contents = re.sub("\"", "", contents)
    #替换;为,
    contents = re.sub(";", ",", contents)
    #替换!/?为.
    contents = re.sub("[!\?]", ".", contents)


    fwrite.write(contents)


def article_transform_to_sentences(article):
    '''用于把原文拆分为短句'''

    #文献原文预处理
    article_init(article)

    fopen = open("article_processed.txt", "r")
    contents = fopen.read()
    fwrite = open("article_sentences.txt", "w")


    #匹配出以标点结尾的句子
    sentences = re.findall(".*?[\.,\?]", contents, re.S)
    #去除空格、加上换行符
    for i in range(len(sentences)):
        fwrite.write(str(sentences[i]).strip() + "\n")


def sentences_transform_to_words():
    '''用于把短句拆分为单词'''

    fopen = open("article_sentences.txt", "r")
    contents = fopen.read()
    fwrite = open("article_words.txt", "w")

    #删除换行符
    words = re.sub("\n", "", contents)
    #将所有标点替换为空格
    words = re.sub("[\.,\?]", " ", words)
    #提取单个单词
    words = re.findall(".*?\s", words, re.S)

    for i in range(len(words)):
        fwrite.write(str(words[i]) + " ")

def db_create_WaE():
    '''
    创建表WaE
    LP = Language Processing
    WaE = Words and Expressions
    '''

    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    sql = '''CREATE TABLE WaE(WORD CHAR(50) PRIMARY KEY NOT NULL, QUANTITY INT NOT NULL);'''
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()


def db_insert_WaE(word, quantity):
    '''向表WaE中压入数据'''

    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    #新增
    sql1 = 'INSERT INTO WaE(WORD, QUANTITY) VALUES("%s", %s);' % (word, quantity)
    #修改
    sql2 = 'UPDATE WaE SET QUANTITY = %s WHERE WORD = "%s";' % (quantity, word)
    try:
        cur.execute(sql1)
        db.commit()
    except:
        db.rollback()
        cur.execute(sql2)
        db.commit()

    db.close()


def words_count():
    '''单词计数并将数据压入表WaE中'''

    fopen = open("article_sentences.txt", "r")
    contents = fopen.read()

    #将单词间均替换为空格
    words = re.sub("[\.,\?]\n", " ", contents)
    #把单词拉入到words列表中
    words = re.findall("\w+", words, re.S)

    #将list转为set
    s = set(words)
    #删除停止词
    s = list(s)
    remove_stopwords_from_words(s)

    #空字典
    dict = {}
    #统计元素个数
    for item in s:
        dict.update({item: words.count(item)})
    #压入数据
    for key, value in dict.items():
        db_insert_WaE(key, value)


def db_recreate_WaE():
    '''重新创建表WaE'''

    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    sql = '''DROP TABLE WaE;'''
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()
    db_create_WaE()


def init_data(article):
    db_recreate_WaE()
    db_create_WaE()

    article_transform_to_sentences(article)
    sentences_transform_to_words()

    words_count()
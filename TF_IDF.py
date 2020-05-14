import sqlite3
import re
import math

def word_frequency(word):
    '''在表wae中计算词频'''
    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    #选取
    sql = 'SELECT*FROM WaE WHERE WORD LIKE "%s";' % (word)
    cur.execute(sql)
    result = cur.fetchone()
    db.close()
    try:
        return result[1]
    except:
        return 0


def total_word():
    '''获取词汇总数'''
    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    #新增
    sql = 'SELECT*FROM WaE;'
    cur.execute(sql)
    result = cur.fetchall()
    db.close()
    return len(result)


def db_create_COCA():
    '''创建表COCA'''
    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    sql = '''CREATE TABLE COCA(WORD CHAR(50) PRIMARY KEY NOT NULL, RANK INT NOT NULL);'''
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()


def db_insert_COCA(word, rank):
    '''向表COCA中压入数据'''
    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    #新增
    sql = 'INSERT INTO COCA(WORD, RANK) VALUES("%s", %s);' % (word, rank)
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()
    

def db_init_COCA():
    '''从txt文件初始化表COCA'''

    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    fopen = open("coca.txt", "r")
    contents = fopen.readline()

    while contents:
        #删掉换行符
        contents = re.sub("\n", "", contents)
        #拿出单词
        coca = re.search(".*?\s", contents, re.S)[0].strip()
        #拿出排名
        rank = int(re.search("\d+", contents, re.S)[0])

        #压入数据
        #新增
        sql = 'INSERT INTO COCA(WORD, RANK) VALUES("%s", %s);' % (coca, rank)
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()

        contents = fopen.readline()
    db.close()


def TF_cal(word):
    '''计算词频'''
    return word_frequency(word) / total_word()


def IDF_cal(word):
    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    #查询
    sql = 'SELECT*FROM COCA WHERE WORD LIKE "%s";' % (word)
    cur.execute(sql)
    result = cur.fetchone()
    db.close()
    try:
        return result[1]
    except:
        return 100


def TF_IDF_cal(word):
    '''计算TF-IDF'''
    return TF_cal(word) * IDF_cal(word)


def db_insert_TFIDF_WaE():
    '''向表WaE中压入TFIDF数据'''
    db = sqlite3.connect("PythonLP.db")
    cur = db.cursor()

    sql = 'SELECT*FROM WaE;'
    cur.execute(sql)
    result = cur.fetchall()
    for item in result:
        #修改
        sql = 'UPDATE WaE SET TFIDF = %s WHERE WORD = "%s";' % (TF_IDF_cal(item[0]), item[0])
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()

    db.close()

# 运行一次生成数据库
if __name__ == "__main__":
    db_create_COCA()
    db_init_COCA()
    # db_insert_TFIDF_WaE()
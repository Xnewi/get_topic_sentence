import re
import sqlite3
from Stopwords import remove_stopwords_from_words


class Article():
    def __init__(self, txt):
        '''
        获取文章
        @para txt 文本
        '''
        self.contents = txt
        self.pretreated_contents = txt
        self.sentences = []
        self.words = []

    def arti_pretreat(self):
        '''文献原文预处理'''
        fwrite = open("article_processed.txt", "w")

        # 全文转化为小写
        self.pretreated_contents = self.contents.lower()
        # 删除"
        self.pretreated_contents = re.sub("\"", "", self.pretreated_contents)
        # 替换;为,
        self.pretreated_contents = re.sub(";", ",", self.pretreated_contents)
        # 替换!/?为.
        self.pretreated_contents = re.sub(
            "[!\?]", ".", self.pretreated_contents)

        # 写入文件article_processed.txt
        fwrite.write(self.pretreated_contents)

    def arti_transform_to_sentences(self):
        '''把原文拆分为短句'''
        # 文献原文预处理
        self.arti_pretreat()

        fwrite = open("article_sentences.txt", "w")

        # 匹配出以标点结尾的句子
        sentences = re.findall(".*?[\.,\?]", self.pretreated_contents, re.S)
        # 去除空格、加上换行符
        for i in range(len(sentences)):
            fwrite.write(str(sentences[i]).strip() + "\n")
            self.sentences.append(str(sentences[i]).strip())

    def arti_transform_to_words(self):
        '''把原文拆分为单词'''
        # 文献原文预处理
        self.arti_pretreat()

        fwrite = open("article_words.txt", "w")

        # 删除换行符
        words = re.sub("\n", "", self.pretreated_contents)
        # 将所有标点替换为空格
        words = re.sub("[\.,\?]", "", words)
        # 提取单个单词
        words = re.findall(".*?\s", words, re.S)

        for i in range(len(words)):
            fwrite.write(str(words[i]) + " ")
            self.words.append(str(words[i]).strip())


class DB_WaE():
    def __init__(self):
        self.db = sqlite3.connect("PythonLP.db")
        self.cur = self.db.cursor()

    def WaE_create(self):
        '''创建表WaE'''
        sql = '''CREATE TABLE WaE(WORD CHAR(50) PRIMARY KEY NOT NULL, QUANTITY INT NOT NULL, TFIDF REAL);'''
        try:
            self.cur.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def WaE_insert(self, word, quantity):
        '''向表WaE中压入数据'''
        # 新增
        sql1 = 'INSERT INTO WaE(WORD, QUANTITY, TFIDF) VALUES("%s", %s, 0);' % (
            word, quantity)
        # 修改
        sql2 = 'UPDATE WaE SET QUANTITY = %s WHERE WORD = "%s";' % (
            quantity, word)
        try:
            self.cur.execute(sql1)
            self.db.commit()
        except:
            self.db.rollback()
            self.cur.execute(sql2)
            self.db.commit()

    def WaE_recreate(self):
        '''重新创建表WaE'''

        sql = '''DROP TABLE WaE;'''
        try:
            self.cur.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

        #创建表WaE
        self.WaE_create()

    def WaE_words_count(self, words):
        '''
        单词计数并将数据压入表WaE中
        @para words 单词表
        '''
        # 将list转为set
        s = set(words)
        #再把set转回list
        s = list(s)
        # 删除停止词
        remove_stopwords_from_words(s)

        # 空字典
        words_dict = {}
        # 统计元素个数
        for item in s:
            words_dict.update({item: words.count(item)})
        # 压入数据
        for key, value in words_dict.items():
            self.WaE_insert(key, value)


def article_init(contents):
    '''文献原文预处理'''
    fwrite = open("article_processed.txt", "w")

    # 全文转化为小写
    contents = contents.lower()
    # 删除"
    contents = re.sub("\"", "", contents)
    # 替换;为,
    contents = re.sub(";", ",", contents)
    # 替换!/?为.
    contents = re.sub("[!\?]", ".", contents)

    fwrite.write(contents)


def article_transform_to_sentences(article):
    '''用于把原文拆分为短句'''
    # 文献原文预处理
    article_init(article)

    fopen = open("article_processed.txt", "r")
    contents = fopen.read()
    fwrite = open("article_sentences.txt", "w")

    # 匹配出以标点结尾的句子
    sentences = re.findall(".*?[\.,\?]", contents, re.S)
    # 去除空格、加上换行符
    for i in range(len(sentences)):
        fwrite.write(str(sentences[i]).strip() + "\n")


def sentences_transform_to_words():
    '''用于把短句拆分为单词'''
    fopen = open("article_sentences.txt", "r")
    contents = fopen.read()
    fwrite = open("article_words.txt", "w")

    # 删除换行符
    words = re.sub("\n", "", contents)
    # 将所有标点替换为空格
    words = re.sub("[\.,\?]", " ", words)
    # 提取单个单词
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

    sql = '''CREATE TABLE WaE(WORD CHAR(50) PRIMARY KEY NOT NULL, QUANTITY INT NOT NULL, TFIDF REAL);'''
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

    # 新增
    sql1 = 'INSERT INTO WaE(WORD, QUANTITY, TFIDF) VALUES("%s", %s, 0);' % (
        word, quantity)
    # 修改
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

    # 将单词间均替换为空格
    words = re.sub("[\.,\?]\n", " ", contents)
    # 把单词拉入到words列表中
    words = re.findall("\w+", words, re.S)

    # 将list转为set
    s = set(words)
    # 删除停止词
    s = list(s)
    remove_stopwords_from_words(s)

    # 空字典
    dict = {}
    # 统计元素个数
    for item in s:
        dict.update({item: words.count(item)})
    # 压入数据
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
    #db_recreate_WaE()
    #db_create_WaE()

    #article_transform_to_sentences(article)
    #sentences_transform_to_words()

    #words_count()

    wae = DB_WaE()
    wae.WaE_create()

    arti = Article(article)
    arti.arti_transform_to_sentences()
    arti.arti_transform_to_words()

    wae.WaE_words_count(arti.words)

test = Article('''I'M GOING RUNNING TODAY. I am not concerned about my calorie consumption for the day, nor am I anxious to get in shape for the winter season. I just want to go running.

I used to dislike running. "If you don't win this game, you're all running five miles tomorrow," the field hockey coach used to warn, during those last days of October when the average temperature seemed to be decreasing exponentially. And so, occasionally, my grief-stricken team would run numerous miserable laps around the fields. At the end of these excursions, our faces and limbs would be numb, and we would all have developed those notorious flu-like symptoms; but the running made us better in the long run, I suppose. Nevertheless, I counted down the days until the end of the field hockey season, vowing never to put on a pair of running shoes again. Then I surprised myself by signing up for outdoor track in the second half of sophomore year. I was foolish to have believed that I could ever escape this insidious and magnetic addiction.

Anyone would have thought that I'd be off the team in a few days, but the last week of January caught me splashing through puddles of melted ice, and February winds nearly blew me off the track. I looked forward to practices this time around, to the claps and the persistent cheers of my fellow trackies. I was feeling a "runner's high" spurred by the endorphins released by exercise. But to attribute my affinity for running solely to chemistry diminishes the personal importance that running has for me. I like running-in the cool shade of the towering oak trees, and in the warm sunlight spilling over the horizon, and in the drops of rain falling gently from the clouds. Certain things become clear to me when I'm running—only while running did I realize that "hippopotami" is possibly the funniest word in the English language, and only while running did I realize that the travel section of The York Times does not necessarily provide an accurate depiction of the entire world. Running lends me precious moments to contemplate my life: while running I find time to dream about changing the world, to think about recent death of a classmate, or to wonder about the secret to college admission.

Running is the awareness of hurdles between me and the finish line; running is the desire to overcome them. Running is putting up with aches and pains, relishing the knowledge that, in the end, I will have built strength and endurance. Running is the instant clarity of vision with which I can see my future just one hundred yards in the distance; it is the understanding that these crucial steps will determine victory or defeat.

Running is not the most important thing in the world to me, but it is what fulfills me when time permits.And right now, before the sun goes down, I like to take advantage of the road that lies ahead. ''')

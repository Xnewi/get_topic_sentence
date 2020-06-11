import nltk
from math import sqrt
from nltk.corpus import wordnet
from DataProcessing import Article
from nltk import word_tokenize

class Process():
    def __init__(self, contents):
        self.text = contents  # 原文本
        self.sentences = []  # 源文本-句子
        self.sentences_vec = []  # 源文本-句子-向量
        self.tokenized_text = []  # 源文本-分词
        self.tokenized_sentences_text = []  # 源文本-句子-分词
        self.corpus = set()  # 源文本-语料库
        self.corpus_dict = {}  # 源文本-语料库-数字映射

    def init(self):
        '''在使用其他函数前先使用，请务必调用'''
        self.sentences = []  # 源文本-句子
        self.sentences_vec = []  # 源文本-句子-向量
        self.tokenized_text = []  # 源文本-分词
        self.tokenized_sentences_text = []  # 源文本-句子-分词
        self.corpus = set()  # 源文本-语料库
        self.corpus_dict = {}  # 源文本-语料库-数字映射
        # 变为小写文本
        self.text = self.text.lower()
        # 其他初始化
        self.sentences_init()
        self.sentences_init()
        self.tokenize()
        self.vec_create()
        # 句子向量初始化，必须放在最后初始化
        self.sentences_vec_init()

    def sentences_init(self):
        '''分句，不必手动调用'''
        temp = Article(self.text)
        temp.arti_transform_to_sentences()
        self.sentences = temp.sentences

        self.tokenized_sentences_text = [[word for word in word_tokenize(
            sentence)] for sentence in self.sentences]

    def how_many_sentences(self):
        return len(self.sentences)

    def tokenize(self):
        '''分词，不必手动调用'''
        self.tokenized_text = nltk.word_tokenize(self.text)

    def vec_create(self):
        '''建立向量表示，不必手动调用'''
        # 建立语料库
        all_list = []
        for text in self.tokenized_text:
            all_list.append(text)
        self.corpus = set(all_list)

        # 建立语料库的数字映射
        self.corpus_dict = dict(zip(self.corpus, range(len(self.corpus))))

    def vector_rep(self, n):
        '''
        生成单句向量，不必手动调用
        @param n, type int: 第n个句子
        查询句子总数可使用how_many_sentences()
        '''
        self.vec_create()
        vec = []
        for key in self.corpus_dict.keys():
            if key in self.tokenized_sentences_text[n]:
                vec.append(
                    (self.corpus_dict[key], self.tokenized_sentences_text[n].count(key)))
            else:
                vec.append((self.corpus_dict[key], 0))

        vec = sorted(vec, key=lambda x: x[0])
        return vec

    def sentences_vec_init(self):
        '''句子向量初始化，不必手动调用'''
        for i in range(0, self.how_many_sentences()):
            self.sentences_vec.append(self.vector_rep(i))

    def similarity_compare(self, n1, n2):
        '''
        返回两句子的余弦相似度
        @param n1, type int: 一个句子的序号
        @param n2, type int: 另一个句子的序号
        序号: 0 to how_many_sentences() - 1
        '''
        vec1 = self.sentences_vec[n1]
        vec2 = self.sentences_vec[n2]
        inner_product = 0
        square_length_vec1 = 0
        square_length_vec2 = 0
        for tup1, tup2 in zip(vec1, vec2):
            inner_product += tup1[1]*tup2[1]
            square_length_vec1 += tup1[1]**2
            square_length_vec2 += tup2[1]**2

        return (inner_product/sqrt(square_length_vec1*square_length_vec2))

class WD():
    def __init__(self, word):
        self.word = word

    def means(self):
        '''返回单词的所有意思'''
        return wordnet.synsets(self.word)

    def definition(self, str1, str2):
        '''
        返回单词的指定定义
        @param str1, type str: 单词的词性
        @param str2, type str: 词性序号
        '''
        valid_str = '''%s.%s.%s''' % (self.word, str1, str2)
        return wordnet.synset(valid_str).definition()

    def examples(self, str1, str2):
        '''
        返回单词的例句
        @param str1, type str: 单词的词性
        @param str2, type str: 词性序号
        '''
        valid_str = '''%s.%s.%s''' % (self.word, str1, str2)
        return wordnet.synset(valid_str).examples()

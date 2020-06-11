import string
import nltk
import math
from collections import Counter
from nltk.corpus import stopwords
from gensim import corpora, models, matutils


class TF_IDF():
    def __init__(self, contents):
        self.text = contents  # 原文本
        self.sentences = []  # 源文本-句子
        # self.sentences_vec = []  # 源文本-句子-向量
        self.tokenized_text = []  # 源文本-分词
        # self.tokenized_sentences_text = []  # 源文本-句子-分词
        # self.corpus = set()  # 源文本-语料库
        # self.corpus_dict = {}  # 源文本-语料库-数字映射
        self.tokens = []
        self.dict = Counter()

        self.nostopwords_tokenized_text = []
        self.sorted_word_scores = {}
        self.sorted_sentences_scores = {}

    def init(self):
        self.tokens_init()
        self.dict_init()
        self.nostopwords_tokenized_text_init()
        self.scores_init()

    def tokens_init(self):
        '''原文本分词 + 分句'''
        self.text = self.text.lower()
        # 删掉所有换行符
        self.text = self.text.replace('\n', '')
        # 分句
        self.sentences = nltk.sent_tokenize(self.text)
        # 分词
        self.tokenized_text = nltk.word_tokenize(self.text)

        for sentence in self.sentences:
            for word in self.tokenized_text:
                # 去掉标点符号
                if word not in string.punctuation:
                    self.tokens.append(word)

    def scores_init(self):
        '''计算文章单词分数和每句分数'''
        # 单词分数
        word_scores = {word: self.tfidf_cal(
            word) for word in self.dict}
        self.sorted_word_scores = sorted(
            word_scores.items(), key=lambda x: x[1], reverse=True)

        # 句子分数
        sentence_scores = {}
        for i in range(0, len(self.sentences)):
            # 先拆句子成词
            sentence_tokenized = nltk.word_tokenize(self.sentences[i])

            # print(type(self.nostopwords_tokenized_text))
            # print(type(self.sorted_word_scores))
            # print(self.sorted_word_scores)
            # print(sentence_tokenized)

            score = 0
            for word in sentence_tokenized:

                #停止词: 零分
                if word not in self.nostopwords_tokenized_text:
                    score += 0
                # 非停止词: 加分~
                else:
                    score += word_scores[word]

                sentence_scores[self.sentences[i]] = score / \
                    (len(sentence_tokenized))

        self.sorted_sentences_scores = sorted(
            sentence_scores.items(), key=lambda x: x[1], reverse=True)

    def nostopwords_tokenized_text_init(self):
        '''分词（去掉所有stopword）'''
        self.nostopwords_tokenized_text = [
            word for word in self.tokens if not word in stopwords.words('english')]

    def dict_init(self):
        # 去除停用词
        filtered = [word for word in self.tokens if not word in stopwords.words(
            'english')]
        # 统计每个单词的出现次数
        self.dict = Counter(filtered)

    def containing_cal(self, word):
        return sum(1 for self.dict in self.nostopwords_tokenized_text if word in self.dict)

    def tf_cal(self, word):
        '''计算指定词的tf'''
        self.dict_init()
        return self.dict[word] / sum(self.dict.values())

    def idf_cal(self, word):
        '''计算指定词的idf'''
        return math.log2(len(self.nostopwords_tokenized_text) / (self.containing_cal(word)))

    def tfidf_cal(self, word):
        '''计算tfidf'''
        return self.tf_cal(word) * self.idf_cal(word)

    def tfidf_words_top(self, n):
        '''获取文章排名前n的单词及其分数'''
        result = {}
        for word, score in self.sorted_word_scores[:n]:
            result[word] = score
        return result


text1 = """
Football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal. 
Unqualified, the word football is understood to refer to whichever form of football is the most popular 
in the regional context in which the word appears. Sports commonly called football in certain places 
include association football (known as soccer in some countries); gridiron football (specifically American 
football or Canadian football); Australian rules football; rugby football (either rugby league or rugby union); 
and Gaelic football. These different variations of football are known as football codes.
"""
test = TF_IDF(text1)
test.init()
print(test.sorted_sentences_scores)
print(test.sentences)

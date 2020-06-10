import string
import nltk
import math
from collections import Counter
from nltk.corpus import stopwords
from gensim import corpora, models, matutils

text1 = """
Football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal. 
Unqualified, the word football is understood to refer to whichever form of football is the most popular 
in the regional context in which the word appears. Sports commonly called football in certain places 
include association football (known as soccer in some countries); gridiron football (specifically American 
football or Canadian football); Australian rules football; rugby football (either rugby league or rugby union); 
and Gaelic football. These different variations of football are known as football codes.
"""



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

    def init(self):
        self.tokens_init()
        self.dict_init()
        self.nostopwords_tokenized_text_init()

    def tokens_init(self):
        '''原文本分词 + 分句'''
        self.text=self.text.lower()
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

    def tfidf_top(self, n):
        '''获取文章排名前n的单词及其分数'''
        word_scores = {word: self.tfidf_cal(word) for word in self.dict}
        sorted_word_scores = sorted(
            word_scores.items(), key=lambda x: x[1], reverse=True)
        
        result = {}
        for word, score in sorted_word_scores[:n]:
            result[word] = score
        return result


test = TF_IDF(text1)
test.init()
#print(t3.count)
#print(t3.count["across"])
#print(t3.count["by"])

print(test.dict)
#print(test.tfidf_top(3))

# print(test.sentences)
# print(test.tokenized_text)
# print(test.count)
# print(test.nostopwords_tokenized_text)

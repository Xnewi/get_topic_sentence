import nltk
from math import sqrt
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from DataProcessing import Article
from nltk import word_tokenize

test_text = '''I'M GOING RUNNING TODAY. I am not concerned about my calorie consumption for the day, nor am I anxious to get in shape for the winter season. I just want to go running.

I used to dislike running. "If you don't win this game, you're all running five miles tomorrow," the field hockey coach used to warn, during those last days of October when the average temperature seemed to be decreasing exponentially. And so, occasionally, my grief-stricken team would run numerous miserable laps around the fields. At the end of these excursions, our faces and limbs would be numb, and we would all have developed those notorious flu-like symptoms; but the running made us better in the long run, I suppose. Nevertheless, I counted down the days until the end of the field hockey season, vowing never to put on a pair of running shoes again. Then I surprised myself by signing up for outdoor track in the second half of sophomore year. I was foolish to have believed that I could ever escape this insidious and magnetic addiction.

Anyone would have thought that I'd be off the team in a few days, but the last week of January caught me splashing through puddles of melted ice, and February winds nearly blew me off the track. I looked forward to practices this time around, to the claps and the persistent cheers of my fellow trackies. I was feeling a "runner's high" spurred by the endorphins released by exercise. But to attribute my affinity for running solely to chemistry diminishes the personal importance that running has for me. I like running-in the cool shade of the towering oak trees, and in the warm sunlight spilling over the horizon, and in the drops of rain falling gently from the clouds. Certain things become clear to me when I'm running—only while running did I realize that "hippopotami" is possibly the funniest word in the English language, and only while running did I realize that the travel section of The York Times does not necessarily provide an accurate depiction of the entire world. Running lends me precious moments to contemplate my life: while running I find time to dream about changing the world, to think about recent death of a classmate, or to wonder about the secret to college admission.

Running is the awareness of hurdles between me and the finish line; running is the desire to overcome them. Running is putting up with aches and pains, relishing the knowledge that, in the end, I will have built strength and endurance. Running is the instant clarity of vision with which I can see my future just one hundred yards in the distance; it is the understanding that these crucial steps will determine victory or defeat.

Running is not the most important thing in the world to me, but it is what fulfills me when time permits.And right now, before the sun goes down, I like to take advantage of the road that lies ahead. '''


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

        self.text = contents  # 原文本
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


test = Process(test_text)
test.init()
# print(test.corpus_dict)
# print(test.sentences)
# print(test.vector_rep(49))
print(len(test.sentences_vec))
print(test.similarity_compare(49, 1))

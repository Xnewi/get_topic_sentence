import numpy

class AP:
    # 相似度矩阵
    ma_sim = []
    # 代表矩阵
    ma_res = []
    # 适选矩阵
    ma_ava = []
    # 矩阵大小
    size = 0
    # 衰减系数
    lamda = 0.5
    # 聚类中心
    centers = []

    def __init__(self, data):
        self.size = data.how_many_sentences()
        self.ma_sim = self.GetSimMatrix(data)
        self.ma_res = numpy.zeros_like(self.ma_sim)
        self.ma_ava = numpy.zeros_like(self.ma_sim)
        self.cal()

    # 得到相似度矩阵
    def GetSimMatrix(self, data):
        matrix = []
        for i in range(self.size):
            matrix.append([])
            for j in range(self.size):
                matrix[i].append(data.similarity_compare(i, j) - 1)
                if i == j:
                    matrix[i][j] = -1
        return matrix

    # 迭代
    def cal(self):
        max_iter = 100
        curr_iter = 0
        max_comp = 30
        curr_comp = 0
        for i in range(max_iter):
            self.upres()
            iter_update_A(self.size, self.ma_res, self.ma_ava)
            for k in range(self.size):
                if self.ma_res[k][k] + self.ma_ava[k][k] > 0:
                    if k not in self.centers:
                        self.centers.append(k)
                    else:
                        curr_comp += 1
            if curr_comp > max_comp:
                break
            curr_iter += 1

    def upres(self):
        for i in range(self.size):
            kSum = [s + a for s, a in zip(self.ma_sim[i], self.ma_ava[i])]
            for j in range(self.size):
                if i != j:
                    nRes = self.ma_sim[i][j] - max(remove(kSum, j))
                else:
                    nRes = self.ma_sim[i][j] - max(remove(self.ma_sim[i], j))
                self.ma_res[i][j] = self.lamda * \
                    self.ma_res[i][j] + (1 - self.lamda) * nRes

    def reset(self):

        self.ma_sim.clear()
        self.ma_res = []
        self.ma_ava = []
        self.size = 0
        self.centers.clear()


def remove(data, index):
    return data[:index] + data[index + 1:]


def iter_update_A(dataLen, R, A):
    old_a = 0  # 更新前的某个a值
    lam = 0.5  # 阻尼系数,用于算法收敛
    # 此循环更新A矩阵
    for i in range(dataLen):
        for k in range(dataLen):
            old_a = A[i][k]
            if i == k:
                max3 = R[0][k]  # 注意初始值的设置
                for j in range(dataLen):
                    if j != k:
                        if R[j][k] > 0:
                            max3 += R[j][k]
                        else:
                            max3 += 0
                A[i][k] = max3
                # 带入阻尼系数更新A值
                A[i][k] = (1-lam)*A[i][k] + lam*old_a
            else:
                max4 = R[0][k]  # 注意初始值的设置
                for j in range(dataLen):
                    # 上图公式中的i!=k 的求和部分
                    if j != k and j != i:
                        if R[j][k] > 0:
                            max4 += R[j][k]
                        else:
                            max4 += 0

                # 上图公式中的min部分
                if R[k][k] + max4 > 0:
                    A[i][k] = 0
                else:
                    A[i][k] = R[k][k] + max4

                # 带入阻尼系数更新A值
                A[i][k] = (1-lam)*A[i][k] + lam*old_a
    # print("max_a:"+str(numpy.max(A)))
    # print(np.min(A))
    return A

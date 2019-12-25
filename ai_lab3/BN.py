from cpt import cpt

class BN:
    def __init__(self, nums, variables, graph, cpts):
        self.nums = nums
        self.variables = variables
        self.graph = graph
        self.cpts = cpts
        # 创建一个名字与编号的字典，便于查找
        index_list = [i for i in range(self.nums)]
        self.variables_dict = dict(zip(self.variables, index_list))
        # 计算全概率矩阵
        self.TotalProbability = self.calculateTotalProbability()

    def calculateProbability(self, event):
        # 分别计算待求变量个数k1和待消除变量个数k2，剩余的为条件变量个数
        k1 = self.count(event, 2)
        k2 = self.count(event, 3)

        probability = []
        for i in range(2**k1):
            p = 0
            for j in range(2**k2):
                index = self.calculateIndex(self.int2bin_list(i, k1), self.int2bin_list(j, k2), event)
                p = p + self.TotalProbability[index]
            probability.append(p)
        # 最后输出的概率矩阵的格式：先输出true，再输出false
        return list(reversed([x/sum(probability) for x in probability]))

    def calculateTotalProbability(self):
        # 全概率矩阵为一个1 * 2^n大小的矩阵，将列号转化为2进制，可表示事件的发生情况
        # 例如共有5个变量，则第7列的概率为p，表示事件00111（12不发生，345发生）发生的概率为p
        TotalProbability = [0 for i in range(2 ** self.nums)]
        for i in range(2 ** self.nums):
            p = 1
            binary_list = self.int2bin_list(i,self.nums)
            for j in range(self.nums):
                # 分没有父节点和有父节点的情况
                # 注意python float在相乘时会产生不精确的问题，因此每次相乘前先乘1000将其转化成整数相乘，最后再除回来
                if self.cpts[j].parents == []:
                    p = p * (self.cpts[j].probabilities[0][1-binary_list[j]] * 1000)
                else:
                    parents_list = self.cpts[j].parents
                    parents_index_list = [self.variables_dict[k] for k in parents_list]
                    index = self.bin_list2int([binary_list[k] for k in parents_index_list])
                    p = p * (self.cpts[j].probabilities[index][1 - binary_list[j]] * 1000)
            TotalProbability[i] = p / 10 ** (self.nums * 3)
        return TotalProbability

    def int2bin_list(self, a, b):
        # 将列号转化成指定长度的二进制数组
        # 下面两句话的含义：将a转化成二进制字符串，然后分割成字符串数组，再将字符串数组转化成整形数组
        # 若得到的整型数组长度不满足self.nums，则在前面补上相应的零
        binary_list = list(map(int, list(bin(a).replace("0b", ''))))
        binary_list = (b - len(binary_list)) * [0] + binary_list
        return binary_list

    def bin_list2int(self, b):
        # 将二进制的数组转化成整数
        result = 0
        for i in range(len(b)):
            result = result + b[len(b)-1-i] * (2 ** i)
        return result

    def calculateIndex(self, i, j, event):
        # 用于生成下标
        # 原理暂略
        index_list = []
        for k in range(len(event)):
            if event[k] == 2:
                index_list.append(i[0])
                del(i[0])
            elif event[k] == 3:
                index_list.append(j[0])
                del(j[0])
            else:
                index_list.append(event[k])

        return self.bin_list2int(index_list)

    def count(self, list, a):
        # 用于统计一个list中含有多少个指定的数字
        c = 0
        for i in list:
            if i == a:
                c = c + 1
        return c
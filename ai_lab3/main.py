import sys

from BN import BN
from cpt import cpt

# 读取文件并生成一个贝叶斯网络
def readBN(filename):
    f = open(filename, 'r')
    # 读取变量数
    nums = int(f.readline())
    f.readline()
    # 读取变量名称
    variables = f.readline()[:-1].split(' ')
    f.readline()
    # 读取有向图邻接表
    graph = []
    for i in range(nums):
        line = f.readline()[:-1].split(' ')
        graph.append(list(map(int, line)))
    f.readline()
    # 读取cpt表
    # 注意，文件中数据格式必须完全按照指定要求，不可有多余的空行或空格
    cpts = []
    for i in range(nums):
        probabilities = []
        while True:
            line = f.readline()[:-1].split(' ')
            if line != ['']:
                probabilities.append(list(map(float, line)))
            else:
                break
        CPT = cpt(variables[i], [], probabilities)
        cpts.append(CPT)
    f.close()
    # 根据邻接表为每个节点生成其父亲节点
    # 注意，这里父亲节点的顺序是按照输入的variables的顺序排列的，不保证更换测试文件时的正确性
    for i in range(nums):
        for j in range(nums):
            if graph[i][j] == 1:
                cpts[j].parents.append(variables[i])

    # 测试父节点生成情况
    # for i in range(nums):
    #     print(cpts[i].parents)
    bayesnet = BN(nums, variables, graph, cpts)
    return bayesnet

# 读取需要求取概率的命令
def readEvents(filename, variables):
    # 条件概率在本程序中的表示：
    # 对变量分类，2表示待求的变量，3表示隐含的需要被消去的变量，0和1表示条件变量的false和true
    # 例如变量为[Burglar, Earthquake, Alarm, John, Mary]
    # 待求的条件概率为P(Burglar | John=true, Mary=false)，则event为[2, 3, 3, 1, 0]
    f = open(filename, 'r')
    events = []
    while True:
        line = f.readline()
        event = []
        if line == "\n":
            continue
        elif not line:
            break
        else:
            for v in variables:
                index = line.find(v)
                if index != -1:
                    if line[index+len(v)] == ' ' or line[index+len(v)] == ',':
                        event.append(2)
                    elif line[index+len(v)] == '=':
                        if line[index+len(v)+1] == 't':
                            event.append(1)
                        else:
                            event.append(0)
                else:
                    event.append(3)
            # 检查文本错误
            if len(event) != len(variables):
                sys.exit()
            events.append(event)
    return events

# 主程序
filename1 = "burglarnetwork.txt"
bayesnet = readBN(filename1)
filename2 = "burglarqueries.txt"
events = readEvents(filename2, bayesnet.variables)
for event in events:
    print(bayesnet.calculateProbability(event))
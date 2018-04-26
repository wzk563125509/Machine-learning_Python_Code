#Logistic 回归梯度上升优化算法

#便利函数, 打开文本文档并逐行读取
def loadDataSet():
    #数据文件格式 X1 X2 Y
    datMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        #为了方便计算 X0 = 1.0
        dataMat.append([1.0, float(lineArr[0], float(lineArr[1]))])
        #标签
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

# sigmoid 函数(阶跃函数) sigmoig(0) = 0.5
def sigmoid(inX):
    return 1.0 / (1 + exp(-inX))


#画出数据集和Logistic回归最佳拟合直线函数
def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]

    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []

    #从数据集中分类出 1.2类点
    for i in range(n):
        if int(labelMat[i] == 1):
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else :
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s = 30, c = 'red', marker = 's')
    ax.scatter(xcord2, ycord2, s = 30, c = 'green')

    x = arange( -3.0, 3.0, 0.1)
    # w0*x0 + w1*x1 + w2*x2 = 0 设置 x0 = 1
    # 分割方程
    y = (-weights[0]-weights[1]*x)/weights[2]

    ax.plot(x,y)
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()


#梯度上升算法
    #计算整个数据记得梯度，来更新回归系数
def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    #矩阵的行数和列数
    m, n =shape(dataMatrix)
    #步长
    alpha = 0.001
    #迭代次数
    maxCycles = 500
    #初始化权重全为0
    weights = ones((n, 1))

    for k in range(maxCycles):
        h = sigmoid(dataMatris * weights)
        error = (labelMat - h)
        #梯度上升， dataMatrix.transpose() * error 为导数
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights

#随机梯度上升 gradAscent的优化
#一次仅用一个人样本点来更新回归系数
def stocGradAscent0(dataMatrix, classLabels):
    #矩阵的行数和列数
    m, n = shape(dataMatrix)
    #步长
    alpha = 0.01
    #初始化权重全为0
    weights = ones(n)

    for k in range(m):
        h = sigmoid(sum(dataMatrix[i]) * weights)
        error = classLabels[i] - h
        #梯度上升， dataMatrix.transpose() * error 为导数
        weights = weights + alpha * error * dataMatrix[i]
    return weights

#改进的随机梯度上升算法
#改进1： alpha在每次迭代过程中会调整，alpha随着迭代次数减小，但不会到0
#改进2： 随机选取样本来更新回归系数 - 减少周期性波动
def stocGradAscent1(dataMatrix, classLabels, numIter = 150):
    m,n = shape(dataMatrix)
    weights = ones(n)
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m);
        alpha = 4/(1.0 + j + i) + 0.01
        randIndex = int(random.uniform(o , len(dataIndex)))
        h = sigmoid(sum(dataMatrix[randIndex] * weights))
        error = classLabels[ranIndex] - h
        weights = weights + alpha * error * dataMatrix[randIndex]
        del(dataIndex[randIndex])
    return weights


#示例从氙气病症预测病马的死亡率 - 利用Logistic

#分类
def classifyVector(inX , weights):
    prob = sigmoid(sum(inX * weights))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0
#数据导入和测试    
def colicTest():
    frTrain = open('horseColicTraining.txt')
    frTest = open('horseColicText.txt')
    trainingSet =[]
    trainingLabels = []
    for line in frTrain.readLines():
        currLine = line.strip().split('\t')
        lineArr = []
        #0--20 一共21个特征
        for i in range(21):
            lineArr.append(float(currLine))

        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))

    trainWeights = stocGrandAscent1(array(trainingSet), trainingLabels, 500)
    errorCount = 0
    numTestVec = 0.0

    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights)) != int(currLine[21]):
            errorCount += 1

    errorRate = (float(errorCount)/numTestVec)
    print("the error rate of this test is : %f" %errorRate)

    return errorRate
#错误率显示
def mulitTest():
    numTest = 10; errorSum = 0.0
    for k in range(numTests):
        errorSum += colicTest()

    print('after %d iterations the average error rate is : %f' %(numTests, errorSum/float(numTests)))

        

from math import log
import operator
import pickle

#计算当前数据集的信息熵（香农熵）
def calcShannonEnt(dataSet):
    #数据集共有多少条记录
    numEntries = len(dataSet)
    labelCounts = {}

    #循环记录,计算总数据集合的信息熵[分类计算各个标签有多少条记录]
    for featVec in dataSet:
        currentLabel = featVec[-1] #数据集中，最后一列存放分类结果/标签
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
        #print('%s %d' %(currentLabel,labelCounts[currentLabel]))

    #计算香农熵
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        #print('键%s : 次数%f : 样本合计%s' %(key,labelCounts[key],numEntries))
        shannonEnt -= prob * log(prob,2)

    #print(shannonEnt)
    #print(' *---* ')
    return shannonEnt


#按照给定特征划分数据集
#参数说明:待划分数据集,划分特征所在列下标,划分特征值
def spiltDataSet(dataSet,axis,value):
    #print('%s' %(axis))
    retDataSet = []
    #找到特征axis = value的数据记录,并将其剔除该特征列后,形成新的数据集-为划分后的数据集
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            #a.extend(b),会将列表b数据拆开,逐个作为列表a的数据项
            reducedFeatVec.extend(featVec[axis+1:])
            #a.append(b),将列表b作为一个整体当成a的数据项
            retDataSet.append(reducedFeatVec)
    return retDataSet


#选择最好的数据集划分方式--选择最优的特征进行划分,比较各个特征划分的信息增益，取最大值
def chooseBestFeatureToSplit(dataSet):
    #计算特征列
    numFeatures = len(dataSet[0])-1
    #计算划分前的信息熵
    baseEntropy = calcShannonEnt(dataSet)

    bestInfoGain = 0.0
    bestFeature = -1

    for i in range(numFeatures):
        #找到该列特征的全部可选值
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)

        newEntropy = 0.0
        for value in uniqueVals:
            #取得划分后的数据集
            subDataSet = spiltDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
            print('%s : %f , %f' %(value,prob,calcShannonEnt(subDataSet)))

        #比较，选择最大的信息增益
        infoGain = baseEntropy - newEntropy
        print('infoGain =  %f , %s' %(infoGain,i))
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i

    print(' ---- ')
    print(' ---- ')
    return bestFeature

#多数表决,选择数量最多的标签最为叶子结点的值
def majorityCnt(classList):
    classCount = {}

    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse = True)
    return sortedClassCount[0][0]


#构建决策树ID3算法
def createTree(dataSet,labels):
    #数据集的标签列表
    classList = [example[-1] for example in dataSet]
    #数据集中，所有的标签都一致，即全部划分为一个类,则停止
    if classList.count(classList[0])== len(dataSet):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)

    #选择最优分类特征
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]

    #以字典变量存储树结构
    myTree  = {bestFeatLabel:{}}
    #删除已选择的特征
    del(labels[bestFeat])

    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)

    #根据选择的特征可选值,分别划分数据集，并构建决策树
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(spiltDataSet(dataSet,bestFeat,value),subLabels)

    return myTree

#使用pickle存储决策树     
def storeTree(inputTree,fileName):
    fw = open(fileName,encoding='utf8')
    pickle.dump(inputTree,fw)
    fw.close()

#使用pickle得到字典类型的决策树
def grabTree(filename):
    fr = open(fileName,encoding='utf8')
    return pickle.load(fr)


#从文本文件中读取数据,第一行为特征名,其余均为记录,同行数据间以'\t'Tab键分割
def createDataSet(fileName):
    fr = open(fileName,encoding='utf-8')
    lines = fr.readlines()

    labels = lines[0][1:].strip().split('\t')
    dataSet = [line.strip().split('\t') for line in lines[1:]]
    
    return dataSet,labels


#使用决策树进行决策
def classify(inputTree,featLabels,testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    classLabel = '未知'
    for key in list(secondDict.keys()):
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else:
                classLabel = secondDict[key]
    return classLabel


#集合测试
def classTest(fileName):
    dataSet,labels = createDataSet(fileName)
    hoRatio = 0.10
    m = len(dataSet)

    numTestVecs = int(m*hoRatio)
    
    errorCount = 0.0
    mLabel = labels[:]
    #tree = createTree(dataSet[:-numTestVecs],mLabel)
    tree = createTree(dataSet[:],mLabel)

    for i in range(numTestVecs):
        classLabel = classify(tree,labels,dataSet[-1-i])
        print("No. %d : The Tree - %s , the real answer - %s " % (int(m-i),classLabel,dataSet[-1-i][-1]))
        if dataSet[-1-i][-1] != classLabel:
            errorCount += 1.0

    print('')
    print('the total error rate is : %f' %(errorCount/float(numTestVecs)))
    return tree        
        
    











    

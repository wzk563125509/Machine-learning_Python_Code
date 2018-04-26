#KNN K-近邻算法 
#需要安装Numpy包
from numpy import *
import operator

#K-近邻算法 （判定向量,训练数据集,训练数据集标签,参数K）
def classify0(inX,dataSet,lables,k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    #欧式距离 - 求判定向量与训练数据集间的距离
    distances = ((diffMat ** 2).sum( axis = 1 )) ** 0.5 
    sortedDisIndicies = distances.argsort()
    classCount = {} #标签数组，记录在距离最近的K条记录中标签出现次数

    for i in range(k):
        voteIlable = lables[sortedDisIndicies[i]]
        classCount[voteIlable] = classCount.get(voteIlable,0) + 1
    sortedclassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedclassCount[0][0] #返回出现次数最多的标签。

#文本记录转换为NumPy的解析程序
def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOLines = len(arrayOLines)

    #数据文本中,特征值有3个
    #记录数据集
    returnMat = zeros((numberOLines,3))
    classLabelVector = []
    index = 0

    for line in arrayOLines:
        line = line.strip()
        #数据文件格式  XX YY ZZ 1 每行内由TAB分隔,最后一列为标签
        listFormLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        #标签输入时,手动转化为int,不然会默认为字符串格式
        classLabelVector.append(int(listFromLine[-1]))
        index += 1

    return returnMat,classLabelVector


#归一化特征值 newValue = ( oldValue - min ) / ( max - min )
def autoNorm(dataSet):
    #得到每列的最大最小值
    minValues = dataSet.min(0)
    maxValues = dataSet.max(0)
    ranges = maxValues - minValues
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minValues,(m,1))
    normDataSet = normDataSet / tile(ranges,(m,1))
    return normDataSet , ranges , minValues


#分类器的测试代码
def classTest():
    hoRatio = 0.10 #数据集中,多少数据作为测试集
    dataMat , labels = file2matrix('TestSet.txt') #文件名
    normMat , ranges , minValues = autoNorm(dataMat)
    m = normMat.shape(0)
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],labels[numTestVecs:m],3)
        print("The classifier came back with: %d, the real answer is: %d" %(classifierResult,labels[i]))
        if classifierResult != labels[i] :
            errorCount += 1.0

        print("The total error rate is : %f" %(errorCount / float(numTestVecs)))

#汇总,构建完整预测函数
def classifyPerson():
    resultList = ['Not at all','In small doses','In large doses']
    percentTats = float(input("Percentage of time spent playing video games? "))
    ffMiles = float(input("Frequent flier miles earned per year? "))
    iceCream = float(input("Liters of ice cream consumed per year? "))

    dataMat,lables = file2matrix('TestSet2.txt')
    normMat , ranges , minValues = autoNorm(dataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr,-minValues)/ranges,normMat,lables,3)

    print("You will probably like this person: ",resultList[classifierResult-1])
    

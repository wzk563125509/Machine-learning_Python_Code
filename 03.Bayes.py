#朴素贝叶斯分类器的应用
from numpy import *
import operator

#创建词汇表，文档中出现的不重复的词列表
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vacabSet = vocabSet | set(document)
    return list(vocabSet)


#构建文档向量,参数：词汇表，文档。
def setOfWords2Vec(vocabSet,inputSet):
    returnVec = [0] * len(vocabSet)
    for word in inputSet:
        # 词袋模型 - 统计该词在文档中出现的次数
        if word in vocabSet:
            returnVec[vocabSet.index(word)] += 1
        else:
            print("the word: %s is not in my Vocabulary!" %word)
    return returnVec


#朴素贝叶斯分类器训练函数,参数:文档向量矩阵,文档类别向量(只有两类 0 and 1)
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)

    #初值设成1与2，防止由于某个词没出现，导致最后整个概率乘积为0
    p0Num = ones(numWords); p1Num = ones(numWords)
    p0Denom = 2.0; p1Denom = 2.0

    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i] #向量相加
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i] #向量相加
            p0Denom += sum(trainMatrix[i])

    #概率取自然对数,解决下溢出问题.
    p1Vect = log(p1Num/p1Denom)
    p0Vect = log(p0Num/p0Denom)

    return p0Vect,p1Vect,pAbusive


#朴素贝叶斯分类函数 参数:欲分类的文档向量,p0Vect,p1Vect,pAbusive(训练函数的三个返回值)
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1 - pClass1)

    if p1 > p0 :
        return 1
    else :
        return 0

# 使用朴素贝叶斯分类器 进行垃圾邮件测试
# 1-1
def textParse(bigString):
    import re
    listOfTokens = re.split(r'\w',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok)>2]
#1-2
def spamTest():
    docList = []; classList = []; fullText = []

    #一共50封邮件，垃圾|非垃圾各25
    for i in range(1,26):
        #文件夹读取文件,一个txt文档一封邮件
        wordList = textParse(open('email/spam/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)#1--垃圾邮件

        wordList = textParse(open('email/ham/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)#0--非垃圾邮件

    vocabList = createVocabList(docList)
    trainingSet = range(50); testSet = []

    #随机取10封邮件作为测试集,并从训练集中剔除
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat = []; trainClasses = []

    #构建训练集的向量矩阵
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])

    #调用函数计算
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))

    errorCount = 0

    #测试集
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1

    #错误率,可以多次迭代计算平均错误率,才比较好
    print("the error rate is : ", float(errorCount)/len(testSet))


#使用朴素贝叶斯分类器从个人广告中获取区域倾向
#2-1 高频词去除函数
def calcMostFreq(vocabList,fullText):
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(),key = operator.itemgetter(1),reverse = True)
    return sortedFreq[:30]

#2-2 RSS源分类器 参数:两个RSS源作为参数
def localWords(feed1,feed0):
    docList = []; classList = []; fullText = []
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.entend(wordList)
        classList.append(1)

        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.entend(wordList)
        classList.append(0)

    vocabList = createVocabList(docList)
    top30Words = calcMostFreq(vocabList, fullText)

    #最靠前的一些词频是常用词，没太多研究意义，可以提升最后效果.去除个数可以尝试一下找最优。
    #也可以找网上的一些 '通用词表'--一些助动词,辅助词等
    for pairW in top30Words:
        if pairW[0] in vocabList:
            vocabList.remove(pairW[0])
    trainingSet = range(2*minLen); testSet = []

    #随机取20条作为测试集
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat = []; trainClasses = []

    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])

    #调用函数计算
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))

    errorCount = 0

    #测试集
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1

    #错误率,可以多次迭代计算平均错误率,才比较好
    print("the error rate is : ", float(errorCount)/len(testSet))

    return vocabList,p0V,p1V

#2-3 分析数据-显示地域相关用词。
def getTopWords(ny,sf):
    vocabList,p0V,p1V = localWords(ny,sf)
    topNY = []; topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i]))

    sortedSF = sorted(topSF, key = lambda pair:pair[1], reverse = True)
    print("SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF")
    for item in sortedSF:
        print(item[0])
        
    sortedNY = sorted(topNY, key = lambda pair:pair[1], reverse = True)
    print("NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY")
    for item in sortedNY:
        print(item[0])

#SVM
from numpy import *
#Part 1 - 简化版的SMO高效算法处理小效果数据集合
#Part 2 - 完整版Platt SMO算法
#Part 3 - 计算超平面的线性方程系数

#SMO算法辅助函数
def load DataSet (fileName):
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        #数据集中， X1 X2 Y[标签类采用 1 / -1]
        dataMat.append([float(lineArr[0]), float(lineArr(1))])
        labelMat.append(float(lineArr[2]))

    return dataMat, labelMat


#Part 1 --- 简化版的SMO算法(数据集, 标签类别, 常数C, 容错率, 最大循环次数)
def amoSimple(dataMatIn, classLabels, C, toler, maxIter):
    detaMatrix = mat(dataMatIn); labelMat = mat(classLabels).transpose() #转置
    b = 0; m, n = shape(dataMatrix) #数据标签的行列
    alphas = mat(zeros(m,1)) #初始化全0的 Alpha 列向量
    ite = 0 #记录当前循环次数

    while(ite < maxIter):
        alphaPairsChanged = 0 #用于记录Alpha是否进行优化
        for i in range(m):
            # multiply 点乘 , 这是求解后模型的计算公式 - 预测出类别
            fXi = float(multiply(alphas,labelMat)).T * (dataMatrix * dataMatrix[i,:].T) + b
            Ei = fXi - float(labelMat[i]) # 预测是实际值的误差

            if((labelMat[i]*Ei < -toler) and (alphas[i] < c)) or ((labelMat[i]*Ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i,m) # 随机选取第二个 阿尔法
                fXj = float(multiply(alphas,labelMat)).T * (dataMatrix * dataMatrix[j,:].T) + b
                Ej = fXi - float(labelMat[j])
                
                alphaIold = alphas[i].copy();
                alphaJold = alphas[j].copy();

                if(labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C ,C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C ,alphas[j] + alphas[i])

                if L == H :
                    print("L == H")
                    continue

                eta = 2.0 * dataMatrix[i,:] * dataMatrix[j,:].T - dataMatrix[i,:] * dataMatrix[i,:].T - dataMatrix[j,:] * dataMatrix[j,:].T
                if eta >= 0:
                    print("eta >=0")
                    continue

                alphas[j] -= labelMat[j] * (Ei - Ej) / eta
                alphas[i] = clipAlpha(alphas[j],H,L)

                if (abs(alphas[j] - alphas[i]) < 0.00001):
                    print("j not moving enough")
                    continue
                alphas[i] += labelMat[j] * labelMat[i] * (alphaJold - alphas[j])
                b1 = b - Ei - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i,:] * dataMatrix[i,:].T - labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[i,:] * dataMatrix[j,:].T
                b2 = b - Ej - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i,:] * dataMatrix[j,:].T - labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[j,:] * dataMatrix[j,:].T

                if (0 < alphas[i]) and (C > alphas[i]) :
                    b = b1
                elif (0 < alphas[j]) and (C > alphas[j]):
                    b = b2
                else:
                    b = (b1 + b2)/2.0

                alphaPairsChanged += 1
                print("iter : %d  i : %d, pairs changed %d" %(ite,i,alphaPairsChanged))

        #只有在全部数据集上遍历 maxIter 次, 且不发生任何Alpha修改，才会退出While循环
        if(alphaPairsChanged == 0):
            ite += 1
        else :
            ite = 0
        print("iteration number: %d" %ite)
        
    return b,alphas
                    

#Part 2 --  完整版Platt SMO
#2.1 完整版 Platt SMO 的支持函数
class optStruct:
    def __init__(self, dataMatIn, classLabels, C, toler):
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = shape(dataMatIn)[0]
        self.alphas = mat(zeros((self.m,1)))
        self.b = 0
        self.eCache = mat(zeros((self.m,2))) #误差缓存

#用于计算误差
def calcEK(oS, k):
    fXk = float(nultiply(oS.alphas, oS.labelMat).T * (oS.X * oS.X[k,:].T)) + oS.b #预测值
    Ek = fXk - float(oS.labelMat[k])
    return Ek

#选择第二个alpha值。简化版中是随机抽取
def selectJ(i, oS, Ei):
    maxK = -1; maxDeltaE = 0; Ej = 0
    oS.eCache[i] = [1, Ei]
    validEcacheList = nonzero(oS.eCache[:,0].A)[0]
    if(len(validEcacheList)) > 1:
        for k in validEcacheList: #选择步长最大的J
            if k == i:
                continue
            Ek = calcEk(oS, k)
            deltaE = abs(Ei - Ek)
            if (deltaE > maxDeltaE):
                maxK = k
                maxDeltaE = deltaE
                Ej = Ek
            else:
                j = selectJrand(i, oS.m) #第一次循环的话，随即挑选
                Ej = calcEk(oS, j)
                            
            return j, Ej

#计算误差并存入缓存
def updateEk(oS, k):
    Ek = calcEk(oS ,k)
    oS.eCache[k] = [1, Ek]

#2.2 完整版 Platt SMO 算法中的优化例程
# 内循环代码
def innerL(i, oS):
    Ei = calcEk(oS, i)
    if ((oS.labelMat[i] * Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i] * Ei > oS.tol ) and (oS.alphas[i] > 0)):
        j, Ej = selectJ(i, oS, Ei) #选择第二个alpha的启发式方法
        alphaIold = oS.alphas[i].copy()
        alphaJold = oS.alphas[j].copy()

        if(oS.labelMat[i] != oS.labelMat[j]):
            L = max(0, oS.alphas[j] - oS.alphas[i])
            H = max(oS.C, oS.C + oS.alphas[j] -oS.alphas[i])
        else:
            L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
            H = max(oS.C, oS.alphas[j] + oS.alphas[i])
        if L == H:
            print("L == H")
            return 0

        eta = 2.0 * oS.X[i,:] * oS.X[j,:].T - oS.X[i,:] * oS.X[i,:].T - oS.X[j,:] * oS.X[j,:].T
        if eta >= 0:
            print("eta >= 0")
            return 0

        oS.alphas[j] -= oS.labelMat[j] * (Ei - Ej) / eta
        oS.alphas[j] = clipAlpha(oS.alphas[j], H, L)
        updateEk(oS, j) #更新误差

        if(abs(oS.alphas[j] - alphaJold) < 0.00001):
            print("j not moving enough")
            return 0
        oS.alphas[i] += oS.labelMat[i] * oS.labelMat[i] * (alphaJold - oS.alphas[j])
        updateEk(oS, i) #更新误差

        b1 = oS.b - Ei - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.X[i,:] * oS.X[i,:].T - oS.labelMat[j] * (oS.alphas[j] - alphaJold) * oS.X[i,:] * oS.X[j,:].T
        b2 = oS.b - Ej - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.X[i,:] * oS.X[j,:].T - oS.labelMat[j] * (oS.alphas[j] - alphaJold) * oS.X[j,:] * oS.X[j,:].T

        if(0 < oS.alphas[i]) and (oS.C > oS.alphas[i]):
            oS.b = b1
        elif (0 < oS,alphas[j]) and (oS.C > oS.alphas[j]):
            oS.b = b2
        else:
            oS.b = (b1 + b2) / 2.0
        return 1
        
    else:
        return 0

# 外循环代码
def smoP(dataMatIn, classLabels, C, toler, maxIter, kTup = ('lin', 0)):
    oS = optStruct(mat(dataMatIn), mat(classLabels).transpose(), C, toler)
    ite = 0
    entireSet = True
    alphaPairsChanged = 0

    #迭代次数超过最大值 或者 整个遍历都未修改任意alpha 
    while(ite < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
        alphaPairsChanged = 0
        if entireSet : #遍历所有值
            for i in range(oS.m):
                alphaPairsChanged += innerL(i, oS)
                print("fullSet, iter:%d  i:%d,  pairs changed %d" %(ite, i, alphaPairsChanged))
            ite += 1
        else: #遍历非边界值
            nonBoundIs = nonzero((oS.alphas.A > 0) * (oS.alphas.A < C))[0]
            for i in nonBoundIs:
                alphaPairsChanged += innerL(i, oS)
                print("non-bound, iter:%d  i:%d, pairs changed %d " %(ite, i, alphaPairsChanged))
            ite +=1

        if entireSet:
            entireSet = False
        elif (alphaPairsChanged == 0):
            entireSet = True

        print("iteration number: %d" %ite)

    return oS.b, oS.alphas


#Part 3  计算 W(转置)--超平面的系数 。 W(转置)*X + b > 0 --> 1类 ， W(转置)*X + b <= 0 --> -1类
def calcWs(alphas, dataArr, classLabels):
    X = mat(dataArr)
    labelMat = mat(classLabels).transpose()
    m,n = shape(X)
    w = zeros((n,1))
    for i in range(m):
        w += multiply(alphas, dataArr, labelArr)
    return w

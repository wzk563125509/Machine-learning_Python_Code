#八皇后问题
import math
import random
def conflict(state,nextX):
    '''
    新放入的皇后(len(state),nextX)位置坐标点
    已经放好的皇后位置(i,state[i]),元组的下标作为行，值作为列。
    比较新旧皇后是否有同行同列/对角关系
    '''
    nextY = len(state)
    for i in range(nextY):
        # 0 -- 同列关系，nextY-i -- 对角关系，行不会重复，从第一行开始排列下来的
        if abs(state[i]-nextX) in (0,nextY-i):
            return True
    return False

def queens(num=8,state=()):
    #从第一行开始逐行确定Queen位置
    for pos in range(num):
        #检测冲突
        if not conflict(state,pos):
            #每行都排满。
            if len(state) == num-1:
                yield (pos,)
            else:
                for result in queens(num,state+(pos,)):
                    yield (pos,)+result


def prettyprint(soultion):
    #在函数内又定义了一个函数，因为其他函数不会用到
    def line(pos,length=len(soultion)):
        return '. ' * (pos) + 'X ' + '. ' * (length-pos-1)
    for pos in soultion:
        print(line(pos))
        
#random.choice(),从括号中，随即选择输出        
prettyprint(random.choice(list(queens(4))))

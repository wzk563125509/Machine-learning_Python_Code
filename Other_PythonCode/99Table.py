for i in range(1,10):
    print('')
    for j in range(1,i+1):
        #print("%d*%d=%d " %(i,j,i*j) , end = '')
        a = '{0}*{1}={2}'.format(j,i,i*j)
        print('{0:6} '.format(a),end='',sep='--')
        #print('{0:1}'.format(),sep='',end='\n',filr=sys.stdout,flush=False)

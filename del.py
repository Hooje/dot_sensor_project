import csv
import random
import os 


def del_front(src):
    for i in range(1,6):
        cmd="sed -i '1,11d' "+src+"/"+str(i)+".csv"
        #cmd="sed -i '1,11d' "+src+".csv"
        os.system(cmd)

if __name__ == '__main__':

    way=["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36"]
    #way = ["zero","sit","lie","curve","tilt","stand1","stand2","stand3","stand4","stand5"]

    path = "../1008/test_set/"
    input(f'are you sure to delete {path}')
    for i in range(len(way)):
        source=way[i]
        src1= path +source

        del_front(src1)        


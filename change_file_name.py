import os

iszero=0 # if is zero, set 1

def rename_func(src):
    src1=src+"/good"
    if iszero ==1:
        src1=src
    dirs=os.listdir(src1)
    print(dirs)
    #print(dirs[0][10:12])
    for i in range(len(dirs)):
        if dirs[i][10:12]=="29":
            os.rename(src1+"/"+dirs[i], src1+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="C6":
            os.rename(src1+"/"+dirs[i],src1+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="D0":
            os.rename(src1+"/"+dirs[i],src1+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="CF":
            os.rename(src1+"/"+dirs[i],src1+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="C0":
            os.rename(src1+"/"+dirs[i],src1+"/"+str(i+1)+".csv")
    if iszero == 1:
        input("you can stop")
    src2=src+"/bad"
    dirs=os.listdir(src2)
    #print(dirs)
    #print(dirs[0][10:12])
    for i in range(len(dirs)):
        if dirs[i][10:12]=="29":
            os.rename(src2+"/"+dirs[i],src2+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="C6":
            os.rename(src2+"/"+dirs[i],src2+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="D0":
            os.rename(src2+"/"+dirs[i],src2+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="CF":
            os.rename(src2+"/"+dirs[i],src2+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="C0":
            os.rename(src2+"/"+dirs[i],src2+"/"+str(i+1)+".csv")
def rename_sit_stand(src):
    src1=src
    dirs=os.listdir(src1)
    print(dirs)
    #print(dirs[0][10:12])
    for i in range(len(dirs)):
        if dirs[i][10:12]=="29":
            os.rename(src1+"/"+dirs[i], src1+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="C6":
            os.rename(src1+"/"+dirs[i],src1+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="D0":
            os.rename(src1+"/"+dirs[i],src1+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="CF":
            os.rename(src1+"/"+dirs[i],src1+"/"+str(i+1)+".csv")
        if dirs[i][10:12]=="C0":
            os.rename(src1+"/"+dirs[i],src1+"/"+str(i+1)+".csv")













if __name__ == '__main__':
    
    #with open(lazy_complete_path('xxx'), 'r') as f:
    #way=["vaccume","pick_high","hair","pick"]
    way=["0","1","2","3","4"]#,"5","6"]#,"7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
    #way=["curve","lie","sit","tilt","zero","stand1","stand2","stand3","stand4","stand5"]
    #way=["sit"]
    for i in range(len(way)):
        source=way[i]
        if iszero == 1:
            source="zero"
        src="../stand_train/"+source
        rename_sit_stand(src)
        src="../stand_test/"+source
        rename_sit_stand(src)
        
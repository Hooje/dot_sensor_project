import os
def rename_sensor25(src):
    src1=src
    dirs=os.listdir(src1)
    print(dirs)
    #print(dirs[0][10:12])
    for i in range(len(dirs)):
        if dirs[i] == '2.csv':
            os.rename(src1+"/"+dirs[i], src1+"/"+'next_5'+".csv")
            print('next_5')
        if dirs[i] == '5.csv':
            os.rename(src1+"/"+dirs[i], src1+"/"+'next_2'+".csv")
            print('next_2')
    for i in range(len(dirs)):
        if dirs[i] == 'next_5.csv':
            os.rename(src1+"/"+dirs[i], src1+"/"+'5'+".csv")
            print('5')
        if dirs[i] == 'next_2.csv':
            os.rename(src1+"/"+dirs[i], src1+"/"+'2'+".csv")
            print('2')

#way=["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]
way=["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20",
    "21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36"]
src = "../threshold_test/rdoom/"
input(f'change_sensor {src}')
for i in range(len(way)):
    source=way[i]
    src1=src+source
    rename_sensor25(src1)
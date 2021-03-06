import csv
import random
import os 


def another_zero(g,n): #除了g以外的   0=x  1=y  2=z ， n=1表示歸零n個，n=1就 歸零g，也就是讓其它兩個變成0，n=2就歸零g以外的，把g變成0 。  只歸零x 就是 (0, 1)

    for k in range(3):
        for i in range(5):
            for a in range(3):
                if n == 1:
                    if a!= g:
                        zero[k][i][a]=0
                else:
                    if a==g:
                        zero[k][i][a]=0
    print(zero)
def create_csv(dest):
    path = dest
    with open(path,'w') as f:
        csv_write = csv.writer(f)
        #csv_head = ["1_x","1_y","1_z","2_x","2_y","2_z","3_x","3_y","3_z","4_x","4_y","4_z","5_x","5_y","5_z","good_or_bad"]
        csv_head = ["1_x","1_y","2_x","2_y","3_x","3_y","4_x","4_y","5_x","5_y","good_or_bad"]
        csv_write.writerow(csv_head)


def write_csv(dest, src, y): # 不歸零
    global rnds, num
    data_row=[[0]*11 for i in range(num)]
    with open(dest,'a+') as f:
        csv_write = csv.writer(f)

        for i in range(1,6):
            with open(src+"/"+str(i)+".csv",'r') as f1:
                reader = csv.DictReader(f1)
                cnt=0
                for row in reader:
                    if int(row["PacketCounter"]) in rnds:

                        data_row[cnt][10]=y #number
                        #data_row[cnt][3*i-3:3*i]=[float(row["Euler_X"]),float(row["Euler_Y"]),float(row["Euler_Z"])]
                        #data_row[cnt][3*i-3:3*i]=[float(row["Euler_X"]),float(row["Euler_Y"]),float(row["Euler_Z"])]
                        data_row[cnt][2*i-2:2*i]=[float(row["Euler_X"]),float(row["Euler_Y"])]
                        
                        cnt+=1
                #print(cnt)
                f1.close()
        for i in range(num):
            csv_write.writerow(data_row[i]) 

        f.close()
def write_csv_zero(dest, src, y,k):
    global rnds, num
    data_row=[[0]*11 for i in range(num)]
    with open(dest,'a+') as f:
        csv_write = csv.writer(f)

        for i in range(1,6):
            with open(src+"/"+str(i)+".csv",'r') as f1:
                reader = csv.DictReader(f1)
                cnt=0
                for row in reader:
                    if int(row["PacketCounter"]) in rnds:
                        #data_row[cnt][15]= random.sample(range(1, 10), 1)
                        data_row[cnt][15]=y
                        data_row[cnt][3*i-3:3*i]=[float(row["Euler_X"])-zero[k][i-1][0],float(row["Euler_Y"])-zero[k][i-1][1],float(row["Euler_Z"])-zero[k][i-1][2]]
                        cnt+=1
                #print(cnt)
                f1.close()
        for i in range(num):
            csv_write.writerow(data_row[i])
 
        f.close()
 
def del_front(src):
    for i in range(1,6):
        cmd="sed -i '1,11d' "+src+"/"+str(i)+".csv"
        os.system(cmd)

if __name__ == '__main__':
    global rnds, num
    delete = 0  # if first time ，set 1
    case = 0 # 0 mean no zero, 1 mean all zero, 2 mean  others
    #way = ["sit","lie","curve","stand1","stand2","stand3","stand5"]
    #way=["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
    way=["0","1","2","3","4","5","6","7","8","9","10","11"]#,"12","13"]#,"14","15","16","17","18","19","20"]
    #way=["0","1","4","6","7","8"]#,"9","10","11","12","13","14","15","16","17","18","19","20"]
    #way = ["stand1","stand2","stand3","stand4","stand5"]
    num=200

    rnds = random.sample(range(1, 500), num)

    dest1='3D_train.csv'
    dest2='3D_test.csv'
    #dest3='sit_stand3.csv'
    create_csv(dest1)   # first time create
    create_csv(dest2)   # first time create
    #create_csv(dest3)   # first time create

    if case == 2:
        #another_zero(0,1) #只歸零x
        #another_zero(1,1)  #只歸零y
        #another_zero(2,1)  #只歸零z
        #another_zero(0,2)  #不歸零x
        #another_zero(1,2)  #不歸零y
        another_zero(2,2)  #不歸零z
    for i in range(len(way)):
        source=way[i]

        src1="../0728train/"+source
        src2="../0728test/"+source
        #src3="../new_data3/"+source #roommate

        if delete == 1 :
            print(f'delete = {delete}')
            del_front(src1)
            del_front(src2)
        if case == 0 :

            write_csv(dest1,src1,i) # y is number 0~20
            write_csv(dest2,src2,i)
            #write_csv(dest3,src3,i)
        if (case == 1 or case == 2):
            print(f'case = {case}')
            write_csv_zero(dest1,src1,i+1, 1)#zero1
            write_csv_zero(dest2,src2,i+1, 2)#zero2
            write_csv_zero(dest3,src3,i+1, 3)#zero3
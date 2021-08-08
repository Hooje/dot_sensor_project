import csv
import random
import os 

zero3=[[-89.70264435,-29.57380104,32.33538437],[-137.8149109, -71.28622437,156.2680664],[-145.7379913,-66.16531372, 4.056286335],[-172.1838684,-73.96080017,30.83816528],[5.57302475,-65.58351898,-140.3482056]]

zero4=[[157.9455414,-21.22393036,18.02519608],[-124.3089142,-60.69921494,18.09119415],[-126.3473816,-85.89363098,-138.1930237],[-129.2294769,-56.93817902,-109.0836258],[24.52201271,-66.82037354,101.7940521]]

zero5=[[161.7288818359375, -85.18094635009766, 22.735139846801758],[-179.31793212890625, -78.49246215820312, 94.67963409423828],[142.3302459716797, -86.31449127197266, 60.94913101196289],[150.5840301513672, -76.37879180908203, -33.412315368652344],[28.124404907226562, -67.50650024414062, 140.1622772216797]]

zero6=[[88.50963592529297, -71.72782135009766, 93.44087982177734],[166.59947204589844, -70.88652801513672, 129.08375549316406],[78.28057861328125, -80.71185302734375, 148.40455627441406],[-171.1695098876953, -77.40680694580078, -66.67517852783203],[54.201202392578125, -80.95574188232422, 168.8130340576172]]

zero7=[[-178.3684844970703, -79.56807708740234, 8.261969566345215],[162.77963256835938, -70.38104248046875, 119.37997436523438],[-166.4423370361328, -68.93321990966797, 111.91091918945312],[129.14527893066406, -71.6200942993164, 4.821927547454834],[-3.2002954483032227, -74.98442840576172, 164.5447235107422]]

zero0 = []
zero1 = []
zero2 = []
#zero=[zero3, zero4, zero5]

#zero=[zero6, zero7]

zero = [zero0, zero1, zero2]

def another_zero(dataset):
    if dataset == 345:
        for k in range(3):
            for i in range(5):
                zero[k][i][1]=0
                zero[k][i][2]=0
    else: #dataset=67
        for k in range(2):
            for i in range(5):
                zero[k][i][1]=0
                zero[k][i][2]=0
        print(zero)
def create_csv(dest):
    path = dest
    with open(path,'w') as f:
        csv_write = csv.writer(f)
        csv_head = ["1_x","1_y","1_z","2_x","2_y","2_z","3_x","3_y","3_z","4_x","4_y","4_z","5_x","5_y","5_z","good_or_bad"]
        csv_write.writerow(csv_head)


def write_csv(dest, src, y):
    global rnds, num
    data_row=[[0]*16 for i in range(num)]
    with open(dest,'a+') as f:
        csv_write = csv.writer(f)
        #good first  1, 3, 5   (hair pick vaccume)
        for i in range(1,6):
            with open(src+"/good/"+str(i)+".csv",'r') as f1:
                reader = csv.DictReader(f1)
                cnt=0
                for row in reader:
                    if int(row["PacketCounter"]) in rnds:
                        #data_row[cnt][15]= random.sample(range(1, 10), 1)
                        data_row[cnt][15]=y
                        data_row[cnt][3*i-3:3*i]=[float(row["Euler_X"]),float(row["Euler_Y"]),float(row["Euler_Z"])]
                        cnt+=1
                #print(cnt)
                f1.close()
        for i in range(num):
            csv_write.writerow(data_row[i])
        #bad after 0, 2, 4  (hair pick vaccume)
        for i in range(1,6):
            with open(src+"/bad/"+str(i)+".csv",'r') as f1:
                reader = csv.DictReader(f1)
                cnt=0
                for row in reader:
                    if int(row["PacketCounter"]) in rnds:
                        #data_row[cnt][15]= random.sample(range(1, 10), 1)
                        data_row[cnt][15]=y-1
                        data_row[cnt][3*i-3:3*i]=[float(row["Euler_X"]),float(row["Euler_Y"]),float(row["Euler_Z"])]
                        cnt+=1
                #print(cnt)
                f1.close()

        for i in range(num):
            csv_write.writerow(data_row[i])
 

        f.close()
def write_csv_zero(dest, src, y,k):
    global rnds, num
    data_row=[[0]*16 for i in range(num)]
    with open(dest,'a+') as f:
        csv_write = csv.writer(f)
        #good first  1, 3, 5   (hair pick vaccume)
        for i in range(1,6):
            with open(src+"/good/"+str(i)+".csv",'r') as f1:
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
        #bad after 0, 2, 4  (hair pick vaccume)
        for i in range(1,6):
            with open(src+"/bad/"+str(i)+".csv",'r') as f1:
                reader = csv.DictReader(f1)
                cnt=0
                for row in reader:
                    if int(row["PacketCounter"]) in rnds:
                        #data_row[cnt][15]= random.sample(range(1, 10), 1)
                        data_row[cnt][15]=y-1
                        data_row[cnt][3*i-3:3*i]=[float(row["Euler_X"])-zero[k][i-1][0],float(row["Euler_Y"])-zero[k][i-1][1],float(row["Euler_Z"])-zero[k][i-1][2]]
                        cnt+=1
                #print(cnt)
                f1.close()

        for i in range(num):
            csv_write.writerow(data_row[i])
 

        f.close()
        '''
def write_csv_zero4(dest, src, y):
    global rnds, num
    data_row=[[0]*16 for i in range(num)]
    with open(dest,'a+') as f:
        csv_write = csv.writer(f)
        #good first  1, 3, 5   (hair pick vaccume)
        for i in range(1,6):
            with open(src+"/good/"+str(i)+".csv",'r') as f1:
                reader = csv.DictReader(f1)
                cnt=0
                for row in reader:
                    if int(row["PacketCounter"]) in rnds:
                        #data_row[cnt][15]= random.sample(range(1, 10), 1)
                        data_row[cnt][15]=y
                        data_row[cnt][3*i-3:3*i]=[float(row["Euler_X"])-zero4[i-1][0],float(row["Euler_Y"])-zero4[i-1][1],float(row["Euler_Z"])-zero4[i-1][2]]
                        cnt+=1
                #print(cnt)
                f1.close()
        for i in range(num):
            csv_write.writerow(data_row[i])
        #bad after 0, 2, 4  (hair pick vaccume)
        for i in range(1,6):
            with open(src+"/bad/"+str(i)+".csv",'r') as f1:
                reader = csv.DictReader(f1)
                cnt=0
                for row in reader:
                    if int(row["PacketCounter"]) in rnds:
                        #data_row[cnt][15]= random.sample(range(1, 10), 1)
                        data_row[cnt][15]=y-1
                        data_row[cnt][3*i-3:3*i]=[float(row["Euler_X"])-zero4[i-1][0],float(row["Euler_Y"])-zero4[i-1][1],float(row["Euler_Z"])-zero4[i-1][2]]
                        cnt+=1
                #print(cnt)
                f1.close()

        for i in range(num):
            csv_write.writerow(data_row[i])
 

        f.close()
        '''
def del_front(src):
    for i in range(1,6):
        cmd="sed -i '1,11d' "+src+"/"+str(i)+".csv"
        os.system(cmd)

if __name__ == '__main__':
    global rnds, num
    dataset = 67 # data 345 or data 67 
    delete = 0  # if first time ，set 1
    case = 2 # 0 mean no zero, 1 mean all zero, 2 mean  only x zero

    #way=["hair","pick","vaccume","pick_high"]
    way=["hair",  "pick","pick_high"]
    num=200

    rnds = random.sample(range(1, 1500), num)
    #print(rnds)
    if dataset==345:
        dest1='all_data_3.csv'
        dest2='all_data_4.csv'
        dest3='all_data_5.csv'
        dest4='all_data_34.csv'
        create_csv(dest1)   # first time create
        create_csv(dest2)   # first time create
        create_csv(dest3)   # first time create
        create_csv(dest4) 
    else:# dataset = 67
        dest1='all_data_6.csv'
        dest2='all_data_7.csv'
        create_csv(dest1)   # first time create
        create_csv(dest2)   # first time create

    if case == 2:
        another_zero(dataset)
    for i in range(len(way)):
        source=way[i]
        if dataset == 345:
            src1="../data3/"+source
            src2="../data4/"+source
            src3="../data5/"+source
        else: # dataset=67
            src1="../data6/"+source
            src2="../data7/"+source

        if delete == 1 :
            print(f'delete = {delete}')
            del_front(src1+"/"+"bad")
            del_front(src1+"/"+"good")
            del_front(src2+"/"+"bad")
            del_front(src2+"/"+"good")
        if case == 0 :
            if dataset==345:
                write_csv(dest1,src1,2*i+1)
                write_csv(dest2,src2,2*i+1)
                write_csv(dest4,src1,2*i+1)
                write_csv(dest4,src2,2*i+1)
                write_csv(dest3,src3,2*i+1)
            else: #datset=67
                write_csv(dest1,src1,2*i+1)
                write_csv(dest2,src2,2*i+1)
        if (case == 1 or case == 2):
            print(f'case = {case}')
            if dataset==345:
                write_csv_zero(dest1,src1,2*i+1, 0)#zero3
                write_csv_zero(dest2,src2,2*i+1, 1)

                write_csv_zero(dest4,src1,2*i+1, 0)#zero3
                write_csv_zero(dest4,src2,2*i+1, 1)

                write_csv_zero(dest3,src3,2*i+1, 2)
            else:# dataset=67
                write_csv_zero(dest1,src1,2*i+1, 0)#zero6
                write_csv_zero(dest2,src2,2*i+1, 1)#zero7
        #
        '''
        #write_csv(dest1,src1,1)
        #write_csv(dest2,src2,1)

        #write_csv(dest,src,1)  #if only 1 and 0
    
    src="../data/vaccume"
    del_front(src+"/"+"bad")
    del_front(src+"/"+"good")
    '''
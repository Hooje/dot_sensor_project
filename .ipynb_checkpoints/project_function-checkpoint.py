from math import cos, sin
import math
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

def quaternion_from_euler(e):
    #Z, Y, X (yaw, pitch, roll),
    roll, pitch, yaw = e[0]*math.pi/180, e[1]*math.pi/180,e[2]*math.pi/180

    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return [qw, qx, qy, qz]

def euler_to_dcm(e1,e2): # w, x , y ,z
    q1=quaternion_from_euler(e1)
    q2=quaternion_from_euler(e2)
    return qua_to_dcm(q1,q2)

def qua_diff(q1,q2):  # mean how to from q1 to q2 --> q1 * z = q2
    n_q1=np.linalg.norm(np.array(q1))
    #print(f'norm = {n_q1}')
    n_q2=np.linalg.norm(np.array(q2))

    q1=[q1[0]/n_q1, q1[1]/n_q1, q1[2]/n_q1, q1[3]/n_q1] #會變成單位四元數  類似單位向量

    q2=[q2[0]/n_q2, q2[1]/n_q2, q2[2]/n_q2, q2[3]/n_q2]

    a=q1[0]; b=-q1[1]; c=-q1[2]; d=-q1[3]
    
    e=q2[0]; f=q2[1]; g=q2[2]; h=q2[3]
    
    z = [(a*e - b*f -c* g- d*h), (b*e + a*f + c*h- d*g) , (a*g - b*h+ c*e + d*f) , (a*h + b*g - c*f + d*e)]
    
    return z

def qua_to_dcm(q1,q2):
    q=qua_diff(q1,q2)
    w,x,y,z=q[0],q[1],q[2],q[3] # in ppt w,x,y,z = q4,q1,q2,q3
    tmp1 = w**2+x**2-y**2-z**2
    tmp2 = w**2-x**2+y**2-z**2
    tmp3 = w**2-x**2-y**2+z**2
    if tmp1 > 1 : 
        tmp1=1
    if tmp1 < -1: 
        tmp1=-1
    if tmp2 > 1 : 
        tmp2=1
    if tmp2 < -1: 
        tmp2=-1
    if tmp3 > 1 : 
        tmp3=1
    if tmp3 < -1: 
        tmp3=-1

    angle1=abs(math.acos(tmp1)*180/math.pi)
    angle2=abs(math.acos(tmp2)*180/math.pi)
    angle3=abs(math.acos(tmp3)*180/math.pi)

    print(angle1, angle2, angle3)

def check_sensor(e, e_b):

    for i in [1]: # 1 or 4 check sensor 2 5
        print(f'sensor {i+1}')
        euler_to_dcm(e[i],e_b[i])

def euler_to_3vector(e):
    #Z, Y, X (yaw, pitch, roll),
    roll, pitch, yaw = e[0]*math.pi/180, e[1]*math.pi/180,e[2]*math.pi/180

    x = cos(pitch)*cos(yaw) + sin(roll)*sin(pitch)*sin(yaw)
    y = cos(roll)*sin(yaw)
    z = -sin(pitch)*cos(yaw) + cos(pitch)*sin(roll)*sin(yaw)


    v1 = np.array([x,y,z])

    x = -cos(pitch)*sin(yaw) + sin(roll)*sin(pitch)*cos(yaw)
    y = cos(roll)*cos(yaw)
    z = sin(pitch)*sin(yaw) + cos(pitch)*sin(roll)*cos(yaw)

    v2 = np.array([x,y,z])

    x = sin(pitch)*cos(roll)
    y = -sin(roll)
    z = cos(pitch)*cos(roll)

    v3 = np.array([x,y,z])

    return [v1,v2,v3]


def project_onto_plane(v, n): # v is your vector, n is Normal

    v2 = np.dot(v,n)/np.dot(n,n) * n # v2 means v to n

    v3 = v - v2 # v3 mean v to plane (normal is n)

    return v3 
def angle_between_vector(v1, v2):
    #print(v1, v2)
    temp = np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    if temp > 1 :
        temp=1
    if temp < -1:
        temp=-1
    return math.acos(temp)*180/math.pi
    #return math.acos(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))*180/math.pi


def angle_of_axis(old_v, old_n, new_v): # 舊的向量， 舊的法向量, 新的向量  
    #print(f'old_v = {old_v}')
    project_new_v = project_onto_plane(new_v, old_n) # 將新向量投影到舊的平面 (以n為法向量
    #print('here ')
    angle = angle_between_vector(old_v, project_new_v) #再計算投影後向量與舊向量的夾角
    #print('there')
    #print(old_v, project_new_v)
    #input(f'angle = {angle}')
    return angle 

def three_angle_of_eulers(e1,e2): # (old, new) 計算兩個尤拉角的前後彎、側彎、旋轉角度
    e1_axis = euler_to_3vector(e1) # e1_axis = [x_axis, y_axis, z_axis] , x_axis = [x, y, z] vector....
    e2_axis = euler_to_3vector(e2)

    angle1 = angle_of_axis(e1_axis[0],e1_axis[1],e2_axis[0])  # 前彎 : 舊x軸和，新x軸投影到以舊y軸為法向量的xz平面 的這個投影向量，的夾角
    angle2 = angle_of_axis(e1_axis[0],e1_axis[2],e2_axis[0])  # 側彎 : 舊x軸和，新x軸投影到以舊z軸為法向量的xy平面 的這個投影向量，的夾角
    angle3 = angle_of_axis(e1_axis[1],e1_axis[0],e2_axis[1])  # 旋轉 : 舊y軸和，新y軸投影到以舊x軸為法向量的yz平面 的這個投影向量，的夾角
    return angle1, angle2, angle3

def threshold_funcion(angle,d_angle, balance_percent):
    #balance_percent = 0.6 
    '''
    balance_1 = 2
    balance_2 = 2
    balance_3 = 2
    '''
    s1 = 1 # 選兩個sensor 來算
    s2 = 2
    # angle[sensor]=[前彎、側彎、旋轉]
    # d_angle[sensor]=[前彎、側彎、旋轉]
    #print(angle[s1][0]-angle[s2][0] , angle[s1][1]-angle[s2][1] , angle[s1][2]-angle[s2][2])
    temp1 = ((angle[s1][0]-angle[s2][0])/(balance_percent *(d_angle[s1][0]-d_angle[s2][0])))**2
    temp2 = ((angle[s1][1]-angle[s2][1])/(balance_percent *(d_angle[s1][1]-d_angle[s2][1])))**2
    temp3 = ((angle[s1][2]-angle[s2][2])/(balance_percent * (d_angle[s1][2]-d_angle[s2][2])))**2
    return temp1 + temp2 + temp3

    #return (temp1)*balance_1+(temp2)*balance_2+(temp3)*balance_3
def func_three_angle(path,dirs,way,path_t,dir_t,way_t, balance_percent):

    d_angle = {} # 前後、側彎、旋轉的最大值

    e_basic = {}

    way_set1 = [1,2,3,4,5] #前彎
    way_set2 = [6,7,8,9,10] #右側
    way_set3 = [11,12,13,14,15] #右旋
    for d in dirs:  # for zero in every people
        d_angle[d] = [[0 for _ in range(3)] for _ in range(5)] # 順便初始化，d_front[mine][sensor]=[angle1, angle2, angle3] 表示某Sensor 的 前、側、旋的夾角

        e_basic[d] = [[],[],[],[],[]]

        for i in range(5):
            with open(f'{path}/{d}/0/{i+1}.csv') as f:
                f.readline() #ignore first line
                temp = f.readline().strip().split(',')
                
                e_basic[d][i]= [float(k) for k in temp[2:]]
        
    for w in way:
        for d in dirs: # for every person 

            s1 = open(f'{path}/{d}/{w}/1.csv','r') #f mean sensor
            s2 = open(f'{path}/{d}/{w}/2.csv','r')
            s3 = open(f'{path}/{d}/{w}/3.csv','r')
            s4 = open(f'{path}/{d}/{w}/4.csv','r')
            s5 = open(f'{path}/{d}/{w}/5.csv','r')
            all_sensor = [s1,s2,s3,s4,s5] 

            e=[[] for _ in range(5)] #for every sensor's euler
            q=[[] for _ in range(5)] #for every sensor's euler to quaternion
            for f in all_sensor: #each sensor
                each_line = f.readline()#first line


            for idx,f in enumerate(all_sensor): #each sensor
                each_line = f.readline()
                each_list = each_line.strip().split(',') # string to list
                e[idx] = [float(k) for k in each_list[2:]] # get sensor

            #input('check max sensor')
            #check_sensor(e,e_basic[d])

            if int(w) in way_set1:
                k = 0
            elif int(w) in way_set2:
                k = 1
            elif int(w) in way_set3:
                k = 2
            else:
                continue
            angles = [[0 for _ in range(3)] for _ in range(5)]
            for i in range(5):
                angles[i] = three_angle_of_eulers(e_basic[d][i],e[i]) #angles[0] = [angle1, angle2, angle3] 表示sensor1變化的三個角度
                #print(d_angle[d][i][k] , angles[k])
                d_angle[d][i][k] += angles[i][k] # 第i個sensor的 前彎、側彎、旋轉  的值增加 

            #print(f'angles = {angles}')




            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()

    #----------------------------------------------------------------- print angle
    print(angles)
    input()

    #----------------------------------------------------------------- for 當下  

    e_basic = {}
    for d in dir_t:  # for zero
        e_basic[d] = [[],[],[],[],[]]
        for sensor_ in range(len(d_angle[d])):

            d_angle[d][sensor_] = [x/5 for x in d_angle[d][sensor_]]  # 前面加五次，把每個都除5  (前彎 側彎 旋轉)
        for i in range(5):
            with open(f'{path_t}/{d}/0/{i+1}.csv') as f:
                f.readline() #ignore first line
                temp = f.readline().strip().split(',')
                e_basic[d][i]= [float(k) for k in temp[2:]]
    
    k_value_set = []

    for w in way_t:
        for d in dir_t: # for every person 

            s1 = open(f'{path2}/{d}/{w}/1.csv','r') #f mean sensor
            s2 = open(f'{path2}/{d}/{w}/2.csv','r')
            s3 = open(f'{path2}/{d}/{w}/3.csv','r')
            s4 = open(f'{path2}/{d}/{w}/4.csv','r')
            s5 = open(f'{path2}/{d}/{w}/5.csv','r')
            all_sensor = [s1,s2,s3,s4,s5] 

            

            e=[[] for _ in range(5)] #for every sensor's euler
            q=[[] for _ in range(5)] #for every sensor's euler to quaternion
            
            for f in all_sensor: #each sensor
                each_line = f.readline()#first line

            for idx,f in enumerate(all_sensor): #each sensor
                each_line = f.readline()
                each_list = each_line.strip().split(',') # string to list
                e[idx] = [float(k) for k in each_list[2:]] # get sensor
            
            #input('check test sensor')
            #check_sensor(e,e_basic[d])
            #input()
            angles = [[] for _ in range(5)]
            for i in range(5):
                angles[i] = three_angle_of_eulers(e_basic[d][i],e[i]) #angles[0] = [angle1, angle2, angle3] 表示sensor1變化的三個角度
            #print(f'angles = {angles}')



            k_value = threshold_funcion(angles,d_angle[d], balance_percent)

            k_value_set.append(k_value > 1) 
            if int(w)%4 == 1 :
                print()
            print(f'k_value = {k_value}')


            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()

    k_value_answer = [0,1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,0,0, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,0,0]

    acc = accuracy_score(k_value_answer,k_value_set)
    matrix = confusion_matrix(k_value_answer,k_value_set)
    print()
    print(acc)
    print(matrix)
if __name__ == '__main__':
    
    path = f'../threshold_max' 
    path2 = f'../threshold_test'
    dirs = ['1202_mine'] 
    dir_t = ['1202_mine']      
    way = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]
    way_t = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36"]
    balance_percent = 0.7
    func_three_angle(path,dirs,way,path2,dir_t,way_t, balance_percent)


'''

euler_to_3vector([0.103113309, -0.506458759 ,   -147.123291])
euler_to_3vector([-0.071697503,    1.085567594, -171.6932068])
euler_to_3vector([-0.651638448,    -0.581820488,    32.06290436])
euler_to_3vector([-0.448454171,    -0.042662635,    -62.60937881])
euler_to_3vector([23.67301178, -29.45196342,    105.3321152])
euler_to_3vector([70,43,43])
euler_to_vector([70,43,43])

0.103113309 -0.506458759    -147.123291
-0.071697503    1.085567594 -171.6932068
-0.651638448    -0.581820488    32.06290436
-0.448454171    -0.042662635    -62.60937881
23.67301178 -29.45196342    105.3321152
'''
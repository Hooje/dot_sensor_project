from math import cos, sin
import math


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


def project_onto_plane(v, n) # v is your vector, n is Normal

    v2 = np.dot(v,n)/np.dot(n,n) * n # v2 means v to n

    v3 = v - v2 # v3 mean v to plane (normal is n)

    return v3 
def angle_between_vector(v1, v2):
    return math.acos(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))*180/math.pi
def angle_of_axis(old_v, old_n, new_v): # 舊的向量， 舊的法向量, 新的向量  
    project_new_v = project_onto_plane(new_v, old_n) # 將新向量投影到舊的平面 (以n為法向量
    angle = angle_between_vector(old_v, project_new_v) #再計算投影後向量與舊向量的夾角
    return angle 

def three_angle_of_eulers(e1,e2) # (old, new) 計算兩個尤拉角的前後彎、側彎、旋轉角度
    e1_axis = euler_to_3vector(e1) # e1_axis = [x_axis, y_axis, z_axis] , x_axis = [x, y, z] vector....
    e2_axis = euler_to_3vector(e2)

    angle1 = angle_of_axis(e1[0],e1[1],e2[0])  # 前彎 : 舊x軸和，新x軸投影到以舊y軸為法向量的xz平面 的這個投影向量，的夾角
    angle2 = angle_of_axis(e1[0],e1[2],e2[0])  # 側彎 : 舊x軸和，新x軸投影到以舊z軸為法向量的xy平面 的這個投影向量，的夾角
    angle3 = angle_of_axis(e1[1],e1[0],e2[1])  # 旋轉 : 舊y軸和，新y軸投影到以舊x軸為法向量的yz平面 的這個投影向量，的夾角
    return angle1, angle2, angle3

def func_three_angle(path,dirs,way,):

    d_angle = {} # 前後、側彎、旋轉的最大值

    e_basic = {}

    way_set1 = [1,2,3,4,5] #前彎
    way_set2 = [6,7,8,9,10] #右側
    way_set3 = [11,12,13,14,15] #右旋
    for d in dirs:  # for zero in every people
        d_angle[d] = [0,0,0] # 順便初始化，d_front[mine]=[angle1, angle2, angle3] 表示前、側、旋的夾角

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

            angles = [[] for _ in range(5)]
            for i in range(5):
                angles[i] = three_angle_of_eulers(e_basic[d][i],e[i]) #angles[0] = [angle1, angle2, angle3] 表示sensor1變化的三個角度
            print(f'angles = {angles}')

            if int(w) in way_set1:
                k = 0
            elif int(w) in way_set2:
                k = 1
            elif int(w) in way_set3:
                k = 2
            else:
                continue
            d_angle[d][k] += angles[k] 

            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()

    d_angle 現在都是5倍 ( 因為每個動作有5個Way )
    接下來就是拿當下的值去和最大限度算k 


euler_to_3vector([0.103113309, -0.506458759 ,   -147.123291])
euler_to_3vector([-0.071697503,    1.085567594, -171.6932068])
euler_to_3vector([-0.651638448,    -0.581820488,    32.06290436])
euler_to_3vector([-0.448454171,    -0.042662635,    -62.60937881])
euler_to_3vector([23.67301178, -29.45196342,    105.3321152])
euler_to_3vector([70,43,43])
euler_to_vector([70,43,43])
'''
0.103113309 -0.506458759    -147.123291
-0.071697503    1.085567594 -171.6932068
-0.651638448    -0.581820488    32.06290436
-0.448454171    -0.042662635    -62.60937881
23.67301178 -29.45196342    105.3321152
'''
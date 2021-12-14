import math
import numpy as np

def ntz(x): # negative to zero 
    if x < 0:
        return 0
    return x
def find_three(index, score, all_matrix, num_decisiontree ,list_three):
    list_three.append((index,score, all_matrix))
    list_three = sorted(list_three, reverse = True, key = lambda s: s[1])
    while len(list_three) > num_decisiontree :
        list_three.pop()
    return list_three

def euler_from_quaternion(q):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        w,x,y,z=q[0],q[1],q[2],q[3]
        t0 = +2.0 * (w * x + y * z) 
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return [roll_x/math.pi*180, pitch_y/math.pi*180, yaw_z/math.pi*180] 
def qua_diff(q1,q2):  # mean how to from q1 to q2 --> q1 * z = q2
    n_q1=normm(q1)
    #print(f'norm = {n_q1}')
    n_q2=normm(q2)

    q1=[q1[0]/n_q1, q1[1]/n_q1, q1[2]/n_q1, q1[3]/n_q1] #會變成單位四元數  類似單位向量

    q2=[q2[0]/n_q2, q2[1]/n_q2, q2[2]/n_q2, q2[3]/n_q2]

    a=q1[0]; b=-q1[1]; c=-q1[2]; d=-q1[3]
    
    e=q2[0]; f=q2[1]; g=q2[2]; h=q2[3]
    
    z = [(a*e - b*f -c* g- d*h), (b*e + a*f + c*h- d*g) , (a*g - b*h+ c*e + d*f) , (a*h + b*g - c*f + d*e)]
    
    return z
def quaternion_from_euler(e):
    #Z, Y, X (yaw, pitch, roll),
    roll, pitch, yaw = e[0]*math.pi/180, e[1]*math.pi/180,e[2]*math.pi/180

    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return [qw, qx, qy, qz]
def cal_angle(q1, q2):
    
    flag = 1

    #print(f'flag  = 1 ')
    if flag == 1 :
        e1 = euler_from_quaternion(q1)
        e2 = euler_from_quaternion(q2)
        return abs(cal_angle_new(e1,e2))
    
    else : 
        n_q1=normm(q1)
        n_q2=normm(q2)
        #print(f'norm {n_q2}')
        angle = (math.acos(q1[0]*q2[0] + q1[1]*q2[1] +q1[2]*q2[2] + q1[3]*q2[3]) *180/math.pi)*2
        #print(angle)
        #print(f'angle = {math.acos(q1[0]*q2[0] + q1[1]*q2[1] +q1[2]*q2[2] + q1[3]*q2[3])*180/math.pi} * 2 \n')
        return angle
        #print(f'angle = {math.acos(q1[0]*q2[0] + q1[1]*q2[1] +q1[2]*q2[2] + q1[3]*q2[3])*180/math.pi} * 2 \n')
    
def normm(qua):
    sum=0
    for i in range(len(qua)):
      sum+=qua[i]**2
    sum=sum**0.5
    return sum
def euler_transfer(a):
    #input('transfer')
    if a[0] > 90 or a[0] < -90:
        #print('transfer')
        a[0]=180-a[0]
        a[1]=180-a[1]
        a[2]=-(180-a[2])

    return a
    
 
def euler_to_vector(e):
    #Z, Y, X (yaw, pitch, roll),
    roll, pitch, yaw = e[0]*math.pi/180, e[1]*math.pi/180,e[2]*math.pi/180

    x = math.cos(yaw)*math.cos(pitch)
    y = math.sin(yaw)*math.cos(pitch)
    z = math.sin(pitch)
    return [x,y,z]
def angle_between_vector(v1, v2):
    #α = arccos[(a · b) / (|a| * |b|)]
    dot = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
    norm_v1= normm(v1)
    norm_v2= normm(v2)
    return math.acos(dot/(norm_v1*norm_v2))*180/math.pi
def cal_angle_new(e1,e2):
    v1=euler_to_vector(e1)
    v2=euler_to_vector(e2)
    return angle_between_vector(v1,v2)
def euler_to_dcm(e1,e2): # w, x , y ,z
    q1=quaternion_from_euler(e1)
    q2=quaternion_from_euler(e2)
    return qua_to_dcm(q1,q2)
def acos_360(x):
    return abs(math.acos(x)*180/math.pi)
def qua_to_dcm(q1,q2):
    q=qua_diff(q1,q2)
    w,x,y,z=q[0],q[1],q[2],q[3] #ppt w,x,y,z = q4,q1,q2,q3
    tmp1 = w**2+x**2-y**2-z**2
    tmp2 = w**2-x**2+y**2-z**2
    tmp3 = w**2-x**2-y**2+z**2
    if tmp1 > 1 :
        #print('error', tmp1)
        tmp1=1
    if tmp1 < -1:
        #print('error', tmp1)
        tmp1=-1
    if tmp2 > 1 :
        #print('error', tmp2)
        tmp2=1
    if tmp2 < -1:
        #print('error', tmp2)
        tmp2=-1
    if tmp3 > 1 :
        #print('error', tmp3)
        tmp3=1
    if tmp3 < -1:
        #print('error', tmp3)
        tmp3=-1

    angle1=abs(math.acos(tmp1)*180/math.pi)
    angle2=abs(math.acos(tmp2)*180/math.pi)
    angle3=abs(math.acos(tmp3)*180/math.pi)
    #print(angle1,angle2,angle3)
    #----------------------------------------------- for every element in dcm
    
    print(f'dcm matrix \n')
    print(f'{tmp1}\t{2*(x*y+z*w)}\t{2*(x*z-y*w)}')
    print(f'{2*(x*y-z*w)}\t{tmp2}\t{2*(y*z+x*w)}')
    print(f'{2*(x*z+y*w)}\t{2*(y*z-x*w)}\t{tmp3}')
    
    '''
    print(f'\nangle')
    print(f'{acos_360(tmp1)}\t{acos_360(2*(x*y+z*w))}\t{acos_360(2*(x*z-y*w))}')
    print(f'{acos_360(2*(x*y-z*w))}\t{acos_360(tmp2)}\t{acos_360(2*(y*z+x*w))}')
    print(f'{acos_360(2*(x*z+y*w))}\t{acos_360(2*(y*z-x*w))}\t{acos_360(tmp3)}')
    print('----------------------------------')
    '''
    #-----------------------------------------------
    return angle1,angle2, angle3
def choose_type(x,y,z):
    print(x,y,z)
    if x == min(x,y,z):
        return 2
    if y == min(x,y,z):
        return 1
    else:
        return 0
def threshold_funcion(dx_12, max_dx_12,  dy_12, max_dy_12, dz_12, max_dz_12, dx_13, \
                        max_dx_13, dy_13, max_dy_13, dz_13, max_dz_13,balance):
    #balance_1 = 1
    #balance_2 = 8.2 #mine
    #balance_3 = 6.6
    #balance_2 = 2.2 #room
    #balance_3 = 7.1
    '''
    for i in range(3):
        balance[i] = math.sqrt(balance[i])
    '''
    balance_1 = balance[0]
    balance_2 = balance[1]
    balance_3 = balance[2]
    
    '''
    balance_1 = 1
    balance_2 = 8.2 #mine
    balance_3 = 6.6
    '''
    #input(balance)

    k = 1 # for not  division by zero
    #print(dx_12, max_dx_12,  dy_12, max_dy_12, dz_12, max_dz_12, dx_13, \
    #                    max_dx_13, dy_13, max_dy_13, dz_13, max_dz_13)
    #input()
    #return (dx_12/max_dx_12)**2+(dy_12/max_dy_12)**2+(dz_12/max_dz_12)**2+\
    #        ntz((dx_12-dy_12)/(dx_12+k))*balance_1 + ntz((dx_12-dz_12)/(dx_12+k))*balance_2 + ntz((dz_12-dx_12)/(dz_12+k))*balance_3
    
    return (dx_12/max_dx_12)**2+(dy_12/max_dy_12)**2+(dz_12/max_dz_12)**2+\
            (dx_13/max_dx_13)**2+(dy_13/max_dy_13)**2+(dz_13/max_dz_13)**2+\
            ntz((dx_12-dy_12)/(dx_12+k))*balance_1 + ntz((dx_12-dz_12)/(dx_12+k))*balance_2 + ntz((dz_12-dx_12)/(dz_12+k))*balance_3
    
    return (dx_12/max_dx_12)**2+(dy_12/max_dy_12)**2+(dz_12/max_dz_12)**2+\
            (dx_13/max_dx_13)**2+(dy_13/max_dy_13)**2+(dz_13/max_dz_13)**2+\
            ntz((dx_12-dy_12)/max_dx_12)*balance_1 + ntz((dx_12-dz_12)/max_dx_12)*balance_2 + ntz((dz_12-dx_12)/max_dz_12)*balance_3
        
    return (dx_12/max_dx_12)**2+(dy_12/max_dy_12)**2+(dz_12/max_dz_12)**2+\
            (dx_13/max_dx_13)**2+(dy_13/max_dy_13)**2+(dz_13/max_dz_13)**2+\
            ntz((dx_12-dy_12)/(dx_12+k))*balance_1 + ntz((dx_12-dz_12)/(dx_12+k))*balance_2 + ntz((dz_12-dx_12)/(dz_12+k))*balance_3

    #return [dx_12, dy_12, dz_12, dx_13,dy_13,dz_13, value]
def weighting_function(w):
    return 1/w
def make_difference_dataset(dest,path,way,num_row,ban,dir, set_zero, use_transfer):
    fp = open(dest,'w') 
    q_basic = {}
    for dire in dir:  # for zero
        q_basic[dire] = [[],[],[],[],[]]
        for i in range(5):
            with open(f'{path}/{dire}/0/{i+1}.csv') as f:
                f.readline() #ignore first line
                temp = f.readline().strip().split(',')
                #print(temp)
                q_basic[dire][i]= quaternion_from_euler([float(k) for k in temp[2:]])
                #if i == 2:
                #    print(f'basic sensor {i+1} : {temp[4]}')
                #    pass
                if set_zero == 2 or set_zero == 3:  # mean no zero
                    q_basic[dire][i]=[1,0,0,0]
        #print(f'q_basic = {q_basic}')
    for idx_move,w in enumerate(way): # for every way
        value = idx_move
        #print(f'\nway : {value}')
        for dire in dir: # for every person
            s1 = open(f'{path}/{dire}/{w}/1.csv','r') #f mean sensor
            s2 = open(f'{path}/{dire}/{w}/2.csv','r')
            s3 = open(f'{path}/{dire}/{w}/3.csv','r')
            s4 = open(f'{path}/{dire}/{w}/4.csv','r')
            s5 = open(f'{path}/{dire}/{w}/5.csv','r') 
            
            all_sensor = [s1,s2,s3,s4,s5] 
            #other_sensor = [s1, s2, s4, s5] #ignore s3
            e=[[],[],[],[],[]] #for every sensor
            q=[[],[],[],[],[]] #for every sensor
            d=[[],[],[],[],[]] #for every sensor , mean difference euler
            for f in all_sensor: #each sensor
                each_line = f.readline()#first line
                #print(f, each_line)
                #print(each_line)

            #num_row_balance = num_row * (len(way)-1) if value == 0 else num_row  # number of good  need to = number of bad
            num_row_balance = num_row
            for i in range(num_row_balance):   # for every row
                each_row = []

                s3_line = s3.readline()
                #input(s3_line)
                each_list = s3_line.strip().split(',')
                e[2] = [float(k) for k in each_list[2:]] #sensor 3
                #print(f'sensor 3 angle z : {e[2][2]}')
                q[2]= quaternion_from_euler(e[2])
                d[2]= qua_diff(q_basic[dire][2],q[2]) #difference with zero 
                #print(f'sensor 3 zero angle z : {euler_from_quaternion(d[2])[2]}')
                e[2]= euler_from_quaternion(d[2]) 
                for idx,f in enumerate(all_sensor): #each sensor
                    if idx == 2:
                        #print('ignore sensor 3')

                        #e[2] = [0,0]
                        if 2 in ban:
                            e[2]=[0,0,0]
                        '''
                        each_row.append(e[idx][0])
                        each_row.append(e[idx][1])
                        '''
                        each_row.append(math.sin(e[idx][0]/180*math.pi))
                        each_row.append(math.cos(e[idx][0]/180*math.pi))
                        each_row.append(math.sin(e[idx][1]/180*math.pi))
                        each_row.append(math.cos(e[idx][1]/180*math.pi))
                        
                    else: 
                        each_line = f.readline()
                        #print(each_line)
                        #print(f'idx = {idx}')
                        each_list = each_line.strip().split(',')
                        e[idx] = [float(k) for k in each_list[2:]]
                        
                        #if e[idx][0] > 90:
                            #print(f'wrong : way {w} sensor {idx+1} angle {e[idx][0]}')
                        #if idx == 1 : # sensor 2 , top sensor
                            #print(f'sensor 2 angle : {e[idx][2]}')
                        #if idx == 3 : # sensor 2 , top sensor
                            #print(f'sensor 4 angle : {e[idx][2]}')
                            #pass
                        q[idx]= quaternion_from_euler(e[idx])
                        d[idx]= qua_diff(q_basic[dire][idx],q[idx])
                        #if idx == 1:
                            #print(f'sensor 2 zero angle z : {euler_from_quaternion(d[idx])[2]}')
                        #if idx == 3:
                            #print(f'sensor 4 zero angle z : {euler_from_quaternion(d[idx])[2]}')
                            #pass
                        if set_zero != 1 or set_zero != 3: # 1 mean only zero , no difference
                            d[idx]= qua_diff(d[2],d[idx]) #  not 1 mean you have to use difference
                        
                        e[idx]= euler_from_quaternion(d[idx])
                        #print(e[idx])
                        #if idx == 1 : # sensor 2 , top sensor
                        #    print(f'difference angle : {e[idx][2]}\n')
                        
                        if idx in ban:
                            e[idx]=[0,0,0]
                        if use_transfer == 1:
                            e[idx]=euler_transfer(e[idx])




                        #e[idx][] = 0 
                        #e[idx][2] = 0 

                        '''
                        each_row.append(e[idx][0]/180*math.pi)
                        each_row.append(e[idx][1]/180*math.pi)
                        each_row.append(e[idx][2]/180*math.pi)

                        '''
                        
                        angle_case = 1
                        if angle_case :
                            e[idx][0]=0
                            e[idx][2]=0
                            value = int(value !=0)
                            #pass
                        print(f'{dire} {value} {e[idx][1]}')
                        each_row.append(math.sin(e[idx][0]/180*math.pi))
                        each_row.append(math.cos(e[idx][0]/180*math.pi))
                        each_row.append(math.sin(e[idx][1]/180*math.pi))
                        each_row.append(math.cos(e[idx][1]/180*math.pi))
                        each_row.append(math.sin(e[idx][2]/180*math.pi))
                        each_row.append(math.cos(e[idx][2]/180*math.pi))
                        
                        
                each_row.append(value)

                #input(each_row)
                #each_row = [str(k) for k in each_row]
                each_row = list(map(lambda k : str(k), each_row )) # float list to string list
                #print(len(each_row))
                fp.write(','.join(each_row)+'\n') # string list to string
                num_feature = len(each_row)
                #print(num_feature)
                    

            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()

    fp.close()
    #print(num_feature)
    return num_feature-1
    
def my_classfier(path,way,dir, good_set, threshold):

    # for zero --------------------------------------------------------------------
    q_basic = {}
    for dire in dir:  # for zero            
        temp_q=[] #for zero sensor's euler to quaternion
        q_basic[dire] = [[],[],[]]

        for i in range(5):
            with open(f'{path}/{dire}/0/{i+1}.csv') as f:
                f.readline() #ignore first line
                temp = f.readline().strip().split(',')
                temp_q.append(quaternion_from_euler([float(k) for k in temp[2:]]))

        q_basic[dire] = [temp_q[0],temp_q[1],temp_q[2]]
        #if set_zero == 0 :# 0 mean not zero
            #q_basic[dire] = [0,0,0]
    #print(f'q_basic  = {q_basic}')
    #input(q_basic)
    #------------------------------------------------------------------------------
    for idx_move,w in enumerate(way): # for every way
        #num_feature = 0
        value = int(idx_move not in good_set) # if good then 0  , bad than 1 

        for dire in dir: # for every person 
            s1 = open(f'{path}/{dire}/{w}/1.csv','r') #f mean sensor
            s2 = open(f'{path}/{dire}/{w}/2.csv','r')
            s3 = open(f'{path}/{dire}/{w}/3.csv','r')
            s4 = open(f'{path}/{dire}/{w}/4.csv','r')
            s5 = open(f'{path}/{dire}/{w}/5.csv','r') 
            
            all_sensor = [s1,s2,s3,s4,s5] 
            e=[[],[],[],[],[]] #for every sensor's euler
            q=[[],[],[],[],[]] #for every sensor's euler to quaternion
            for f in all_sensor: #each sensor
                each_line = f.readline()#first line

            num_row_balance = 1 # check one tiem is ok 
            for i in range(num_row_balance): # for every row
                each_row = []
                #input()
                for idx,f in enumerate(all_sensor): #each sensor
                    each_line = f.readline()
                    each_list = each_line.strip().split(',') # string to list
                    e[idx] = [float(k) for k in each_list[2:]] # get sensor

                    q[idx]= quaternion_from_euler(e[idx])

                diff=[cal_angle(q[0],q[1]),cal_angle(q[2],q[0]), cal_angle(q[2],q[1])]
                    
                #if set_zero == 1 :
                    #input(q_basic[dire][1])
                temp = [cal_angle(q_basic[dire][1], q_basic[dire][0]) ,cal_angle(q_basic[dire][0], q_basic[dire][2]), cal_angle(q_basic[dire][1], q_basic[dire][2])]
                temp2 = [abs(diff[0]-temp[0]),abs(diff[1]-temp[1]),abs(diff[2]-temp[2])]
                diff = temp2
                #if set_zero == 2 :
                temp = [cal_angle(q[0], q_basic[dire][0]),cal_angle(q[1], q_basic[dire][1]),cal_angle(q[2], q_basic[dire][2])]
                temp2 = [abs(temp[1]-temp[0]),abs(temp[0]-temp[2]),abs(temp[2]-temp[1])]
                for t in temp2:
                    diff.append(t)

                for d in diff:
                    each_row.append(d)

                each_row.append(value)
                #input(f'{dire} {w} {each_row}')
                if each_row[0]<threshold and each_row[1] <threshold and each_row[2]<threshold and each_row[3]<threshold and each_row[4] <threshold and each_row[5]<threshold:

                    #input(int(w in good_set)
                    if int(w) in good_set :
                        #print('correct')
                        pass
                    else:
                        print(each_row)
                        print(f'{dire} {w} wrong')
                else:
                    #print(f'way {w} is bad')
                    if int(w) not in good_set:
                        #print('correct')
                        pass 
                    else:
                        print(each_row)
                        print(f'{dire}  {w} wrong')

                if (abs(abs(e[0][0])-0) > abs(abs(e[0][0])-180)):
                    #print(f'way {w} is back way')
                    #print(f'{dire} {w} back {e[0][0]}')
                    pass
                #print()
                
            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()

def my_dcm_init(path,init_way,dir,path_t,move_way,dir_t,weight):
    use_sensor13 = 0

    dx_12 =  {} #sensor 1 2  x  difference , dx['mine'] ...
    dy_12 =  {}
    dz_12 =  {}
    dx_13 =  {}
    dy_13 =  {}
    dz_13 =  {}
    
    max_dx_12 =  {}
    max_dy_12 =  {}
    max_dz_12 =  {}
    max_dx_13 =  {}
    max_dy_13 =  {}
    max_dz_13 =  {}

    way_set1 = [1,2,3,4,5] #前彎
    way_set2 = [6,7,8,9,10] #右側
    way_set3 = [11,12,13,14,15] #右旋
    # for zero --------------------------------------------------------------------
    e_basic = {}
    for dire in dir:  # for zero
        e_basic[dire] = [[],[],[],[],[]]
        
        dx_12[dire] = [0,0,0]  
        dy_12[dire] = [0,0,0]  
        dz_12[dire] = [0,0,0]  
        dx_13[dire] = [0,0,0]  
        dy_13[dire] = [0,0,0]  
        dz_13[dire] = [0,0,0]  
        
        for i in range(5):
            with open(f'{path}/{dire}/0/{i+1}.csv') as f:
                f.readline() #ignore first line
                temp = f.readline().strip().split(',')
                #print(temp)
                e_basic[dire][i]= [float(k) for k in temp[2:]]
        
        if use_sensor13 == 1:
            e_basic[dire][0] = e_basic[dire][2]        

    #------------------------------------------------------------------------------


    for idx_move,w in enumerate(init_way): # for every way
        #num_feature = 0
        #value = int(idx_move not in good_set) # if good then 0  , bad than 1 

        for dire in dir: # for every person 

            s1 = open(f'{path}/{dire}/{w}/1.csv','r') #f mean sensor
            s2 = open(f'{path}/{dire}/{w}/2.csv','r')
            s3 = open(f'{path}/{dire}/{w}/3.csv','r')
            s4 = open(f'{path}/{dire}/{w}/4.csv','r')
            s5 = open(f'{path}/{dire}/{w}/5.csv','r')

            all_sensor = [s1,s2,s3,s4,s5] 
            if use_sensor13 == 1:
                all_sensor = [s3,s2,s3,s4,s5] 

            e=[[],[],[],[],[]] #for every sensor's euler
            q=[[],[],[],[],[]] #for every sensor's euler to quaternion
            for f in all_sensor: #each sensor
                each_line = f.readline()#first line

            num_row_balance = 1 # check one tiem is ok 
            for i in range(num_row_balance): # for every row
                each_row = []
                #input()
                for idx,f in enumerate(all_sensor): #each sensor
                    each_line = f.readline()
                    each_list = each_line.strip().split(',') # string to list
                    e[idx] = [float(k) for k in each_list[2:]] # get sensor

                    #q[idx]= quaternion_from_euler(e[idx])
                #print(f'way = {w}')
                #print(f'sensor 1 difference')
                angle_1x, angle_1y, angle_1z  =euler_to_dcm(e_basic[dire][0],e[0]) #sensor 1
                #print(f'sensor 2 difference  ( change to sensor 5 )')
                angle_2x, angle_2y, angle_2z  =euler_to_dcm(e_basic[dire][4],e[4]) #sensor 2
                #print(f'sensor 3 difference')
                #print(angle_2x, angle_2y, angle_2z)
                angle_3x, angle_3y, angle_3z  =euler_to_dcm(e_basic[dire][2],e[2]) #sensor 3
                '''
                print(f'sensor 4 difference')
                angle_4x, angle_4y, angle_4z  =euler_to_dcm(e_basic[dire][3],e[3]) #sensor 4
                print(f'sensor 5 difference')
                angle_5x, angle_5y, angle_5z  =euler_to_dcm(e_basic[dire][4],e[4]) #sensor 5
                
                input()
                '''
                # -------------------------- one way five time
                if int(w) in way_set1:
                    k = 0
                elif int(w) in way_set2:
                    k = 1
                elif int(w) in way_set3:
                    k = 2
                else:
                    continue
                #print(f'k = {k}')
                '''
                print(f'{angle_1z}')
                print(f'{angle_2z}')
                print(f'way_set = {k+1} {abs(angle_1z-angle_2z)} ')
                print(f'now dz = {dz_12[k]}')
                '''
                dx_12[dire][k] += abs(angle_1x-angle_2x)
                dy_12[dire][k] += abs(angle_1y-angle_2y)
                dz_12[dire][k] += abs(angle_1z-angle_2z)

                dx_13[dire][k] += abs(angle_1x-angle_3x)
                dy_13[dire][k] += abs(angle_1y-angle_3y)
                dz_13[dire][k] += abs(angle_1z-angle_3z)



                #print(f' dx_12 = {dx_12}')

            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()
    thres = {}
    balance = {}
    for dire in dir: # for every person threshold
        tmp = 5   # 5 是為了平均   

        #tmp *= weighting_function(weight) #threshold weighting
        dx_12[dire] = list(map(lambda x:x/tmp, dx_12[dire]))
        dy_12[dire] = list(map(lambda x:x/tmp, dy_12[dire]))
        dz_12[dire] = list(map(lambda x:x/tmp, dz_12[dire]))
        dx_13[dire] = list(map(lambda x:x/tmp, dx_13[dire]))
        dy_13[dire] = list(map(lambda x:x/tmp, dy_13[dire]))
        dz_13[dire] = list(map(lambda x:x/tmp, dz_13[dire]))
        print('maximum is ....')
        print(f' dx_12 = {dx_12}')
        print(f' dy_12 = {dy_12}')
        print(f' dz_12 = {dz_12}')
        print(f' dx_13 = {dx_13}')
        print(f' dy_13 = {dy_13}')
        print(f' dz_13 = {dz_13}')


        temp = [0,0,0]
        for i in range(3):
            temp[i] = dx_12[dire][i]**2+dy_12[dire][i]**2+dz_12[dire][i]**2
            print(dx_12[dire][i]**2+dy_12[dire][i]**2+dz_12[dire][i]**2)
            print(i)
        #balance[dire] = [1,temp[0]/temp[1],temp[0]/temp[2]]


        max_dx_12[dire] = max(dx_12[dire][0],dx_12[dire][1],dx_12[dire][2])
        max_dy_12[dire] = max(dy_12[dire][0],dy_12[dire][1],dy_12[dire][2])
        max_dz_12[dire] = max(dz_12[dire][0],dz_12[dire][1],dz_12[dire][2])

        max_dx_13[dire] = max(dx_13[dire][0],dx_13[dire][1],dx_13[dire][2])
        max_dy_13[dire] = max(dy_13[dire][0],dy_13[dire][1],dy_13[dire][2])
        max_dz_13[dire] = max(dz_13[dire][0],dz_13[dire][1],dz_13[dire][2]) 
        
        temp[0] = dx_12[dire][0]/max_dx_12[dire] + dy_12[dire][0]/max_dy_12[dire] + dz_12[dire][0]/max_dz_12[dire]
        temp[1] = dx_12[dire][1]/max_dx_12[dire] + dy_12[dire][1]/max_dy_12[dire] + dz_12[dire][1]/max_dz_12[dire]
        temp[2] = dx_12[dire][2]/max_dx_12[dire] + dy_12[dire][2]/max_dy_12[dire] + dz_12[dire][2]/max_dz_12[dire]
        balance[dire] = [1,temp[0]/temp[1],temp[0]/temp[2]]
        '''
        thres_set_1 = threshold_funcion(dx_12[dire][0], dy_12[dire][0], dz_12[dire][0], dx_13[dire][0], dy_13[dire][0], dz_13[dire][0]) #這裡已經算過threshold weighting了

        thres_set_2 = threshold_funcion(dx_12[dire][1], dy_12[dire][1], dz_12[dire][1], dx_13[dire][1], dy_13[dire][1], dz_13[dire][1])
        thres_set_3 = threshold_funcion(dx_12[dire][2], dy_12[dire][2], dz_12[dire][2], dx_13[dire][2], dy_13[dire][2], dz_13[dire][2])
        thres[dire] = [thres_set_1,thres_set_2,thres_set_3] 
        '''

    #print(thres)
    
    #------------------------------------------------------------------------------------ for test  ways row

    # for zero --------------------------------------------------------------------
    e_basic = {}
    for dire in dir_t:  # for zero
        e_basic[dire] = [[],[],[],[],[]]

        for i in range(5):
            with open(f'{path_t}/{dire}/0/{i+1}.csv') as f:
                f.readline() #ignore first line
                temp = f.readline().strip().split(',')
                #print(temp)
                e_basic[dire][i]= [float(k) for k in temp[2:]]

                

    for idx_move,w in enumerate(move_way): # for every way
        #print(idx_move)
        if idx_move % 4 ==1:
            print()
        #num_feature = 0
        #value = int(idx_move not in good_set) # if good then 0  , bad than 1 

        for dire in dir_t: # for every person 
            s1 = open(f'{path_t}/{dire}/{w}/1.csv','r') #f mean sensor
            s2 = open(f'{path_t}/{dire}/{w}/2.csv','r')
            s3 = open(f'{path_t}/{dire}/{w}/3.csv','r')
            s4 = open(f'{path_t}/{dire}/{w}/4.csv','r')
            s5 = open(f'{path_t}/{dire}/{w}/5.csv','r') 
            
            all_sensor = [s1,s2,s3,s4,s5] 
            if use_sensor13 == 1:
                all_sensor = [s3,s2,s3,s4,s5] 

            e=[[],[],[],[],[]] #for every sensor's euler
            q=[[],[],[],[],[]] #for every sensor's euler to quaternion
            for f in all_sensor: #each sensor
                each_line = f.readline()#first line

            num_row_balance = 1 # check one tiem is ok 
            for i in range(num_row_balance): # for every row
                each_row = []
                #input()
                for idx,f in enumerate(all_sensor): #each sensor
                    each_line = f.readline()
                    each_list = each_line.strip().split(',') # string to list
                    e[idx] = [float(k) for k in each_list[2:]] # get sensor

                    #q[idx]= quaternion_from_euler(e[idx])

                angle_1x, angle_1y, angle_1z  =  euler_to_dcm(e_basic[dire][0],e[0])
                angle_2x, angle_2y, angle_2z  =  euler_to_dcm(e_basic[dire][1],e[1])
                angle_3x, angle_3y, angle_3z  =  euler_to_dcm(e_basic[dire][2],e[2])

                angle_12x = abs(angle_1x-angle_2x)
                angle_12y = abs(angle_1y-angle_2y)
                angle_12z = abs(angle_1z-angle_2z)
                angle_13x = abs(angle_1x-angle_3x)
                angle_13y = abs(angle_1y-angle_3y)
                angle_13z = abs(angle_1z-angle_3z)
                '''
                choose = choose_type(angle_12x,angle_12y,angle_12z) #choose the rotate direction
                print(f'choose = {choose}')
                
                print('threshold is ....')
                print(f' dx_12 = {dx_12}')
                print(f' dy_12 = {dy_12}')
                print(f' dz_12 = {dz_12}')
                print(f' dx_13 = {dx_13}')
                print(f' dy_13 = {dy_13}')
                print(f' dz_13 = {dz_13}')
                input('correct?')
                '''
                #print(angle_12x)
                #k_value = threshold_funcion(angle_12x, angle_12y, angle_12z, angle_13x, angle_13y, angle_13z)
                k_value = threshold_funcion(angle_12x,max_dx_12[dire], angle_12y,max_dy_12[dire], \
                    angle_12z,max_dz_12[dire], angle_13x,max_dx_13[dire], angle_13y,max_dy_13[dire], angle_13z,max_dz_13[dire],balance[dire])
                #if k_value > thres[dire][choose]:
                '''
                if k_value > 2:
                    print(f'bad')
                else:
                    print('good')
                '''
                print(f'k_value = {k_value}')
            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()


def my_dcm_classfier(path,way,dir, good_set, threshold):

    # for zero --------------------------------------------------------------------
    e_basic = {}
    for dire in dir:  # for zero
        e_basic[dire] = [[],[],[],[],[]]

        for i in range(5):
            with open(f'{path}/{dire}/0/{i+1}.csv') as f:
                f.readline() #ignore first line
                temp = f.readline().strip().split(',')
                #print(temp)
                e_basic[dire][i]= [float(k) for k in temp[2:]]

                

    #------------------------------------------------------------------------------
    for idx_move,w in enumerate(way): # for every way
        #num_feature = 0
        #value = int(idx_move not in good_set) # if good then 0  , bad than 1 
        value = int(idx_move)
        for dire in dir: # for every person 
            s1 = open(f'{path}/{dire}/{w}/1.csv','r') #f mean sensor
            s2 = open(f'{path}/{dire}/{w}/2.csv','r')
            s3 = open(f'{path}/{dire}/{w}/3.csv','r')
            s4 = open(f'{path}/{dire}/{w}/4.csv','r')
            s5 = open(f'{path}/{dire}/{w}/5.csv','r') 
            
            all_sensor = [s1,s2,s3,s4,s5] 
            e=[[],[],[],[],[]] #for every sensor's euler
            q=[[],[],[],[],[]] #for every sensor's euler to quaternion
            for f in all_sensor: #each sensor
                each_line = f.readline()#first line

            num_row_balance = 1 # check one tiem is ok 
            for i in range(num_row_balance): # for every row
                each_row = []
                #input()
                for idx,f in enumerate(all_sensor): #each sensor
                    each_line = f.readline()
                    each_list = each_line.strip().split(',') # string to list
                    e[idx] = [float(k) for k in each_list[2:]] # get sensor

                    #q[idx]= quaternion_from_euler(e[idx])

                angle_1x, angle_1y, angle_1z  =euler_to_dcm(e_basic[dire][0],e[0])
                angle_2x, angle_2y, angle_2z  =euler_to_dcm(e_basic[dire][1],e[1])
                angle_3x, angle_3y, angle_3z  =euler_to_dcm(e_basic[dire][2],e[2])
                '''
                b_angle_12x,b_angle_12y,b_angle_12z = euler_to_dcm(e_basic[dire][0],e_basic[dire][1])
                b_angle_13x,b_angle_13y,b_angle_13z = euler_to_dcm(e_basic[dire][2],e_basic[dire][0])
                angle_12x,angle_12y,angle_12z = euler_to_dcm(e[0],e[1])
                angle_13x,angle_13y,angle_13z = euler_to_dcm(e[2],e[0])
                
                each_row.append(abs(angle_12x-b_angle_12x))
                each_row.append(abs(angle_12y-b_angle_12y))
                each_row.append(abs(angle_12z-b_angle_12z))
                each_row.append(abs(angle_13x-b_angle_13x))
                each_row.append(abs(angle_13y-b_angle_13y))
                each_row.append(abs(angle_13z-b_angle_13z))
                '''

                each_row.append(abs(angle_1x-angle_2x))
                each_row.append(abs(angle_1y-angle_2y))
                each_row.append(abs(angle_1z-angle_2z))
                each_row.append(abs(angle_1x-angle_3x))
                each_row.append(abs(angle_1y-angle_3y))
                each_row.append(abs(angle_1z-angle_3z))

                '''
                if each_row[0]<threshold and each_row[1] <threshold and each_row[2]<threshold and each_row[3]<threshold and each_row[4] <threshold and each_row[5]<threshold:

                    #input(int(w in good_set)
                    if int(w) in good_set :
                        print('correct')
                        pass
                    else:
                        print(each_row)
                        print(f'{dire} {w} wrong')
                else:
                    #print(f'way {w} is bad')
                    if int(w) not in good_set:
                        print('correct')
                        pass 
                    else:
                        print(each_row)
                        print(f'{dire}  {w} wrong')
                '''
                print(f' {w}, {each_row}')
                #if (abs(abs(e[0][0])-0) > abs(abs(e[0][0])-180)):
                    #print(f'way {w} is back way')
                    #print(f'{dire} {w} back {e[0][0]}')
                    #pass
                #print()
                
            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()

def make_dcm_dataset(dest,path,way,num_row,ban,dir,set_zero, good_set):
    fp = open(dest,'w') 

    first_row = ' '
    fp.write(first_row+'\n')
    #------------------------------for zero
    e_basic = {}
    for dire in dir:  # for zero
        e_basic[dire] = [[],[],[],[],[]]

        for i in range(5):
            with open(f'{path}/{dire}/0/{i+1}.csv') as f:
                f.readline() #ignore first line
                temp = f.readline().strip().split(',')
                #print(temp)
                e_basic[dire][i]= [float(k) for k in temp[2:]]

                if set_zero == 0:  # mean no zero
                    e_basic[dire][i]=[0,0,0]
        print(f'e_basic = {e_basic}')
    for idx_move,w in enumerate(way): # for movement
        value = int(idx_move not in good_set) # if good then 0  , bad than 1 
        #value = idx_move
        #print(f'way = {w}')
        for dire in dir:

            s1 = open(f'{path}/{dire}/{w}/1.csv','r') #f mean sensor
            s2 = open(f'{path}/{dire}/{w}/2.csv','r')
            s3 = open(f'{path}/{dire}/{w}/3.csv','r')
            s4 = open(f'{path}/{dire}/{w}/4.csv','r')
            s5 = open(f'{path}/{dire}/{w}/5.csv','r') 
            
            all_sensor = [s1,s2,s3,s4,s5] 
            e=[[],[],[],[],[]] #for every sensor
            e_backup=[[],[],[],[],[]] 
            q=[[],[],[],[],[]] #for every sensor

            for f in all_sensor: #each sensor
                each_line = f.readline()#first line
                #print(each_line)
            num_row_balance = len(way)-len(good_set) if value == 0 else len(good_set)  # number of good  need to = number of bad
            num_row_balance *= num_row
            #num_row_balance = num_row
            for i in range(num_row_balance):
                each_row = []
                for idx,f in enumerate(all_sensor): #each sensor
                    each_line = f.readline()
                    each_list = each_line.strip().split(',') # string to list
                    e[idx] = [float(k) for k in each_list[2:]] # get sensor

                    #q[idx]= quaternion_from_euler(e[idx])


                b_angle_12x,b_angle_12y,b_angle_12z = euler_to_dcm(e_basic[dire][0],e_basic[dire][1])
                b_angle_13x,b_angle_13y,b_angle_13z = euler_to_dcm(e_basic[dire][2],e_basic[dire][0])
                angle_12x,angle_12y,angle_12z = euler_to_dcm(e[0],e[1])
                angle_13x,angle_13y,angle_13z = euler_to_dcm(e[2],e[0])
                

                each_row.append(abs(angle_12x-b_angle_12x))
                each_row.append(abs(angle_12y-b_angle_12y))
                each_row.append(abs(angle_12z-b_angle_12z))
                each_row.append(abs(angle_13x-b_angle_13x))
                each_row.append(abs(angle_13y-b_angle_13y))
                each_row.append(abs(angle_13z-b_angle_13z))
                
                '''
                each_row.append(angle_12x)
                each_row.append(angle_12y)
                each_row.append(angle_12z)
                each_row.append(angle_13x)
                each_row.append(angle_13y)
                each_row.append(angle_13z)
                '''
                #diff=[cal_angle(q[0],q[1]),cal_angle(q[2],q[0]), cal_angle(q[2],q[1])]
                '''
                for idx,f in enumerate(all_sensor): #each sensor
                    each_line = f.readline()

                    each_list = each_line.strip().split(',')
                    e[idx] = [float(k) for k in each_list[2:]]
                    #print(f'sensor {idx+1} ')
                    angle1, angle2, angle3 = euler_to_dcm(e[idx], e_basic[dire][idx])

                    #angle1, angle2, angle3 =e[idx][0],e[idx][1],e[idx][2]
                    #e_backup[idx]=e[idx]
                    #q[idx]= quaternion_from_euler(e[idx])
                    #euler_x,euler_y,_= euler_from_quaternion([1,0,0,0])

                    if 1 : #三個角度都不會太大，sin cos沒差
                        each_row.append(angle1)
                        each_row.append(angle2)
                        each_row.append(angle3)
                    else :
                        each_row.append(math.sin(angle1/180*math.pi))
                        each_row.append(math.cos(angle1/180*math.pi))
                        each_row.append(math.sin(angle2/180*math.pi))
                        each_row.append(math.cos(angle2/180*math.pi))
                        each_row.append(math.sin(angle3/180*math.pi))
                        each_row.append(math.cos(angle3/180*math.pi))
                    
                '''
                each_row.append(value)

                print(each_row)
                #each_row = [str(k) for k in each_row]
                each_row = list(map(lambda k : str(k), each_row )) # float list to string list
                #print(len(each_row))
                num_feature = len(each_row)
                fp.write(','.join(each_row)+'\n') # string list to string
                    


            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()

    fp.close()
    return num_feature-1

def make_angle_dataset(dest,path,way,num_row,ban,dir,use_sin_cos,set_zero, use_abs, add_diff, good_set):
    fp = open(dest,'w') 

    first_row = 'sensor_12, sensor_13, sensor_23, good_or_bad'
    fp.write(first_row+'\n')

    # for zero --------------------------------------------------------------------
    q_basic = {}
    for dire in dir:  # for zero            
        temp_q=[] #for zero sensor's euler to quaternion
        q_basic[dire] = [[],[],[]]

        for i in range(5):
            with open(f'{path}/{dire}/0/{i+1}.csv') as f:
                f.readline() #ignore first line
                temp = f.readline().strip().split(',')
                temp_q.append(quaternion_from_euler([float(k) for k in temp[2:]]))
        '''
        q_basic[dire][0] = cal_angle(temp_q[0],temp_q[1])
        q_basic[dire][1] = cal_angle(temp_q[2],temp_q[0])
        q_basic[dire][2] = cal_angle(temp_q[2],temp_q[1])

        if set_zero == 2: # 2 mean new way of zero
        '''
        q_basic[dire] = [temp_q[0],temp_q[1],temp_q[2]]
        if set_zero == 0 :# 0 mean not zero
            q_basic[dire] = [0,0,0]
    print(f'q_basic  = {q_basic}')
    #input(q_basic)
    #------------------------------------------------------------------------------
    for idx_move,w in enumerate(way): # for every way
        #num_feature = 0
        value = int(idx_move not in good_set) # if good then 0  , bad than 1 
        #if idx_move ==5 or idx_move ==6:
            #value = 0
        #print(f'\nway : {value}')
        for dire in dir: # for every person 
            s1 = open(f'{path}/{dire}/{w}/1.csv','r') #f mean sensor
            s2 = open(f'{path}/{dire}/{w}/2.csv','r')
            s3 = open(f'{path}/{dire}/{w}/3.csv','r')
            s4 = open(f'{path}/{dire}/{w}/4.csv','r')
            s5 = open(f'{path}/{dire}/{w}/5.csv','r') 
            
            all_sensor = [s1,s2,s3,s4,s5] 
            e=[[],[],[],[],[]] #for every sensor's euler
            q=[[],[],[],[],[]] #for every sensor's euler to quaternion
            for f in all_sensor: #each sensor
                each_line = f.readline()#first line



            num_row_balance = len(way)-len(good_set) if value == 0 else len(good_set)  # number of good  need to = number of bad
            num_row_balance *= num_row
            #input(num_row_balance)
            for i in range(num_row_balance): # for every row
                each_row = []
                #input()
                for idx,f in enumerate(all_sensor): #each sensor
                    each_line = f.readline()
                    each_list = each_line.strip().split(',') # string to list
                    e[idx] = [float(k) for k in each_list[2:]] # get sensor

                    q[idx]= quaternion_from_euler(e[idx])

                
                diff_01 = cal_angle(q[0],q[1])
                diff_20 = cal_angle(q[2],q[0])
                diff_21 = cal_angle(q[2],q[1])


                diff=[diff_01, diff_20, diff_21]
  
                if set_zero == 1 :
                    #input(q_basic[dire][1])
                    temp = [cal_angle(q_basic[dire][1], q_basic[dire][0]) ,cal_angle(q_basic[dire][0], q_basic[dire][2]), cal_angle(q_basic[dire][1], q_basic[dire][2])]
                    temp2 = [abs(diff[0]-temp[0]),abs(diff[1]-temp[1]),abs(diff[2]-temp[2])]
                    diff = temp2
                if set_zero == 2 :
                    temp = [cal_angle(q[0], q_basic[dire][0]),cal_angle(q[1], q_basic[dire][1]),cal_angle(q[2], q_basic[dire][2])]
                    diff = [abs(temp[1]-temp[0]),abs(temp[0]-temp[2]),abs(temp[2]-temp[1])]
                if use_abs == 1:
                    for i in range(3):
                        diff[i]=abs(diff[i])
                for idx in ban :  # ban 0 --> all - 3 ,  ban 2 --> curve
                    diff[idx]=0

                if use_sin_cos == 1 :
                    each_row.append(math.sin(diff[0])) # sensor 2-1
                    each_row.append(math.cos(diff[0])) # sensor 2-1

                    each_row.append(math.sin(diff[1])) # sensor 1-3
                    each_row.append(math.cos(diff[1])) # sensor 1-3

                    each_row.append(math.sin(diff[2])) # sensor 2-3
                    each_row.append(math.cos(diff[2])) # sensor 2-3

                else : 
                    each_row.append(diff[0]) # sensor 2-1
                    each_row.append(diff[1]) # sensor 1-3
                    each_row.append(diff[2]) # sensor 2-3
                    if add_diff == 1:
                        each_row.append(diff[0]+diff[1]) # sensor 2-3
                        each_row[0]=0
                        each_row[1]=0
                each_row.append(value)

                #each_row = [str(k) for k in each_row]
                each_row = list(map(lambda k : str(k), each_row )) # float list to string list
                #print(len(each_row))
                fp.write(','.join(each_row)+'\n') # string list to string
                num_feature = len(each_row)
                #print(num_feature)
                print(dire, w, each_row)
                #print((e[0][0]))
                if (abs(abs(e[0][0])-0) > abs(abs(e[0][0])-180)):
                    pass
                    #print(f'{dire} {w} back {e[0][0]}')
                    
                #print()
                
            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()

    fp.close()
    #print(num_feature)
    return num_feature-1
    
def make_dataset(dest,path,way,num_row,case):
    fp = open(dest,'w') 

    for idx_move,w in enumerate(way): # for every way
        value = idx_move

        s1 = open(f'{path}/{w}/1.csv','r') #f mean sensor
        s2 = open(f'{path}/{w}/2.csv','r')
        s3 = open(f'{path}/{w}/3.csv','r')
        s4 = open(f'{path}/{w}/4.csv','r')
        s5 = open(f'{path}/{w}/5.csv','r') 
        
        all_sensor = [s1,s2,s3,s4,s5] 
        q=[[],[],[],[],[]] #for every sensor

        for f in all_sensor: #each sensor
            each_line = f.readline()#first line
            #print(each_line)
        for i in range(num_row):
            each_row = []

            for idx,f in enumerate(all_sensor): #each sensor
                each_line = f.readline()
                #print(each_line)

                each_list = each_line.strip().split(',')
                q[idx] = [float(k) for k in each_list[2:]]

                euler_x,euler_y,_= euler_from_quaternion(q[idx])
                #euler_x,euler_y,_= euler_from_quaternion([1,0,0,0])

                each_row.append(math.sin(euler_x/180*math.pi))
                each_row.append(math.cos(euler_x/180*math.pi))
                each_row.append(math.sin(euler_y/180*math.pi))
                each_row.append(math.cos(euler_y/180*math.pi))

            if case == 2: 
                each_row.append(cal_angle(q[0], q[1])) #s1 s2
                each_row.append(cal_angle(q[1], q[2])) #s2 s3
            if case == 4: 
                diff01=cal_angle(q[0], q[1])
                diff12=cal_angle(q[1], q[2])
                each_row.append(math.sin(diff01)) #s1 s2
                each_row.append(math.cos(diff01)) #s1 s2
                each_row.append(math.sin(diff12)) #s2 s3
                each_row.append(math.sin(diff12)) #s2 s3

            each_row.append(value)

            #input(each_row)
            #each_row = [str(k) for k in each_row]
            each_row = list(map(lambda k : str(k), each_row )) # float list to string list
            fp.write(','.join(each_row)+'\n') # string list to string
                

        s1.close()
        s2.close()
        s3.close()
        s4.close()
        s5.close()

    fp.close()
def make_eu_dataset(dest,path,way,num_row,case,ban,dir):
    fp = open(dest,'w') 

    first_row = '  '
    fp.write(first_row+'\n')

    for idx_move,w in enumerate(way): # for movement
        value = idx_move
        print(f'way = {w}')
        for dire in dir:

            s1 = open(f'{path}/{dire}/{w}/1.csv','r') #f mean sensor
            s2 = open(f'{path}/{dire}/{w}/2.csv','r')
            s3 = open(f'{path}/{dire}/{w}/3.csv','r')
            s4 = open(f'{path}/{dire}/{w}/4.csv','r')
            s5 = open(f'{path}/{dire}/{w}/5.csv','r') 
            
            all_sensor = [s1,s2,s3,s4,s5] 
            e=[[],[],[],[],[]] #for every sensor
            e_backup=[[],[],[],[],[]] 
            q=[[],[],[],[],[]] #for every sensor

            for f in all_sensor: #each sensor
                each_line = f.readline()#first line
                #print(each_line)
            for i in range(num_row):
                each_row = []

                for idx,f in enumerate(all_sensor): #each sensor
                    each_line = f.readline()
                    #print(each_line)
                    #print(f'idx = {idx}')
                    each_list = each_line.strip().split(',')
                    e[idx] = [float(k) for k in each_list[2:]]
                    e_backup[idx]=e[idx]
                    q[idx]= quaternion_from_euler(e[idx])
                    #euler_x,euler_y,_= euler_from_quaternion([1,0,0,0])

                    #v=euler_to_vector(e[idx])
                    each_row.append(e[idx][0])
                    each_row.append(e[idx][1])
                    each_row.append(e[idx][2])
                    '''
                    each_row.append(v[0])
                    each_row.append(v[1])
                    each_row.append(v[2])
                    
                    if idx in ban:
                        e[idx]=[0,0]
                    each_row.append(math.sin(e[idx][0]/180*math.pi))
                    each_row.append(math.cos(e[idx][0]/180*math.pi))
                    each_row.append(math.sin(e[idx][1]/180*math.pi))
                    each_row.append(math.cos(e[idx][1]/180*math.pi))
                    '''

                '''

                if case == 2: 

                    each_row.append(cal_angle(q[0], q[1])) #f1 f2
                    each_row.append(cal_angle(q[1], q[2])) #f2 f3
                if case == 4: 
                    diff01=cal_angle(q[0], q[1])
                    diff12=cal_angle(q[1], q[2])
                    each_row.append(math.sin(diff01)) #s1 s2
                    each_row.append(math.cos(diff01)) #s1 s2
                    each_row.append(math.sin(diff12)) #s2 s3
                    each_row.append(math.sin(diff12)) #s2 s3            
                if case == 5: 
                    diff02=cal_angle(q[0], q[2])
                    each_row.append(diff02) #s1 s3
                if case == 6: 
                    diff02=cal_angle(q[0], q[2])
                    each_row.append(math.sin(diff02)) #s1 s3
                    each_row.append(math.cos(diff02)) #s1 s3
                if case == 7: 
                    diff01=cal_angle(q[0], q[1])
                    each_row.append(diff01) #s1 s3            
                if case == 8: 
                    diff01=cal_angle(q[0], q[1])
                    each_row.append(math.sin(diff01)) #s1 s3
                    each_row.append(math.cos(diff01)) #s1 s3
                '''
                

                # cal z diff
                #print('no z diff')
                #zdiff01=e_backup[0][2]-e_backup[2][2]
                #zdiff12=e_backup[1][2]-e_backup[2][2]
                #print(f' {value}  {zdiff01}')
                #print(zdiff12)
                #each_row.append(zdiff01) #s1 s2
                #each_row.append(zdiff12) #s2 s3
                '''
                each_row.append(math.sin(zdiff01)) #s1 s2
                each_row.append(math.cos(zdiff01)) #s1 s2
                each_row.append(math.sin(zdiff12)) #s2 s3
                each_row.append(math.sin(zdiff12)) #s2 s3  
                '''
                each_row.append(value)

                #input(each_row)
                #each_row = [str(k) for k in each_row]
                each_row = list(map(lambda k : str(k), each_row )) # float list to string list
                #print(len(each_row))
                num_feature = len(each_row)
                fp.write(','.join(each_row)+'\n') # string list to string
                    

            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()

    fp.close()
    return num_feature-1

'''
def init(case):
    if case == 'diff':
        first_row = '1xs,1xc, 1ys, 1yc, 1zs, 1zc, 2xs,2xc, 2ys, 2yc, 2zs, 2zc, 3xs, 3xc, 3ys, 3yc, 4xs, 4xc, 4ys, 4yc, 4zs, 4zc, 5xs, 5xc, 5ys, 5yc, 5zs, 5zc, good_or_bad'
        y_th = 28 #-12 # 12 is sincos
    if case == 1: # good or bad in 20th (21)
        first_row  =  '1_x_sin,1_x_cos,1_y_sin,1_y_cos,2_x_sin,2_x_cos,2_y_sin,2_y_cos,3_x_sin,3_x_cos,3_y_sin,3_y_cos,4_x_sin,4_x_cos,4_y_sin,4_y_cos,5_x_sin,5_x_cos,5_y_sin,5_y_cos,good_or_bad'
        y_th = 20 
        #print('  z diff')
    if case == 2: # good or bad in 22th (23)
        first_row  =  '1_x_sin,1_x_cos,1_y_sin,1_y_cos,2_x_sin,2_x_cos,2_y_sin,2_y_cos,3_x_sin,3_x_cos,3_y_sin,3_y_cos,4_x_sin,4_x_cos,4_y_sin,4_y_cos,5_x_sin,5_x_cos,5_y_sin,5_y_cos,diff_12,\
        diff_23,good_or_bad'
        #difference no use sin cos
        y_th = 22
    if case == 3: # data used before
      y_th  = 10
    if case == 4 : # difference use sin cos
        first_row  =  '1_x_sin,1_x_cos,1_y_sin,1_y_cos,2_x_sin,2_x_cos,2_y_sin,2_y_cos,3_x_sin,3_x_cos,3_y_sin,3_y_cos,4_x_sin,4_x_cos,4_y_sin,4_y_cos,5_x_sin,5_x_cos,5_y_sin,5_y_cos,diff_12_sin,\
        diff_12_cos,diff_23_sin,diff_23_cos,good_or_bad'
        #difference no use sin cos
        y_th = 24
    if case == 5 : # 1 difference no sin cos
        first_row  =  '1_x_sin,1_x_cos,1_y_sin,1_y_cos,2_x_sin,2_x_cos,2_y_sin,2_y_cos,3_x_sin,3_x_cos,3_y_sin,3_y_cos,4_x_sin,4_x_cos,4_y_sin,4_y_cos,5_x_sin,5_x_cos,5_y_sin,5_y_cos,diff_02\
        ,good_or_bad'
        #difference no use sin cos
        y_th = 21
    if case == 6 : # 1 difference use sin cos
        first_row  =  '1_x_sin,1_x_cos,1_y_sin,1_y_cos,2_x_sin,2_x_cos,2_y_sin,2_y_cos,3_x_sin,3_x_cos,3_y_sin,3_y_cos,4_x_sin,4_x_cos,4_y_sin,4_y_cos,5_x_sin,5_x_cos,5_y_sin,5_y_cos,diff_02_sin,\
        diff_02_cos,good_or_bad'
        #difference no use sin cos
        y_th = 22
    
    if case == 7 : # 1 difference no sin cos
        first_row  =  '1_x_sin,1_x_cos,1_y_sin,1_y_cos,2_x_sin,2_x_cos,2_y_sin,2_y_cos,3_x_sin,3_x_cos,3_y_sin,3_y_cos,4_x_sin,4_x_cos,4_y_sin,4_y_cos,5_x_sin,5_x_cos,5_y_sin,5_y_cos,diff[0]\
        ,good_or_bad'
        #difference no use sin cos
        y_th = 21
    if case == 8 : # 1 difference no sin cos
        first_row  =  '1_x_sin,1_x_cos,1_y_sin,1_y_cos,2_x_sin,2_x_cos,2_y_sin,2_y_cos,3_x_sin,3_x_cos,3_y_sin,3_y_cos,4_x_sin,4_x_cos,4_y_sin,4_y_cos,5_x_sin,5_x_cos,5_y_sin,5_y_cos,diff[0]_sin\
        ,diff[0]_cos,good_or_bad'
        #difference no use sin cos
        y_th = 22

    return first_row,y_th
'''
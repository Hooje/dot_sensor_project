import math
import numpy as np


def init(case):
    if case == 1: # good or bad in 20th (21)
        first_row  =  '1_x_sin,1_x_cos,1_y_sin,1_y_cos,2_x_sin,2_x_cos,2_y_sin,2_y_cos,3_x_sin,3_x_cos,3_y_sin,3_y_cos,4_x_sin,4_x_cos,4_y_sin,4_y_cos,5_x_sin,5_x_cos,5_y_sin,5_y_cos,good_or_bad'
        y_th = 20
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
    return first_row,y_th

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
     
        return roll_x/math.pi*180, pitch_y/math.pi*180, yaw_z/math.pi*180 


def quaternion_from_euler(e):
    #Z, Y, X (yaw, pitch, roll),
    roll, pitch, yaw = e[0]*math.pi/180, e[1]*math.pi/180,e[2]*math.pi/180

    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return [qw, qx, qy, qz]
def cal_angle(q1, q2):
   n_q1=normm(q1)
   n_q2=normm(q2)
   angle = math.acos(q1[0]*q2[0] + q1[1]*q2[1] +q1[2]*q2[2] + q1[3]*q2[3])*180/math.pi * 2
   return angle
   #print(f'angle = {math.acos(q1[0]*q2[0] + q1[1]*q2[1] +q1[2]*q2[2] + q1[3]*q2[3])*180/math.pi} * 2 \n')
def normm(qua):
   sum=0
   for i in range(4):
      sum+=qua[i]**2
   sum=sum**0.5
   return sum

    
def make_dataset(dest,path,way,num_row,case):
    fp = open(dest,'w') 

    for idx_move,w in enumerate(way): # for movement
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
def make_eu_dataset(dest,path,way,num_row,case,ban):
    fp = open(dest,'w') 

    for idx_move,w in enumerate(way): # for movement
        value = idx_move

        s1 = open(f'{path}/{w}/1.csv','r') #f mean sensor
        s2 = open(f'{path}/{w}/2.csv','r')
        s3 = open(f'{path}/{w}/3.csv','r')
        s4 = open(f'{path}/{w}/4.csv','r')
        s5 = open(f'{path}/{w}/5.csv','r') 
        
        all_sensor = [s1,s2,s3,s4,s5] 
        e=[[],[],[],[],[]] #for every sensor
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

                q[idx]= quaternion_from_euler(e[idx])
                #euler_x,euler_y,_= euler_from_quaternion([1,0,0,0])

                if idx in ban:
                    e[idx]=[0,0]
                each_row.append(math.sin(e[idx][0]/180*math.pi))
                each_row.append(math.cos(e[idx][0]/180*math.pi))
                each_row.append(math.sin(e[idx][1]/180*math.pi))
                each_row.append(math.cos(e[idx][1]/180*math.pi))

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

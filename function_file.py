import math


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
                each_row.append(cal_angle(q[0], q[1])) #f1 f2
                each_row.append(cal_angle(q[1], q[2])) #f2 f3
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

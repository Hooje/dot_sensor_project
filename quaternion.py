#  ??, use z2  https://www.mathworks.com/matlabcentral/answers/415936-angle-between-2-quaternions
#  better one : use z0  https://math.stackexchange.com/questions/167827/compute-angle-between-quaternions-in-matlab
from pyquaternion import Quaternion
import math 
import quaternion
import numpy as np
def normm(qua):
   sum=0
   for i in range(4):
      sum+=qua[i]**2
   sum=sum**0.5
   return sum

 
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

def qua_to_angle(q1,q2):  #how to from q1 to q2   -->　q1 * z = q2
   n_q1=normm(q1)
   #print(f'norm = {n_q1}')
   n_q2=normm(q2)

   q1=[q1[0]/n_q1, q1[1]/n_q1, q1[2]/n_q1, q1[3]/n_q1] #會變成單位四元數  類似單位向量

   q2=[q2[0]/n_q2, q2[1]/n_q2, q2[2]/n_q2, q2[3]/n_q2]

   x = Quaternion(q1) 

   y = Quaternion(q2)
   #conj_quaternion = my_quaternion.conjugate
   zc = x.conjugate *y
   print(type(q1))
   a=q1[0]; b=-q1[1]; c=-q1[2]; d=-q1[3]
   e=q2[0]; f=q2[1]; g=q2[2]; h=q2[3]
   z = [(a*e - b*f -c* g- d*h), (b*e + a*f + c*h- d*g) , (a*g - b*h+ c*e + d*f) , (a*h + b*g - c*f + d*e)]
   print(zc)
   print(z)
   #print(x)
   #print(y)
   print(f'q1 = {q1}')
   print(f'q2 = {q2}')
   print(q1*zc) #this is correct    
   print(q2*zc)
   input()
   #print(z)
   #print(x*z)
   angle0 = ( math.acos(z[0]) * 2 )*180/math.pi # this is correct
   angle3 = ( math.acos(z[3]) * 2 )*180/math.pi
   print(angle0, angle3)
   #print('euler')
   a,b,c=euler_from_quaternion(x)
   print(a,b,c)
   a,b,c=euler_from_quaternion(y)
   print(a,b,c)
   a,b,c=euler_from_quaternion(z)
   print(a,b,c)
   print()
def cal_angle(q1, q2):
   n_q1=normm(q1)
   #print(f'norm = {n_q1}')
   n_q2=normm(q2)
   print(f'angle = {math.acos(q1[0]*q2[0] + q1[1]*q2[1] +q1[2]*q2[2] + q1[3]*q2[3])*180/math.pi} * 2 \n')


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

q1 = [0.9897052,   0.021346753, -0.14117369, -0.009901799 ]#2.755847931 -16.25458527   -1.596380353
q2 = [1,0,0,0]

print(qua_diff(q2, q1))

input()
qua_to_angle(q1,q2)
cal_angle(q1,q2)


exit(0)
q1 = [0.9897052,   0.021346753, -0.14117369, -0.009901799 ]#2.755847931 -16.25458527   -1.596380353
q2 = [0.29726613,  -0.002300085,   -0.007810124,   -0.95475996]
qua_to_angle(q1,q2)
cal_angle(q1,q2)

q1 = [0.98415405,  -0.010155259,   -0.002827282,   0.17700246 ]
q2 = [0.30383646,  -0.002709363,   -0.008969343,   -0.95267814]
qua_to_angle(q1,q2)
cal_angle(q1,q2)


q1 = [0.89920574,  0.052675977, -0.31929377, 0.29445887]
q2 = [0.23364507,  0.6522624,   -0.60282236, 0.39568815]
qua_to_angle(q1,q2)
cal_angle(q1,q2)
q1 = [0.6286867,   -0.7020504,  -0.20587273, 0.26361862]
q2 = [0.009228709, 0.066409506, 0.6392755,   -0.76604927]
qua_to_angle(q1,q2)
cal_angle(q1,q2)


q1 = [0.31628433,  -0.8413104,  0.41368985,  -0.14498934]
q2 = [0.27828878,  -0.6635542,  -0.19023666, 0.66787815]
qua_to_angle(q1,q2)
cal_angle(q1,q2)

q1 = [0.31020337,  -0.004680461,   -0.003569651,   -0.95065206]
q2 = [0.010360244, 0.005515528, -0.003372066,   -0.99992555]
qua_to_angle(q1,q2)
cal_angle(q1,q2)


q1 = [0.23891003,  -0.004226953,   -0.00561559, -0.9710162]
q2 = [0.49962693,  0.5043285,   -0.48798952, 0.50783056]
qua_to_angle(q1,q2)
cal_angle(q1,q2)

q1 = [0.98415405,  -0.010155259,   -0.002827282,   0.17700246]
q2 = [0.30383646,  -0.002709363,   -0.008969343,   -0.95267814]
qua_to_angle(q1,q2)
cal_angle(q1,q2)

q1 = [0.9897052,   0.021346753, -0.14117369, -0.009901799]
a,b,c=euler_from_quaternion(q1)
print(a,b,c)
q1 = [0.99736637,  -0.017296363,   0.006053309 -0.07017637]
a,b,c=euler_from_quaternion(q1)
print(a,b,c)
print('flag\n')
q1 = [1,   0, 0,  0]
q2 = [0.9897052,   0.021346753, -0.14117369, -0.009901799]
qua_to_angle(q2,q1)
#cal_angle(q1,q2)
a,b,c=euler_from_quaternion(q1)

q1 = [1,   0, 0,  0]
q2 = [0.050670847, 0.27909154,  -0.33062238, -0.9001291]
qua_to_angle(q2,q1)
#cal_angle(q1,q2)
a,b,c=euler_from_quaternion(q1)
#print(a,b,c)
'''
44.95615387 28.03258133 -161.6861267
0.050670847 0.27909154  -0.33062238 -0.9001291


0.99736637  -0.017296363   0.006053309 -0.07017637
0 0 0

2.755847931 -16.25458527   -1.596380353
0.9897052   0.021346753 -0.14117369 -0.009901799

-1.620144129   23.96466064 -74.95474243
0.7798492   0.114778854 0.17329745  -0.5904483

0.31020337  -0.004680461   -0.003569651   -0.95065206 #wxyz   90
0.010360244 0.005515528 -0.003372066   -0.99992555

0.210725725 -0.715083957   -143.7671509
0.533635378 0.706764102 -178.4464874

0.23891003  -0.004226953   -0.00561559 -0.9710162   90
0.49962693  0.5043285   -0.48798952 0.50783056
0.482389361 -0.599134862   -152.2201843
27.08872604 -88.85431671   64.79935455



0.28875265  -0.003871514   -0.003870664   -0.9573881    0
0.29726613  -0.002300085   -0.007810124   -0.95475996


0.98415405  -0.010155259   -0.002827282   0.17700246   180
0.30383646  -0.002709363   -0.008969343   -0.95267814

0.89920574  0.052675977 -0.31929377 0.29445887   90
0.23364507  0.6522624   -0.60282236 0.39568815

0.6286867   -0.7020504  -0.20587273 0.26361862   90
0.009228709 0.066409506 0.6392755   -0.76604927

0.31628433  -0.8413104  0.41368985  -0.14498934   90
0.27828878  -0.6635542  -0.19023666 0.66787815


#q1=[ 0.968, 0.008, -0.008, 0.252]
#q2=[ 0.382, 0.605,  0.413, 0.563]
q1=[ -0.004680461,   -0.003569651,   -0.95065206,   0.31020337]
q2=[ 0.005515528, -0.003372066,   -0.99992555,  0.010360244]

x, y, z=euler_from_quaternion(q1[0], q1[1], q1[2], q1[3])
x2, y2, z2=euler_from_quaternion(q2[0], q2[1], q2[2], q2[3])

print(x,y,z) #150 1.12 0.66
print(x2,y2,z2) #5.73 21.45 94.51
#150 1.12 0.66#5.73 21.45 94.51



n_q1=normm(q1)
#print(f'norm = {n_q1}')
n_q2=normm(q2)

q1=[q1[0]/n_q1, q1[1]/n_q1, q1[2]/n_q1, q1[3]/n_q1] #會變成單位四元數  類似單位向量

q2=[q2[0]/n_q2, q2[1]/n_q2, q2[2]/n_q2, q2[3]/n_q2]

x = Quaternion(q1) 

y = Quaternion(q2)



#conj_quaternion = my_quaternion.conjugate
z = x.conjugate * y

print(x)
print(y)
print(z)

print(z[0])
angle = ( math.acos(z[3]) * 2 )*180/math.pi

print(angle) # should be 127



q1=[0.31020337,  -0.004680461,   -0.003569651,   -0.95065206]
q2=[0.010360244, 0.005515528, -0.003372066,   -0.99992555]

x, y, z=euler_from_quaternion(q1[0], q1[1], q1[2], q1[3])
x2, y2, z2=euler_from_quaternion(q2[0], q2[1], q2[2], q2[3])
print(f'{x}    {y}    {z}')
print(f'{x2}    {y2}    {z2}')

x = Quaternion(q1) 

y = Quaternion(q2)



#conj_quaternion = my_quaternion.conjugate
z = x.conjugate * y
angle = ( math.acos(z[0]) * 2 )*180/math.pi

print(angle) # should be 127


q1=[0.23891003,  -0.004226953,   -0.00561559, -0.9710162]
q2=[0.49962693,  0.5043285,   -0.48798952, 0.50783056]
x, y, z=euler_from_quaternion(q1[0], q1[1], q1[2], q1[3])
x2, y2, z2=euler_from_quaternion(q2[0], q2[1], q2[2], q2[3])
print(f'{x}    {y}    {z}')
print(f'{x2}    {y2}    {z2}')

x = Quaternion(q1) 

y = Quaternion(q2)



#conj_quaternion = my_quaternion.conjugate
z = x.conjugate * y
angle = ( math.acos(z[0]) * 2 )*180/math.pi

print(angle) # should be 127
'''


'''

0.31020337  -0.004680461   -0.003569651   -0.95065206 #wxyz   90
0.010360244 0.005515528 -0.003372066   -0.99992555

0.210725725 -0.715083957   -143.7671509
0.533635378 0.706764102 -178.4464874



0.23891003  -0.004226953   -0.00561559 -0.9710162   90
0.49962693  0.5043285   -0.48798952 0.50783056
0.482389361 -0.599134862   -152.2201843
27.08872604 -88.85431671   64.79935455



0.28875265  -0.003871514   -0.003870664   -0.9573881    0
0.29726613  -0.002300085   -0.007810124   -0.95475996


0.98415405  -0.010155259   -0.002827282   0.17700246   180
0.30383646  -0.002709363   -0.008969343   -0.95267814


0.89920574  0.052675977 -0.31929377 0.29445887   90
0.23364507  0.6522624   -0.60282236 0.39568815

0.6286867   -0.7020504  -0.20587273 0.26361862   90
0.009228709 0.066409506 0.6392755   -0.76604927

0.31628433  -0.8413104  0.41368985  -0.14498934   90
0.27828878  -0.6635542  -0.19023666 0.66787815

'''
import numpy as np
from function_file import *
from numpy import ravel
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

way = [0,1,2,3,4]#,5,6]
num_row = 2
case = 2 # case = 2 mean add difference between three sensor
number = 10


if case == 1: # good or bad in 20th (21)
    first_row  =  '1_x_sin,1_x_cos,1_y_sin,1_y_cos,2_x_sin,2_x_cos,2_y_sin,2_y_cos,3_x_sin,3_x_cos,3_y_sin,3_y_cos,4_x_sin,4_x_cos,4_y_sin,4_y_cos,5_x_sin,5_x_cos,5_y_sin,5_y_cos,good_or_bad'
    y_th = 20
if case == 2: # good or bad in 22th (23)
    first_row  =  '1_x_sin,1_x_cos,1_y_sin,1_y_cos,2_x_sin,2_x_cos,2_y_sin,2_y_cos,3_x_sin,3_x_cos,3_y_sin,3_y_cos,4_x_sin,4_x_cos,4_y_sin,4_y_cos,5_x_sin,5_x_cos,5_y_sin,5_y_cos,diff_12,diff_23,good_or_bad'
    #difference no use sin cos
    y_th = 22



if __name__ == '__main__':        
    rfc=RandomForestClassifier()
    #path = '../0808/me_q'
    make_dataset('test_create','../0808/me_q',way,num_row,case)
    make_dataset('test2_create','../0808/room_q',way,num_row,case)

    fp = open('test_create','r') 

    data = np.loadtxt(fp, delimiter=',')
    X = data[:, :y_th-1]  # select columns 1 through end
    y = data[:, y_th]   # select column 0

    fp2 = open('test2_create','r') 
    data2 = np.loadtxt(fp2,delimiter=',')

    # if want to select sensor , can use ....  in notion python technique
    X2 = data2[:, :y_th-1]  # select columns 1 through end
    y2 = data2[:, y_th]   # select column 0

    #print(X)
    #print('\n\n\n\n\n')
    #print(X2)
    #input(type(X))
    #validation_score=0
    test_score=0

    all_matrix=[[0]*len(way) for i in range(len(way))]
    for i in range(number):
        rfc.fit(X, y)
        #validation_score+=rfc.score(x_test, y_test)  
        test_score+=rfc.score(X2, y2)

        y_prime = rfc.predict(X2)

        array=confusion_matrix(y_prime,y2)

        all_matrix+=array
    print(test_score/number)
    print(all_matrix)

    #fp = open('test_create.csv','w') 
    #fp.write(first_row+'\n')
    fp.close()
    fp2.close()


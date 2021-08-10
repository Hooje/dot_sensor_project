import numpy as np
from function_file import *
from numpy import ravel
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
way=["0","1","2","3","4"]#,"5","6"]#,"7","8","9","10"]#,"11","12","13","14","15","16","17","18","19","20"]
#way = [0,1,2,3,4]#,5,6]
num_row = 100
case = 2 # case = 2 mean add difference between three sensor, case 3 mean before used, case 4 mean 2 difference sin and cos, case 5 mean 1 difference, 6 mean 1 difference sin cos
number = 5
ban = [0,1,2,3,4] #ignore which sensor，0 mean sensor 1,  i mean sensor i+1



if __name__ == '__main__':      

    first_row,y_th = init(case)
    rfc=RandomForestClassifier()
    path = '../0808/me_q'
    path2 = '../0808/room_q'
    #path = '../stand_train'
    #path2 = '../stand_test'
    make_eu_dataset('test_create',path,way,num_row,case,ban)
    make_eu_dataset('test2_create',path2,way,num_row,case,ban)
    #input(first_row)
    fp = open('test_create','r') 

    data = np.loadtxt(fp, delimiter=',',skiprows=1)
    X = data[:, :y_th-1]  # select columns 1 through end
    y = data[:, y_th]   # select column 0

    fp2 = open('test2_create','r') 
    data2 = np.loadtxt(fp2,delimiter=',',skiprows=1)

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


# 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 #
import numpy as np
from function_file import *
from numpy import ravel
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

from sklearn.tree import export_graphviz
import pydot# Pull out one tree from the forest

way=["0","7","8","9","10","11","13","15","17"]  # 9 way
#way = ["0","1","2"]#,"3","4"]
#way=["1","2","3","4","7","8","9","10","11","12","13","14","15","16","17","18"]
way_test=["0","1","2","3","4","5","6","7"]
#way_test=["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]#,"19","20"]
#way=["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]#,"19","20"]
# 0 6 8 14 16 17 18
#way = ['5','6']
#way=["0","1","2","3","4","5","6"]
#way=["0","7","8","9","10","11","12","13","14","15","16","17","18"]

num_row = 1
#case = 'dcm'
case = 'mine'
#case = 'vector'
#case = 'angle'
#case = 'diff' 
# case = 2 mean add difference between three sensor, case 3 mean before used, case 4 mean 2 difference sin and cos,\
# case 5 mean 1 difference, 6 mean 1 difference sin cos, 7 mean 1 and two diff, 8 use sin and cos 
ban = [] #ignore which sensor，0 mean sensor 1,  i mean sensor i+1
set_zero = 1
use_sin_cos = 0
dir_name = '0818'
#dir_t_name = '0818'
dir_t_name = '0911'
path = f'../{dir_name}' # 0818 is three person   0824 is turn sesnro 90 degree
path2 = f'../{dir_t_name}'
#train_dir = ['me','yuchi','room'] # room is useless
train_dir = ['me','yuchi','ichen'] # room is useless
#train_dir = ['me']#,'me2']
#test_dir = ['ichen']
test_dir = ['test_set']
use_abs = 1
add_diff = 0
number = 20
m_depth = 1
good_set = [0]
good_set_t= [0,1]#,2]#,3]#,4]
collect_tree = 1

#for diff  -------------------------------------------------------------------
use_transfer = 0 #mean transfer large euler x, 

# angle : 0 mean not zero, 1 mean use zero
# diff :  1 mean only zero, no difference, 2 mean no zero only sensor diff, 3 mean no difference no zero just like case 1


#path = '../0808/me_q'
#path2 = '../0808/room_q'


#path = '../0728train'
#path2 = '../0728test'
#------------------------------------- for my classfier

threshold = 10

test_mine = 8 # 18 or 8
if test_mine == 18:
    m_path = path
    m_way = way
    m_dir = train_dir
    m_good_set = good_set
else:
    m_path = path2
    m_way = way_test
    m_dir = ['test_set']
    m_good_set = good_set_t

#-------------------------------------
if __name__ == '__main__':      
    #first_row,y_th = init(case)
    rfc=RandomForestClassifier(max_depth=m_depth)
    #print(f'set_zero : {set_zero}')
    print(f'ban : {ban}')
    #print('use ori sensor 3')
                
    
    #path = '../stand_train'
    #path2 = '../stand_test'
    if case == 'mine':

        my_dcm_classfier(m_path,m_way,m_dir,  m_good_set,threshold)
        #my_classfier(m_path,m_way,m_dir,  m_good_set,threshold)
        exit()
    elif case == 'angle':
        _=make_angle_dataset('test_create',path,way,num_row,ban,train_dir,use_sin_cos, set_zero, use_abs, add_diff, good_set)
        y_th=make_angle_dataset('test2_create',path2,way_test,num_row,ban,test_dir,use_sin_cos, set_zero,use_abs, add_diff, good_set_t)
        print(y_th)
    elif case == 'diff':
        print(f'diff set_zero: {set_zero}')
        _=make_difference_dataset('test_create',path,way,num_row,ban,train_dir,set_zero, use_transfer)
        y_th=make_difference_dataset('test2_create',path2,way,num_row,ban,test_dir,set_zero, use_transfer)
        print(y_th)    
    elif case == 'dcm':
        print(f'dcm set_zero: {set_zero}')
        _=make_dcm_dataset('test_create',path,way,num_row,ban,train_dir,set_zero, good_set)
        #y_th=make_dcm_dataset('test2_create',path2,way_test,num_row,ban,test_dir,set_zero, good_set)
        y_th=make_dcm_dataset('test2_create',path2,way_test,num_row,ban,test_dir,set_zero, good_set)
        print(y_th)
    else : 
        print('eu_use_vector')
        _=make_eu_dataset('test_create',path,way,num_row,case,ban,train_dir)
        y_th=make_eu_dataset('test2_create',path2,way,num_row,case,ban,test_dir)
        print(f'y_th = {y_th}')
    #input(first_row)

    print(y_th)
    fp = open('test_create','r') 

    data = np.loadtxt(fp, delimiter=',',skiprows=1)
    X = data[:, :y_th]  # select columns 1 through end
    y = data[:, y_th]   # select column 0

    fp2 = open('test2_create','r') 
    data2 = np.loadtxt(fp2,delimiter=',',skiprows=1)

    # if want to select sensor , can use ....  in notion python technique
    X2 = data2[:, :y_th]  # select columns 1 through end
    y2 = data2[:, y_th]   # select column 0

    #print(X)
    #print(y)
    #print('\n\n\n\n\n')
    #print(X2)
    #input(type(X))
    #validation_score=0
    test_score=0


    #feature_num =   len(way) if case != 'angle' else 2
    feature_num = 2    
    all_matrix=[[0]*feature_num for i in range(feature_num)]
    for i in range(number):
        rfc.fit(X, y)
        #validation_score+=rfc.score(x_test, y_test)  
        test_score+=rfc.score(X2, y2)

        y_prime = rfc.predict(X2)

        array=confusion_matrix(y_prime,y2)
        #print(array.shape)
        #input()
        all_matrix+=array
    print(test_score/number)
    print(all_matrix)

    #fp = open('test_create.csv','w') 


    if collect_tree == 1: 
        list_three = []
        num_decisiontree = 3
        for idx_tree,tree in enumerate(rfc.estimators_):

            all_matrix=[[0]*feature_num for i in range(feature_num)]
            test_score=0
            for i in range(number):
                #x_train, x_test, y_train, y_test=train_test_split(x,y, test_size=0.9, random_state=random.randint(1, 50))
                tree.fit(X, y)

                test_score+= tree.score(X2, y2)

                y_prime = tree.predict(X2)

                array=confusion_matrix(y_prime,y2)        
                all_matrix+=array

            #print(idx_tree,test_score/number)
            list_three = find_three(idx_tree, test_score/number, all_matrix,num_decisiontree, list_three)

        #tree_name='tree_dot'
        #視覺化
        for i in range(num_decisiontree):        
            print(f' number {i} score and array is = {list_three[i][1]}\n{list_three[i][2]}')
            tree_name=(f'graph/{i}')

            #feature_list = ['sensor_12', 'sensor_13', 'sensor_23']
            #feature_list = ['sensor_13', 'sensor_23'] # ban 0
            #feature_list = ['sensor_1_angle1', 'sensor_1_angle2', 'sensor_1_angle3','sensor_2_angle1', 'sensor_2_angle2', 'sensor_2_angle3','sensor_3_angle1', 'sensor_3_angle2', 'sensor_3_angle3','sensor_4_angle1', 'sensor_4_angle2', 'sensor_4_angle3','sensor_5_angle1', 'sensor_5_angle2', 'sensor_5_angle3'] # ban 2
            feature_list = ['angle_12x','angle_12y','angle_12z','angle_13x','angle_13y','angle_13z']
            #feature_list = ['angle_12x','angle_13x']
            export_graphviz(rfc.estimators_[list_three[i][0]], out_file = tree_name, feature_names = feature_list , rounded = True)#, precision = 1)# Use dot file to create a graph
            (graph, ) = pydot.graph_from_dot_file(tree_name)# Write graph to a png file
            tree_name+='.png'
            graph.write_png(tree_name)


    fp.close()
    fp2.close()
    
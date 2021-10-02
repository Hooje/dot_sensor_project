from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
#from sklearn import joblib 
from sklearn.metrics import confusion_matrix
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from numpy import ravel
import random
import math
from sklearn import cluster, manifold #manifold is for t-sne
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import copy 
#data_number=200
path="3D_train.csv"
test_path="3D_test.csv"
number=50
num_fea=21
m_depth= 5
use_diff=2 #2 mean combine
collect_tree = 0 #1 means to get the photo of tree 
num_decisiontree = 5 #取前幾名的樹
ignore_z = 0 #ignore 1 means  no combine feature,  ignore 2 mean  1 3 difference


list_three = []

x_1_sin=[]
y_1_sin=[]
x_2_sin=[]
y_2_sin=[]
x_3_sin=[]
y_3_sin=[]
x_4_sin=[]
y_4_sin=[]
x_5_sin=[]
y_5_sin=[]
x_1_cos=[]
y_1_cos=[]
x_2_cos=[]
y_2_cos=[]
x_3_cos=[]
y_3_cos=[]
x_4_cos=[]
y_4_cos=[]
x_5_cos=[]
y_5_cos=[]
add_x_1_sin=[]
add_y_1_sin=[]
add_x_2_sin=[]
add_y_2_sin=[]
add_x_3_sin=[]
add_y_3_sin=[]
add_x_4_sin=[]
add_y_4_sin=[]
add_x_5_sin=[]
add_y_5_sin=[]
add_x_1_cos=[]
add_y_1_cos=[]
add_x_2_cos=[]
add_y_2_cos=[]
add_x_3_cos=[]
add_y_3_cos=[]
add_x_4_cos=[]
add_y_4_cos=[]
add_x_5_cos=[]
add_y_5_cos=[]

x_list=[ 
x_1_sin, y_1_sin,
x_2_sin, y_2_sin,  
x_3_sin, y_3_sin,
x_4_sin, y_4_sin, 
x_5_sin, y_5_sin,
x_1_cos, y_1_cos, 
x_2_cos, y_2_cos,
x_3_cos, y_3_cos, 
x_4_cos, y_4_cos,
x_5_cos, y_5_cos,]

x_add_list=[
add_x_1_sin, add_y_1_sin,
add_x_2_sin, add_y_2_sin, 
add_x_3_sin, add_y_3_sin,
add_x_4_sin, add_y_4_sin, 
add_x_5_sin, add_y_5_sin,
add_x_1_cos, add_y_1_cos, 
add_x_2_cos, add_y_2_cos,
add_x_3_cos, add_y_3_cos, 
add_x_4_cos, add_y_4_cos,
add_x_5_cos, add_y_5_cos]
'''
feature_list = [["1_x_sin","1_y_sin","1_z_sin","2_x_sin","2_y_sin","2_z_sin","3_x_sin","3_y_sin","3_z_sin","4_x_sin","4_y_sin","4_z_sin","5_x_sin","5_y_sin","5_z_sin"\
               ,"1_x_cos","1_y_cos","1_z_cos","2_x_cos","2_y_cos","2_z_cos","3_x_cos","3_y_cos","3_z_cos","4_x_cos","4_y_cos","4_z_cos","5_x_cos","5_y_cos","5_z_cos"],
               ["1_x_sin","1_y_sin","1_z_sin","2_x_sin","2_y_sin","2_z_sin","3_x_sin","3_y_sin","3_z_sin","4_x_sin","4_y_sin","4_z_sin","5_x_sin","5_y_sin","5_z_sin"\
               ,"1_x_cos","1_y_cos","1_z_cos","2_x_cos","2_y_cos","2_z_cos","3_x_cos","3_y_cos","3_z_cos","4_x_cos","4_y_cos","4_z_cos","5_x_cos","5_y_cos","5_z_cos",\
               "add_1_x_sin","add_1_y_sin","add_1_z_sin","add_2_x_sin","add_2_y_sin","add_2_z_sin","add_3_x_sin","add_3_y_sin","add_3_z_sin","add_4_x_sin","add_4_y_sin","add_4_z_sin","add_5_x_sin","add_5_y_sin","add_5_z_sin"\
               ,"add_1_x_cos","add_1_y_cos","add_1_z_cos","add_2_x_cos","add_2_y_cos","add_2_z_cos","add_3_x_cos","add_3_y_cos","add_3_z_cos","add_4_x_cos","add_4_y_cos","add_4_z_cos","add_5_x_cos","add_5_y_cos","add_5_z_cos"]]
               '''
feature_list = [["1_x_sin","1_y_sin","2_x_sin","2_y_sin","3_x_sin","3_y_sin","4_x_sin","4_y_sin","5_x_sin","5_y_sin"\
               ,"1_x_cos","1_y_cos","2_x_cos","2_y_cos","3_x_cos","3_y_cos","4_x_cos","4_y_cos","5_x_cos","5_y_cos"],
               ["1_x_sin","1_y_sin","2_x_sin","2_y_sin","3_x_sin","3_y_sin","4_x_sin","4_y_sin","5_x_sin","5_y_sin"\
               ,"1_x_cos","1_y_cos","2_x_cos","2_y_cos","3_x_cos","3_y_cos","4_x_cos","4_y_cos","5_x_cos","5_y_cos",\
               "add_1_x_sin","add_1_y_sin","add_2_x_sin","add_2_y_sin","add_3_x_sin","add_3_y_sin","add_4_x_sin","add_4_y_sin","add_5_x_sin","add_5_y_sin"\
               ,"add_1_x_cos","add_1_y_cos","add_2_x_cos","add_2_y_cos","add_3_x_cos","add_3_y_cos","add_4_x_cos","add_4_y_cos","add_5_x_cos","add_5_y_cos"]]

def init():
    for i in range(20):
        x_list[i]=[]
        x_add_list[i]=[]

def find_three(index, score, all_matrix, list_three):
    global list_three
    list_three.append((index,score, all_matrix))
    list_three = sorted(list_three, reverse = True, key = lambda s: s[1])
    while len(list_three) > num_decisiontree :
        list_three.pop()

def origin_train():
    input("origin0\n?")
    file=pd.read_csv(path)
    rfc=RandomForestClassifier()
    #x=file[["1_x","1_y","1_z","2_x","2_y","2_z","3_x","3_y","3_z","4_x","4_y","4_z","5_x","5_y","5_z"]]
    x=file[["1_x","1_y","2_x","2_y","3_x","3_y","4_x","4_y","5_x","5_y"]]
    y=file[["good_or_bad"]]
    file_t=pd.read_csv(test_path)
    #x_t=file_t[["1_x","1_y","1_z","2_x","2_y","2_z","3_x","3_y","3_z","4_x","4_y","4_z","5_x","5_y","5_z"]]
    x_t=file_t[["1_x","1_y","2_x","2_y","3_x","3_y","4_x","4_y","5_x","5_y"]]
    y_t=file_t[["good_or_bad"]]
    y_t=ravel(y_t)
    y=ravel(y)
    validation_score=0
    test_score=0

    all_matrix_o=[[0]*num_fea for i in range(num_fea)]


    for i in range(number):

        x_train, x_test, y_train, y_test=train_test_split(x,y, test_size=0.7, random_state=random.randint(1, 50))
        rfc.fit(x_train, y_train)


        validation_score+=rfc.score(x_test, y_test)  

        test_score+=rfc.score(x_t, y_t)

        y_prime = rfc.predict(x_t)

        array=confusion_matrix(y_prime,y_t)

        all_matrix_o+=array

    print(all_matrix_o)

    print("score validation", validation_score/number)
    print("score test ",test_score/number)  
    #print("good or bad", cnt/len(y_t))


def sin_cos():
    input('sin_cos?')
    file=pd.read_csv(path)
    rfc=RandomForestClassifier(max_depth=m_depth)
    #x_pre=file[["1_x","1_y","1_z","2_x","2_y","2_z","3_x","3_y","3_z","4_x","4_y","4_z","5_x","5_y","5_z"]]
    x_pre=file[["1_x","1_y","2_x","2_y","3_x","3_y","4_x","4_y","5_x","5_y"]]
    if use_diff == 1:
        x_diff=x_pre  #會同時改兩個，後面要用 deepcopy
        x_diff["1_x"]=x_pre["1_x"]-x_pre["2_x"]
        x_diff["1_y"]=x_pre["1_y"]-x_pre["2_y"]
       # x_diff["1_z"]=x_pre["1_z"]-x_pre["2_z"]

        x_diff["2_x"]=x_pre["2_x"]-x_pre["3_x"]
        x_diff["2_y"]=x_pre["2_y"]-x_pre["3_y"]
        #x_diff["2_z"]=x_pre["2_z"]-x_pre["3_z"]

        x_diff["4_x"]=x_pre["3_x"]-x_pre["4_x"]  #new four is difference between three and four
        x_diff["4_y"]=x_pre["3_y"]-x_pre["4_y"]
        #x_diff["4_z"]=x_pre["3_z"]-x_pre["4_z"]

        x_diff["5_x"]=x_pre["4_x"]-x_pre["5_x"] 
        x_diff["5_y"]=x_pre["4_y"]-x_pre["5_y"]
        #x_diff["5_z"]=x_pre["4_z"]-x_pre["5_z"]

    if use_diff ==2 : #combine
        #print(f'x_pre = {x_pre}')
        x_diff=copy.deepcopy(x_pre)
        #print(f'x_pre = {x_pre}')
        x_diff["1_x"]=x_pre["1_x"]-x_pre["2_x"]
        x_diff["1_y"]=x_pre["1_y"]-x_pre["2_y"]
        #x_diff["1_z"]=x_pre["1_z"]-x_pre["2_z"]

        x_diff["2_x"]=x_pre["2_x"]-x_pre["3_x"]
        x_diff["2_y"]=x_pre["2_y"]-x_pre["3_y"]
        #x_diff["2_z"]=x_pre["2_z"]-x_pre["3_z"]

        x_diff["4_x"]=x_pre["3_x"]-x_pre["4_x"]  #new four is difference between three and four
        x_diff["4_y"]=x_pre["3_y"]-x_pre["4_y"]
        #x_diff["4_z"]=x_pre["3_z"]-x_pre["4_z"]

        x_diff["5_x"]=x_pre["4_x"]-x_pre["5_x"] 
        x_diff["5_y"]=x_pre["4_y"]-x_pre["5_y"]
        #x_diff["5_z"]=x_pre["4_z"]-x_pre["5_z"]
        #print(f'x_pre = {x_pre}')
        #input()

    #print(type(x_pre))
    #input()
    y=file[["good_or_bad"]]
    y=ravel(y)

    for i,colume in enumerate(x_pre):
        #print(colume)
        for num in x_pre[colume]:

            tmp_sin=math.sin(num/180*math.pi)
            tmp_cos=math.cos(num/180*math.pi)
            if ignore_z != 0:
                if ('2' in colume) or  ('4' in colume) or ('5' in colume) :
                    #print("")
                    tmp_sin=0 
                    tmp_cos=0
            x_list[i].append(tmp_sin)
            x_list[i+10].append(tmp_cos)
    if use_diff == 2 :
        
        for i,colume in enumerate(x_diff):
            #print(colume)    
            for num in x_diff[colume]:   
                tmp_sin=math.sin(num/180*math.pi)
                tmp_cos=math.cos(num/180*math.pi)
                if ignore_z == 1:
                    if ('1' in colume) or ('2' in colume) or ('3' in colume) or  ('4' in colume) or ('5' in colume) :
                        #print("yes")
                        tmp_sin=0 
                        tmp_cos=0                
                if ignore_z == 2:
                    if ('2' in colume) or  ('4' in colume) or ('5' in colume) :
                        #print("yes")
                        tmp_sin=0 
                        tmp_cos=0


                x_add_list[i].append(tmp_sin)
                x_add_list[i+10].append(tmp_cos)
        

        x_dict={
            "1_x_sin": x_list[0], "1_y_sin": x_list[1], #"1_z_sin": x_list[2],
            "2_x_sin": x_list[2], "2_y_sin": x_list[3], #"2_z_sin": x_list[5], 
            "3_x_sin": x_list[4], "3_y_sin": x_list[5], #"3_z_sin": x_list[8],
            "4_x_sin": x_list[6], "4_y_sin": x_list[7],#"4_z_sin": x_list[11], 
            "5_x_sin": x_list[8], "5_y_sin": x_list[9], #"5_z_sin": x_list[14],
            "1_x_cos": x_list[10], "1_y_cos": x_list[11], #"1_z_cos": x_list[17], 
            "2_x_cos": x_list[12], "2_y_cos": x_list[13], #"2_z_cos": x_list[20],
            "3_x_cos": x_list[14], "3_y_cos": x_list[15], #"3_z_cos": x_list[23], 
            "4_x_cos": x_list[16], "4_y_cos": x_list[17], #"4_z_cos": x_list[26],
            "5_x_cos": x_list[18], "5_y_cos": x_list[19], #"5_z_cos": x_list[29],

            "add_1_x_sin": x_add_list[0], "add_1_y_sin": x_add_list[1], #"add_1_z_sin": x_add_list[2],
            "add_2_x_sin": x_add_list[2], "add_2_y_sin": x_add_list[3], #"add_2_z_sin": x_add_list[5], 
            "add_3_x_sin": x_add_list[4], "add_3_y_sin": x_add_list[5], #"add_3_z_sin": x_add_list[8],
            "add_4_x_sin": x_add_list[6], "add_4_y_sin": x_add_list[7],#"add_4_z_sin": x_add_list[11], 
            "add_5_x_sin": x_add_list[8], "add_5_y_sin": x_add_list[9], #"add_5_z_sin": x_add_list[14],
            "add_1_x_cos": x_add_list[10], "add_1_y_cos": x_add_list[11], #"add_1_z_cos": x_add_list[17], 
            "add_2_x_cos": x_add_list[12], "add_2_y_cos": x_add_list[13], #"add_2_z_cos": x_add_list[20],
            "add_3_x_cos": x_add_list[14], "add_3_y_cos": x_add_list[15], #"add_3_z_cos": x_add_list[23], 
            "add_4_x_cos": x_add_list[16], "add_4_y_cos": x_add_list[17], #"add_4_z_cos": x_add_list[26],
            "add_5_x_cos": x_add_list[18], "add_5_y_cos": x_add_list[19], #"add_5_z_cos": x_add_list[29],


        }
    else :
        x_dict={
            "1_x_sin": x_list[0], "1_y_sin": x_list[1], #"1_z_sin": x_list[2],
            "2_x_sin": x_list[2], "2_y_sin": x_list[3], #"2_z_sin": x_list[5], 
            "3_x_sin": x_list[4], "3_y_sin": x_list[5], #"3_z_sin": x_list[8],
            "4_x_sin": x_list[6], "4_y_sin": x_list[7],#"4_z_sin": x_list[11], 
            "5_x_sin": x_list[8], "5_y_sin": x_list[9], #"5_z_sin": x_list[14],
            "1_x_cos": x_list[10], "1_y_cos": x_list[11], #"1_z_cos": x_list[17], 
            "2_x_cos": x_list[12], "2_y_cos": x_list[13], #"2_z_cos": x_list[20],
            "3_x_cos": x_list[14], "3_y_cos": x_list[15], #"3_z_cos": x_list[23], 
            "4_x_cos": x_list[16], "4_y_cos": x_list[17], #"4_z_cos": x_list[26],
            "5_x_cos": x_list[18], "5_y_cos": x_list[19], #"5_z_cos": x_list[29]


        }

    x=pd.DataFrame(x_dict)

    input(f'usediff = {use_diff}  \n{x}\ncontinue?')
    print(x["add_3_x_cos"])
    init()

    file_t=pd.read_csv(test_path)
    #x_t_p=file_t[["1_x","1_y","1_z","2_x","2_y","2_z","3_x","3_y","3_z","4_x","4_y","4_z","5_x","5_y","5_z"]]
    x_t_p=file_t[["1_x","1_y","2_x","2_y","3_x","3_y","4_x","4_y","5_x","5_y"]]
    y_t=file_t[["good_or_bad"]]
    y_t=ravel(y_t)    
    if use_diff == 1:
        x_diff=x_t_p
        x_diff["1_x"]=x_t_p["1_x"]-x_t_p["2_x"]
        x_diff["1_y"]=x_t_p["1_y"]-x_t_p["2_y"]
        #x_diff["1_z"]=x_t_p["1_z"]-x_t_p["2_z"]

        x_diff["2_x"]=x_t_p["2_x"]-x_t_p["3_x"]
        x_diff["2_y"]=x_t_p["2_y"]-x_t_p["3_y"]
        #x_diff["2_z"]=x_t_p["2_z"]-x_t_p["3_z"]

        x_diff["4_x"]=x_t_p["3_x"]-x_t_p["4_x"]
        x_diff["4_y"]=x_t_p["3_y"]-x_t_p["4_y"]
        #x_diff["4_z"]=x_t_p["3_z"]-x_t_p["4_z"]

        x_diff["5_x"]=x_t_p["4_x"]-x_t_p["5_x"]
        x_diff["5_y"]=x_t_p["4_y"]-x_t_p["5_y"]
        #x_diff["5_z"]=x_t_p["4_z"]-x_t_p["5_z"]
        x_t_p=x_diff
    if use_diff ==2 : #combine
        x_diff=copy.deepcopy(x_t_p)
        x_diff["1_x"]=x_t_p["1_x"]-x_t_p["2_x"]
        x_diff["1_y"]=x_t_p["1_y"]-x_t_p["2_y"]
        #x_diff["1_z"]=x_t_p["1_z"]-x_t_p["2_z"]

        x_diff["2_x"]=x_t_p["2_x"]-x_t_p["3_x"]
        x_diff["2_y"]=x_t_p["2_y"]-x_t_p["3_y"]
        #x_diff["2_z"]=x_t_p["2_z"]-x_t_p["3_z"]

        x_diff["4_x"]=x_t_p["3_x"]-x_t_p["4_x"]
        x_diff["4_y"]=x_t_p["3_y"]-x_t_p["4_y"]
        #x_diff["4_z"]=x_t_p["3_z"]-x_t_p["4_z"]

        x_diff["5_x"]=x_t_p["4_x"]-x_t_p["5_x"]
        x_diff["5_y"]=x_t_p["4_y"]-x_t_p["5_y"]
        #x_diff["5_z"]=x_t_p["4_z"]-x_t_p["5_z"]

    for i,colume in enumerate(x_t_p):
        #print(colume)
        for num in x_t_p[colume]:

            tmp_sin=math.sin(num/180*math.pi)
            tmp_cos=math.cos(num/180*math.pi)
            if ignore_z != 0:
                if ('2' in colume) or  ('4' in colume) or ('5' in colume) :
                    #print("yes")
                    tmp_sin=0 
                    tmp_cos=0
            x_list[i].append(tmp_sin)
            x_list[i+10].append(tmp_cos)
    if use_diff == 2 :
        for i,colume in enumerate(x_diff):
            #print(colume)    
            for num in x_diff[colume]:   
                tmp_sin=math.sin(num/180*math.pi)
                tmp_cos=math.cos(num/180*math.pi)
                if ignore_z == 1:
                    if ('1' in colume) or ('2' in colume) or ('3' in colume) or  ('4' in colume) or ('5' in colume) :
                        #print("yes")
                        tmp_sin=0 
                        tmp_cos=0                
                if ignore_z == 2:
                    if ('2' in colume) or  ('4' in colume) or ('5' in colume) :
                        #print("yes")
                        tmp_sin=0 
                        tmp_cos=0
                

                x_add_list[i].append(tmp_sin)
                x_add_list[i+10].append(tmp_cos)
        '''
    for i,colume in enumerate(x_t_p):
        #print(i,colume)
        for num in x_t_p[colume]:
            x_list[i].append(math.sin(num/180*math.pi))
            x_list[i+10].append(math.cos(num/180*math.pi))
    if use_diff == 2 :
        for i,colume in enumerate(x_diff):
            #print(i,colume)
            for num in x_diff[colume]:
                x_add_list[i].append(math.sin(num/180*math.pi))
                x_add_list[i+10].append(math.cos(num/180*math.pi))
        '''


        x_dict={
            "1_x_sin": x_list[0], "1_y_sin": x_list[1], #"1_z_sin": x_list[2],
            "2_x_sin": x_list[2], "2_y_sin": x_list[3], #"2_z_sin": x_list[5], 
            "3_x_sin": x_list[4], "3_y_sin": x_list[5], #"3_z_sin": x_list[8],
            "4_x_sin": x_list[6], "4_y_sin": x_list[7],#"4_z_sin": x_list[11], 
            "5_x_sin": x_list[8], "5_y_sin": x_list[9], #"5_z_sin": x_list[14],
            "1_x_cos": x_list[10], "1_y_cos": x_list[11], #"1_z_cos": x_list[17], 
            "2_x_cos": x_list[12], "2_y_cos": x_list[13], #"2_z_cos": x_list[20],
            "3_x_cos": x_list[14], "3_y_cos": x_list[15], #"3_z_cos": x_list[23], 
            "4_x_cos": x_list[16], "4_y_cos": x_list[17], #"4_z_cos": x_list[26],
            "5_x_cos": x_list[18], "5_y_cos": x_list[19], #"5_z_cos": x_list[29],

            "add_1_x_sin": x_add_list[0], "add_1_y_sin": x_add_list[1], #"add_1_z_sin": x_add_list[2],
            "add_2_x_sin": x_add_list[2], "add_2_y_sin": x_add_list[3], #"add_2_z_sin": x_add_list[5], 
            "add_3_x_sin": x_add_list[4], "add_3_y_sin": x_add_list[5], #"add_3_z_sin": x_add_list[8],
            "add_4_x_sin": x_add_list[6], "add_4_y_sin": x_add_list[7],#"add_4_z_sin": x_add_list[11], 
            "add_5_x_sin": x_add_list[8], "add_5_y_sin": x_add_list[9], #"add_5_z_sin": x_add_list[14],
            "add_1_x_cos": x_add_list[10], "add_1_y_cos": x_add_list[11], #"add_1_z_cos": x_add_list[17], 
            "add_2_x_cos": x_add_list[12], "add_2_y_cos": x_add_list[13], #"add_2_z_cos": x_add_list[20],
            "add_3_x_cos": x_add_list[14], "add_3_y_cos": x_add_list[15], #"add_3_z_cos": x_add_list[23], 
            "add_4_x_cos": x_add_list[16], "add_4_y_cos": x_add_list[17], #"add_4_z_cos": x_add_list[26],
            "add_5_x_cos": x_add_list[18], "add_5_y_cos": x_add_list[19], #"add_5_z_cos": x_add_list[29],


        }
    else :
        x_dict={
            "1_x_sin": x_list[0], "1_y_sin": x_list[1], #"1_z_sin": x_list[2],
            "2_x_sin": x_list[2], "2_y_sin": x_list[3], #"2_z_sin": x_list[5], 
            "3_x_sin": x_list[4], "3_y_sin": x_list[5], #"3_z_sin": x_list[8],
            "4_x_sin": x_list[6], "4_y_sin": x_list[7],#"4_z_sin": x_list[11], 
            "5_x_sin": x_list[8], "5_y_sin": x_list[9], #"5_z_sin": x_list[14],
            "1_x_cos": x_list[10], "1_y_cos": x_list[11], #"1_z_cos": x_list[17], 
            "2_x_cos": x_list[12], "2_y_cos": x_list[13], #"2_z_cos": x_list[20],
            "3_x_cos": x_list[14], "3_y_cos": x_list[15], #"3_z_cos": x_list[23], 
            "4_x_cos": x_list[16], "4_y_cos": x_list[17], #"4_z_cos": x_list[26],
            "5_x_cos": x_list[18], "5_y_cos": x_list[19], #"5_z_cos": x_list[29]


        }

    x_t=pd.DataFrame(x_dict)

    
    #pc=PCA(n_components=2)
    #x_tsne = pc.fit(x)
    #x_t_tsne = pc.fit(x_t)
    
    #x_tsne = manifold.TSNE(n_components=8, init='random', random_state=5, verbose=1).fit_transform(x)

    #x_t_tsne = manifold.TSNE(n_components=8, init='random', random_state=5, verbose=1).fit_transform(x_t)

    validation_score=0
    test_score=0

    all_matrix=[[0]*num_fea for i in range(num_fea)]
    for i in range(number):
        #x_train, x_test, y_train, y_test=train_test_split(x,y, test_size=0.9, random_state=random.randint(1, 50))


        rfc.fit(x, y)
        #rfc.fit(x_train, y_train)


        validation_score+=rfc.score(x_test, y_test)  

        test_score+=rfc.score(x_t, y_t)

        y_prime = rfc.predict(x_t)

        array=confusion_matrix(y_prime,y_t)

        all_matrix+=array
    print(all_matrix)

    print("forest score validation", validation_score/number)
    print("forest score test ",test_score/number)  
    #print("good or bad", cnt/len(y_t))
    #print(x["1_x_sin"])

    ## for graph name
    import time # 引入time

    nowTime = int(time.time()) # 取得現在時間
    struct_time = time.localtime(nowTime) # 轉換成時間元組

    tree_name=(f'graph/{struct_time.tm_mday}{struct_time.tm_hour}{struct_time.tm_min}{struct_time.tm_sec}')
    from sklearn.tree import export_graphviz
    import pydot# Pull out one tree from the forest

    print(f'number of trees is : {len(rfc.estimators_)}')
    if collect_tree == 1: 

        for idx_tree,tree in enumerate(rfc.estimators_):

            all_matrix=[[0]*num_fea for i in range(num_fea)]
            validation_score=0
            test_score=0
            for i in range(number):
                #x_train, x_test, y_train, y_test=train_test_split(x,y, test_size=0.9, random_state=random.randint(1, 50))
                tree.fit(x, y)


                validation_score+= tree.score(x_test, y_test)  

                test_score+= tree.score(x_t, y_t)

                y_prime = tree.predict(x_t)

                array=confusion_matrix(y_prime,y_t)        
                all_matrix+=array

            #print(idx_tree,test_score/number)
            find_three(idx_tree, test_score/number, all_matrix)

        #tree_name='tree_dot'
        #視覺化

        for i in range(num_decisiontree):        
            print(f' number {i} score and array is = {list_three[i][1]}\n{list_three[i][2]}')
            tree_name=(f'graph/{i}')
            if use_diff == 2: 
                fl=feature_list[1]
            else:
                fl=feature_list[0]
            export_graphviz(rfc.estimators_[list_three[i][0]], out_file = tree_name, feature_names = fl     , rounded = True, precision = 1)# Use dot file to create a graph
            (graph, ) = pydot.graph_from_dot_file(tree_name)# Write graph to a png file
            tree_name+='.png'
            graph.write_png(tree_name)

def cluste():
    input('cluster?')
    use_combine_cluster = 1
    file=pd.read_csv(path)
    x_pre=file[["1_x","1_y","1_z","2_x","2_y","2_z","3_x","3_y","3_z","4_x","4_y","4_z","5_x","5_y","5_z"]]
    if use_combine_cluster ==1:
        if use_diff == 1:
            x_diff=x_pre  #會同時改兩個，後面要用 deepcopy
            x_diff["1_x"]=x_pre["1_x"]-x_pre["2_x"]
            x_diff["1_y"]=x_pre["1_y"]-x_pre["2_y"]
            x_diff["1_z"]=x_pre["1_z"]-x_pre["2_z"]

            x_diff["2_x"]=x_pre["2_x"]-x_pre["3_x"]
            x_diff["2_y"]=x_pre["2_y"]-x_pre["3_y"]
            x_diff["2_z"]=x_pre["2_z"]-x_pre["3_z"]

            x_diff["4_x"]=x_pre["3_x"]-x_pre["4_x"]  #new four is difference between three and four
            x_diff["4_y"]=x_pre["3_y"]-x_pre["4_y"]
            x_diff["4_z"]=x_pre["3_z"]-x_pre["4_z"]

            x_diff["5_x"]=x_pre["4_x"]-x_pre["5_x"] 
            x_diff["5_y"]=x_pre["4_y"]-x_pre["5_y"]
            x_diff["5_z"]=x_pre["4_z"]-x_pre["5_z"]

        if use_diff ==2 : #combine
            #print(f'x_pre = {x_pre}')
            x_diff=copy.deepcopy(x_pre)
            #print(f'x_pre = {x_pre}')
            x_diff["1_x"]=x_pre["1_x"]-x_pre["2_x"]
            x_diff["1_y"]=x_pre["1_y"]-x_pre["2_y"]
            x_diff["1_z"]=x_pre["1_z"]-x_pre["2_z"]

            x_diff["2_x"]=x_pre["2_x"]-x_pre["3_x"]
            x_diff["2_y"]=x_pre["2_y"]-x_pre["3_y"]
            x_diff["2_z"]=x_pre["2_z"]-x_pre["3_z"]

            x_diff["4_x"]=x_pre["3_x"]-x_pre["4_x"]  #new four is difference between three and four
            x_diff["4_y"]=x_pre["3_y"]-x_pre["4_y"]
            x_diff["4_z"]=x_pre["3_z"]-x_pre["4_z"]

            x_diff["5_x"]=x_pre["4_x"]-x_pre["5_x"] 
            x_diff["5_y"]=x_pre["4_y"]-x_pre["5_y"]
            x_diff["5_z"]=x_pre["4_z"]-x_pre["5_z"]
            #print(f'x_pre = {x_pre}')
            #input()

        #print(type(x_pre))
        #input()
        y=file[["good_or_bad"]]
        y=ravel(y)

        for i,colume in enumerate(x_pre):
            #print(colume)
            for num in x_pre[colume]:

                tmp_sin=math.sin(num/180*math.pi)
                tmp_cos=math.cos(num/180*math.pi)
                if ignore_z == 1:
                    if 'z' in colume:
                        #print("yes")
                        tmp_sin=0 
                        tmp_cos=0
                x_list[i].append(tmp_sin)
                x_list[i+10].append(tmp_cos)
        if use_diff == 2 :
            
            for i,colume in enumerate(x_diff):
                #print(colume)    
                for num in x_diff[colume]:   
                    tmp_sin=math.sin(num/180*math.pi)
                    tmp_cos=math.cos(num/180*math.pi)
                    if ignore_z == 1:
                        if 'z' in colume:
                            #print("yes")
                            tmp_sin=0 
                            tmp_cos=0


                    x_add_list[i].append(tmp_sin)
                    x_add_list[i+10].append(tmp_cos)
            

            x_dict={
                "1_x_sin": x_list[0], "1_y_sin": x_list[1], "1_z_sin": x_list[2],
                "2_x_sin": x_list[3], "2_y_sin": x_list[4], "2_z_sin": x_list[5], 
                "3_x_sin": x_list[6], "3_y_sin": x_list[7], "3_z_sin": x_list[8],
                "4_x_sin": x_list[9], "4_y_sin": x_list[10],"4_z_sin": x_list[11], 
                "5_x_sin": x_list[12], "5_y_sin": x_list[13], "5_z_sin": x_list[14],
                "1_x_cos": x_list[15], "1_y_cos": x_list[16], "1_z_cos": x_list[17], 
                "2_x_cos": x_list[18], "2_y_cos": x_list[19], "2_z_cos": x_list[20],
                "3_x_cos": x_list[21], "3_y_cos": x_list[22], "3_z_cos": x_list[23], 
                "4_x_cos": x_list[24], "4_y_cos": x_list[25], "4_z_cos": x_list[26],
                "5_x_cos": x_list[27], "5_y_cos": x_list[28], "5_z_cos": x_list[29],

                "add_1_x_sin": x_add_list[0], "add_1_y_sin": x_add_list[1], "add_1_z_sin": x_add_list[2],
                "add_2_x_sin": x_add_list[3], "add_2_y_sin": x_add_list[4], "add_2_z_sin": x_add_list[5], 
                "add_3_x_sin": x_add_list[6], "add_3_y_sin": x_add_list[7], "add_3_z_sin": x_add_list[8],
                "add_4_x_sin": x_add_list[9], "add_4_y_sin": x_add_list[10],"add_4_z_sin": x_add_list[11], 
                "add_5_x_sin": x_add_list[12], "add_5_y_sin": x_add_list[13], "add_5_z_sin": x_add_list[14],
                "add_1_x_cos": x_add_list[15], "add_1_y_cos": x_add_list[16], "add_1_z_cos": x_add_list[17], 
                "add_2_x_cos": x_add_list[18], "add_2_y_cos": x_add_list[19], "add_2_z_cos": x_add_list[20],
                "add_3_x_cos": x_add_list[21], "add_3_y_cos": x_add_list[22], "add_3_z_cos": x_add_list[23], 
                "add_4_x_cos": x_add_list[24], "add_4_y_cos": x_add_list[25], "add_4_z_cos": x_add_list[26],
                "add_5_x_cos": x_add_list[27], "add_5_y_cos": x_add_list[28], "add_5_z_cos": x_add_list[29],


            }
        else :
            x_dict={
                "1_x_sin": x_list[0], "1_y_sin": x_list[1], "1_z_sin": x_list[2],
                "2_x_sin": x_list[3], "2_y_sin": x_list[4], "2_z_sin": x_list[5], 
                "3_x_sin": x_list[6], "3_y_sin": x_list[7], "3_z_sin": x_list[8],
                "4_x_sin": x_list[9], "4_y_sin": x_list[10],"4_z_sin": x_list[11], 
                "5_x_sin": x_list[12], "5_y_sin": x_list[13], "5_z_sin": x_list[14],
                "1_x_cos": x_list[15], "1_y_cos": x_list[16], "1_z_cos": x_list[17], 
                "2_x_cos": x_list[18], "2_y_cos": x_list[19], "2_z_cos": x_list[20],
                "3_x_cos": x_list[21], "3_y_cos": x_list[22], "3_z_cos": x_list[23], 
                "4_x_cos": x_list[24], "4_y_cos": x_list[25], "4_z_cos": x_list[26],
                "5_x_cos": x_list[27], "5_y_cos": x_list[28], "5_z_cos": x_list[29]


            }
        '''
        x_dict={
            "1_x_sin": x_list[0], "1_y_sin": x_list[1], "1_z_sin": x_list[2],
            "2_x_sin": x_list[3], "2_y_sin": x_list[4], "2_z_sin": x_list[5], 
            "3_x_sin": x_list[6], "3_y_sin": x_list[7], "3_z_sin": x_list[8],
            "4_x_sin": x_list[9], "4_y_sin": x_list[10],"4_z_sin": x_list[11], 
            "5_x_sin": x_list[12], "5_y_sin": x_list[13], "5_z_sin": x_list[14],
            "1_x_cos": x_list[15], "1_y_cos": x_list[16], "1_z_cos": x_list[17], 
            "2_x_cos": x_list[18], "2_y_cos": x_list[19], "2_z_cos": x_list[20],
            "3_x_cos": x_list[21], "3_y_cos": x_list[22], "3_z_cos": x_list[23], 
            "4_x_cos": x_list[24], "4_y_cos": x_list[25], "4_z_cos": x_list[26],
            "5_x_cos": x_list[27], "5_y_cos": x_list[28], "5_z_cos": x_list[29]

        }
        '''
        x=pd.DataFrame(x_dict)

        input(f'usediff = {use_diff}  \n{x}\ncontinue?')
        init()

        file_t=pd.read_csv(test_path)
        x_t_p=file_t[["1_x","1_y","1_z","2_x","2_y","2_z","3_x","3_y","3_z","4_x","4_y","4_z","5_x","5_y","5_z"]]
        y_t=file_t[["good_or_bad"]]
        y_t=ravel(y_t)    
        if use_diff == 1:
            x_diff=x_t_p
            x_diff["1_x"]=x_t_p["1_x"]-x_t_p["2_x"]
            x_diff["1_y"]=x_t_p["1_y"]-x_t_p["2_y"]
            x_diff["1_z"]=x_t_p["1_z"]-x_t_p["2_z"]

            x_diff["2_x"]=x_t_p["2_x"]-x_t_p["3_x"]
            x_diff["2_y"]=x_t_p["2_y"]-x_t_p["3_y"]
            x_diff["2_z"]=x_t_p["2_z"]-x_t_p["3_z"]

            x_diff["4_x"]=x_t_p["3_x"]-x_t_p["4_x"]
            x_diff["4_y"]=x_t_p["3_y"]-x_t_p["4_y"]
            x_diff["4_z"]=x_t_p["3_z"]-x_t_p["4_z"]

            x_diff["5_x"]=x_t_p["4_x"]-x_t_p["5_x"]
            x_diff["5_y"]=x_t_p["4_y"]-x_t_p["5_y"]
            x_diff["5_z"]=x_t_p["4_z"]-x_t_p["5_z"]
            x_t_p=x_diff
        if use_diff ==2 : #combine
            x_diff=copy.deepcopy(x_pre)
            x_diff["1_x"]=x_pre["1_x"]-x_pre["2_x"]
            x_diff["1_y"]=x_pre["1_y"]-x_pre["2_y"]
            x_diff["1_z"]=x_pre["1_z"]-x_pre["2_z"]

            x_diff["2_x"]=x_pre["2_x"]-x_pre["3_x"]
            x_diff["2_y"]=x_pre["2_y"]-x_pre["3_y"]
            x_diff["2_z"]=x_pre["2_z"]-x_pre["3_z"]

            x_diff["4_x"]=x_pre["3_x"]-x_pre["4_x"]  #new four is difference between three and four
            x_diff["4_y"]=x_pre["3_y"]-x_pre["4_y"]
            x_diff["4_z"]=x_pre["3_z"]-x_pre["4_z"]

            x_diff["5_x"]=x_pre["4_x"]-x_pre["5_x"] 
            x_diff["5_y"]=x_pre["4_y"]-x_pre["5_y"]
            x_diff["5_z"]=x_pre["4_z"]-x_pre["5_z"]

        for i,colume in enumerate(x_t_p):
            #print(colume)
            for num in x_t_p[colume]:

                tmp_sin=math.sin(num/180*math.pi)
                tmp_cos=math.cos(num/180*math.pi)
                if ignore_z == 1:
                    if 'z' in colume:
                        #print("yes")
                        tmp_sin=0 
                        tmp_cos=0
                x_list[i].append(tmp_sin)
                x_list[i+10].append(tmp_cos)
        if use_diff == 2 :
            for i,colume in enumerate(x_diff):
                #print(colume)    
                for num in x_diff[colume]:   
                    tmp_sin=math.sin(num/180*math.pi)
                    tmp_cos=math.cos(num/180*math.pi)
                    if ignore_z == 1:
                        if 'z' in colume:
                            #print("yes")
                            tmp_sin=0 
                            tmp_cos=0
                    

                    x_add_list[i].append(tmp_sin)
                    x_add_list[i+10].append(tmp_cos)
            '''
        for i,colume in enumerate(x_t_p):
            #print(i,colume)
            for num in x_t_p[colume]:
                x_list[i].append(math.sin(num/180*math.pi))
                x_list[i+10].append(math.cos(num/180*math.pi))
        if use_diff == 2 :
            for i,colume in enumerate(x_diff):
                #print(i,colume)
                for num in x_diff[colume]:
                    x_add_list[i].append(math.sin(num/180*math.pi))
                    x_add_list[i+10].append(math.cos(num/180*math.pi))
            '''

            x_dict={
                "1_x_sin": x_list[0], "1_y_sin": x_list[1], "1_z_sin": x_list[2],
                "2_x_sin": x_list[3], "2_y_sin": x_list[4], "2_z_sin": x_list[5], 
                "3_x_sin": x_list[6], "3_y_sin": x_list[7], "3_z_sin": x_list[8],
                "4_x_sin": x_list[9], "4_y_sin": x_list[10],"4_z_sin": x_list[11], 
                "5_x_sin": x_list[12], "5_y_sin": x_list[13], "5_z_sin": x_list[14],
                "1_x_cos": x_list[15], "1_y_cos": x_list[16], "1_z_cos": x_list[17], 
                "2_x_cos": x_list[18], "2_y_cos": x_list[19], "2_z_cos": x_list[20],
                "3_x_cos": x_list[21], "3_y_cos": x_list[22], "3_z_cos": x_list[23], 
                "4_x_cos": x_list[24], "4_y_cos": x_list[25], "4_z_cos": x_list[26],
                "5_x_cos": x_list[27], "5_y_cos": x_list[28], "5_z_cos": x_list[29],

                "add_1_x_sin": x_add_list[0], "add_1_y_sin": x_add_list[1], "add_1_z_sin": x_add_list[2],
                "add_2_x_sin": x_add_list[3], "add_2_y_sin": x_add_list[4], "add_2_z_sin": x_add_list[5], 
                "add_3_x_sin": x_add_list[6], "add_3_y_sin": x_add_list[7], "add_3_z_sin": x_add_list[8],
                "add_4_x_sin": x_add_list[9], "add_4_y_sin": x_add_list[10],"add_4_z_sin": x_add_list[11], 
                "add_5_x_sin": x_add_list[12], "add_5_y_sin": x_add_list[13], "add_5_z_sin": x_add_list[14],
                "add_1_x_cos": x_add_list[15], "add_1_y_cos": x_add_list[16], "add_1_z_cos": x_add_list[17], 
                "add_2_x_cos": x_add_list[18], "add_2_y_cos": x_add_list[19], "add_2_z_cos": x_add_list[20],
                "add_3_x_cos": x_add_list[21], "add_3_y_cos": x_add_list[22], "add_3_z_cos": x_add_list[23], 
                "add_4_x_cos": x_add_list[24], "add_4_y_cos": x_add_list[25], "add_4_z_cos": x_add_list[26],
                "add_5_x_cos": x_add_list[27], "add_5_y_cos": x_add_list[28], "add_5_z_cos": x_add_list[29]


            }
        else :
            x_dict={
                "1_x_sin": x_list[0], "1_y_sin": x_list[1], "1_z_sin": x_list[2],
                "2_x_sin": x_list[3], "2_y_sin": x_list[4], "2_z_sin": x_list[5], 
                "3_x_sin": x_list[6], "3_y_sin": x_list[7], "3_z_sin": x_list[8],
                "4_x_sin": x_list[9], "4_y_sin": x_list[10],"4_z_sin": x_list[11], 
                "5_x_sin": x_list[12], "5_y_sin": x_list[13], "5_z_sin": x_list[14],
                "1_x_cos": x_list[15], "1_y_cos": x_list[16], "1_z_cos": x_list[17], 
                "2_x_cos": x_list[18], "2_y_cos": x_list[19], "2_z_cos": x_list[20],
                "3_x_cos": x_list[21], "3_y_cos": x_list[22], "3_z_cos": x_list[23], 
                "4_x_cos": x_list[24], "4_y_cos": x_list[25], "4_z_cos": x_list[26],
                "5_x_cos": x_list[27], "5_y_cos": x_list[28], "5_z_cos": x_list[29]


            }

        x_t=pd.DataFrame(x_dict)

    
    #  original  not combine feature
    if use_combine_cluster ==0:
        if use_diff == 1:
            x_diff=x_pre
            x_diff["1_x"]=x_pre["1_x"]-x_pre["2_x"]
            x_diff["1_y"]=x_pre["1_y"]-x_pre["2_y"]
            x_diff["1_z"]=x_pre["1_z"]-x_pre["2_z"]

            x_diff["2_x"]=x_pre["2_x"]-x_pre["3_x"]
            x_diff["2_y"]=x_pre["2_y"]-x_pre["3_y"]
            x_diff["2_z"]=x_pre["2_z"]-x_pre["3_z"]

            x_diff["4_x"]=x_pre["3_x"]-x_pre["4_x"]  #new four is difference between three and four
            x_diff["4_y"]=x_pre["3_y"]-x_pre["4_y"]
            x_diff["4_z"]=x_pre["3_z"]-x_pre["4_z"]

            x_diff["5_x"]=x_pre["4_x"]-x_pre["5_x"] 
            x_diff["5_y"]=x_pre["4_y"]-x_pre["5_y"]
            x_diff["5_z"]=x_pre["4_z"]-x_pre["5_z"]

            x_pre=x_diff


        y=file[["good_or_bad"]]
        y=ravel(y)

        for i,colume in enumerate(x_pre):
            #print(i,colume)
            for num in x_pre[colume]:
                x_list[i].append(math.sin(num/180*math.pi))
                x_list[i+10].append(math.cos(num/180*math.pi))
        x_dict={
                "1_x_sin": x_list[0], "1_y_sin": x_list[1], "1_z_sin": x_list[2],
                "2_x_sin": x_list[3], "2_y_sin": x_list[4], "2_z_sin": x_list[5], 
                "3_x_sin": x_list[6], "3_y_sin": x_list[7], "3_z_sin": x_list[8],
                "4_x_sin": x_list[9], "4_y_sin": x_list[10],"4_z_sin": x_list[11], 
                "5_x_sin": x_list[12], "5_y_sin": x_list[13], "5_z_sin": x_list[14],
                "1_x_cos": x_list[15], "1_y_cos": x_list[16], "1_z_cos": x_list[17], 
                "2_x_cos": x_list[18], "2_y_cos": x_list[19], "2_z_cos": x_list[20],
                "3_x_cos": x_list[21], "3_y_cos": x_list[22], "3_z_cos": x_list[23], 
                "4_x_cos": x_list[24], "4_y_cos": x_list[25], "4_z_cos": x_list[26],
                "5_x_cos": x_list[27], "5_y_cos": x_list[28], "5_z_cos": x_list[29]


        }
        x=pd.DataFrame(x_dict)

        init()

        file_t=pd.read_csv(test_path)
        x_t_p=file_t[["1_x","1_y","1_z","2_x","2_y","2_z","3_x","3_y","3_z","4_x","4_y","4_z","5_x","5_y","5_z"]]
        y_t=file_t[["good_or_bad"]]
        y_t=ravel(y_t)    
        if use_diff == 1:
            x_diff=x_t_p
            x_diff["1_x"]=x_t_p["1_x"]-x_t_p["2_x"]
            x_diff["1_y"]=x_t_p["1_y"]-x_t_p["2_y"]
            x_diff["1_z"]=x_t_p["1_z"]-x_t_p["2_z"]

            x_diff["2_x"]=x_t_p["2_x"]-x_t_p["3_x"]
            x_diff["2_y"]=x_t_p["2_y"]-x_t_p["3_y"]
            x_diff["2_z"]=x_t_p["2_z"]-x_t_p["3_z"]

            x_diff["4_x"]=x_t_p["3_x"]-x_t_p["4_x"]
            x_diff["4_y"]=x_t_p["3_y"]-x_t_p["4_y"]
            x_diff["4_z"]=x_t_p["3_z"]-x_t_p["4_z"]

            x_diff["5_x"]=x_t_p["4_x"]-x_t_p["5_x"]
            x_diff["5_y"]=x_t_p["4_y"]-x_t_p["5_y"]
            x_diff["5_z"]=x_t_p["4_z"]-x_t_p["5_z"]
            x_t_p=x_diff

        for i,colume in enumerate(x_t_p):
            #print(i,colume)
            for num in x_t_p[colume]:
                x_list[i].append(math.sin(num/180*math.pi))
                x_list[i+10].append(math.cos(num/180*math.pi))
        x_dict={
            "1_x_sin": x_list[0], "1_y_sin": x_list[1], "1_z_sin": x_list[2],
            "2_x_sin": x_list[3], "2_y_sin": x_list[4], "2_z_sin": x_list[5], 
            "3_x_sin": x_list[6], "3_y_sin": x_list[7], "3_z_sin": x_list[8],
            "4_x_sin": x_list[9], "4_y_sin": x_list[10],"4_z_sin": x_list[11], 
            "5_x_sin": x_list[12], "5_y_sin": x_list[13], "5_z_sin": x_list[14],
            "1_x_cos": x_list[15], "1_y_cos": x_list[16], "1_z_cos": x_list[17], 
            "2_x_cos": x_list[18], "2_y_cos": x_list[19], "2_z_cos": x_list[20],
            "3_x_cos": x_list[21], "3_y_cos": x_list[22], "3_z_cos": x_list[23], 
            "4_x_cos": x_list[24], "4_y_cos": x_list[25], "4_z_cos": x_list[26],
            "5_x_cos": x_list[27], "5_y_cos": x_list[28], "5_z_cos": x_list[29]

        }
        x_t=pd.DataFrame(x_dict)
    



    x_tsne = manifold.TSNE(n_components=2, init='random', random_state=5, verbose=1).fit_transform(x)
    
    x_t_tsne = manifold.TSNE(n_components=2, init='random', random_state=5, verbose=1).fit_transform(x_t)
    '''
    kmeans_fit = cluster.KMeans(n_clusters = num_fea).fit(x)

   
    new_dy = kmeans_fit.predict(x)


    plt.rcParams['font.size'] = 14
    plt.figure(figsize=(16, 8))# 以不同顏色畫出原始的 10 群資料

    plt.subplot(121)
    plt.title(f'Original data ({num_fea} groups)')
    plt.scatter(x_tsne.T[0], x_tsne.T[1], c=y, cmap=plt.cm.Set1)# 根據重新分成的 5 組來畫出資料
    plt.subplot(122)
    plt.title(f'KMeans= {num_fea} groups')
    plt.scatter(x_tsne.T[0], x_tsne.T[1], c=new_dy, cmap=plt.cm.Set1)# 顯示圖表
    plt.tight_layout()
    plt.show()

    plt.savefig('graph/ori_pridict_plot.png')
    '''

    cnt=0
    num_kmean_times = 20
    y_cl_idx_group = [[],[],[],[],[],[],[]] # ...[i] means index of cluster i
    yt_cl_idx_group = [[],[],[],[],[],[],[]] # ...[i] means index of cluster i
    y_idx_group = [[],[],[],[],[],[],[]]
    yt_idx_group = [[],[],[],[],[],[],[]]
    for k in range(num_kmean_times):
        kmeans_fit = cluster.KMeans(n_clusters = num_fea).fit(x)
        
        #cluster_y = kmeans_fit.predict(x_tsne)
        cluster_y = kmeans_fit.predict(x)

        cluster_y_t = kmeans_fit.predict(x_t)
        '''
        print(list(y))
        print(list(y_t))
        '''
        
        #print(list(cluster_y))
        #print()
        #print(list(cluster_y_t))
        
        map_sit=cluster_y_t[0]
        map_stand=cluster_y_t[-1]
        
        #print(f'mapsit = {map_sit}, map_stand = {map_stand}')
        for i in range(len(cluster_y)):
            if  ((y[i]==1) == (cluster_y_t[i]!=map_sit)) or ((y[i]==7) == (cluster_y_t[i]!=map_stand)) :
                #print(i)
                cnt+=1
       # print(cnt)
        #print(len(cluster_y))
        


        for idx_array in range(len(cluster_y)):
            #print(idx_array)
            y_cl_idx_group[cluster_y[idx_array]].append(idx_array)
            yt_cl_idx_group[cluster_y_t[idx_array]].append(idx_array)
            y_idx_group[y[idx_array]-1].append(idx_array)                #y是從1~7，所以要減1
            yt_idx_group[y_t[idx_array]-1].append(idx_array)

        #print(list(cluster_y))
        #print(list(y))

        #print(list(cluster_y_t))
        #print(list(y_t))
        
        '''
        for i in range(len(y)):
            if cluster_y[i]!= cluster_y_t[i]:
                cnt+=1
        '''
    #print(confusion_matrix(cluster_y,cluster_y_t))
    #print(1-cnt/len(y)/num_kmean_times)
    print(f'accuracy is {1-cnt/len(cluster_y)/num_kmean_times}')


    # tsne then cluster
    '''
    cnt=0
    kmeans_fit = cluster.KMeans(n_clusters = num_fea).fit(x_tsne)
    

    #cluster_y = kmeans_fit.predict(x_tsne)
    cluster_y = kmeans_fit.predict(x_tsne)

    cluster_y_t = kmeans_fit.predict(x_t_tsne)
    #print(confusion_matrix(cluster_y,cluster_y_t))
    for i in range(len(y)):
        if cluster_y[i]!= cluster_y_t[i]:
            cnt+=1

    #print(1-cnt/len(y))

    '''

    input('finish predict  ready to draw picture\ncontinue?')
    mycolor=["pink","blue","brown","red","grey","yellow","green"]
    plt.rcParams['font.size'] = 14

    print('start')
    plt.figure(figsize=(16, 8))# 以不同顏色畫出原始的 10 群資料
    
    plt.subplot(222) #  mean , from top to down    from left to right    the number
    #plt.title(f'Original data ({num_fea} groups)')
    print('start 2 ')
    plt.title('my own precict raw data (not tsne) ')
    for i in range(7):
        for idx in y_cl_idx_group[i]: #my own predict
            plt.scatter(x_tsne.T[0][idx], x_tsne.T[1][idx], c=mycolor[i])# 畫圖是二維，所以還是要tsne    
    print('finish  own predict')
    plt.subplot(221)
    
    #plt.title(f'Original data ({num_fea} groups)')
    plt.title('my own correct raw data (not tsne) ')
    for i in range(7):
        for idx in y_idx_group[i]: # my own correct
            plt.scatter(x_tsne.T[0][idx], x_tsne.T[1][idx], c=mycolor[i])# 畫圖是二維，所以還是要tsne
    
    print('finish  own  correct')
    plt.subplot(224)
    #plt.title(f'KMeans= {num_fea} groups')
    plt.title('roommate precict raw data (not tsne) ')
    for i in range(7):
        for idx in yt_cl_idx_group[i]: #roommate predict
            plt.scatter(x_t_tsne.T[0][idx], x_t_tsne.T[1][idx], c=mycolor[i])# 畫圖是二維，所以還是要tsne   
    #plt.scatter(x_t_tsne.T[0], x_t_tsne.T[1], c=cluster_y_t, cmap=plt.cm.Set1)# 顯示圖表    
    
    
    plt.subplot(223)
    plt.title('roommate correct raw data (not tsne) ')
    for i in range(7):
        for idx in yt_idx_group[i]: #roommate correct
            plt.scatter(x_t_tsne.T[0][idx], x_t_tsne.T[1][idx], c=mycolor[i])# 畫圖是二維，所以還是要tsne   
    #plt.scatter(x_t_tsne.T[0], x_t_tsne.T[1], c=y_t, cmap=plt.cm.Set1)# 顯示圖表
    
    plt.tight_layout()
    plt.show()
    print('finish  rommate correct')
    plt.savefig('graph/compare_raw_predict.png')
    
    
    input('finish raw data')
    return


    # for x_t
    '''
    kmeans_fit = cluster.KMeans(n_clusters = num_fea).fit(x_tsne)

    cluster_y = kmeans_fit.predict(x_tsne)
    cluster_y_t = kmeans_fit.predict(x_t_tsne)


    plt.rcParams['font.size'] = 14
    plt.figure(figsize=(16, 8))# 以不同顏色畫出原始的 10 群資料

    plt.subplot(121)
    #plt.title(f'Original data ({num_fea} groups)')
    plt.title('my own precict tsne data ')
    plt.scatter(x_tsne.T[0], x_tsne.T[1], c=cluster_y, cmap=plt.cm.Set1)# 根據重新分成的 5 組來畫出資料
    plt.subplot(122)
    #plt.title(f'KMeans= {num_fea} groups')
    plt.title('roommate precict tsne data ')
    plt.scatter(x_t_tsne.T[0], x_t_tsne.T[1], c=cluster_y_t, cmap=plt.cm.Set1)# 顯示圖表
    plt.tight_layout()
    plt.show()

    plt.savefig('graph/compare_tsne_predict.png')
    

    '''

if __name__ == '__main__':
    #origin_train()

    sin_cos()
    #cluste()



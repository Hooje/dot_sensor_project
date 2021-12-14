'''
punc = '。，、；：「」『』（）─？！─…﹏《》〈〉．～　,.; !\"#$%&\'()*+,-./:;<=>?@[]^_`{¦}~'  # 加上你要的全型，當成String直接加進去就好
#print(f'punc = {punc}, 最後記得要註解掉，這個不用印')
n =  int(input())
if n < 2:
    print('ILLEGAL_N')

else:
    #print(n)
    #n = 4
    sentence = input() #讀第一行
    #subsentence = sentence.split('')

    cnt = 0 # 數字數，滿n個就印
    every_line = '' # 要印的字
    for word in sentence: # 一個字一個字看
        #print(word)
        if word in punc: # 如果下一個字是符號，那就要從0開始數 ｎ　個，而不是用前一句的最後幾個字再加一個字
            cnt = 0
            every_line = '' #要印的字就要從頭開始
            continue  # continue表示這層的for不用繼續往後走，直接看下一個 for
        every_line += word  # string 可以用加的
        cnt += 1  
        if cnt == n : #字數滿了，就印出來
            print(every_line)  #印出來
            every_line = every_line[1:]  # [1:]表示從第1個開始到最後，也就是不看第0個  
            cnt -= 1   # cnt 表示累積字數，減一，等等就再加一個字就滿了

        elif word == sentence[-1]:  #如果已經到最後一個字，但不足n個字，也要印出來  (題目沒說，我猜要印 )
            print(every_line)

'''

# 數字串數，把每個print(every_line) 稍微修改

punc = '。，、；：「」『』（）─？！─…﹏《》〈〉．～　,.; !\"#$%&\'()*+,-./:;<=>?@[]^_`{¦}~'  # 加上你要的全型，當成String直接加進去就好
#print(f'punc = {punc}')

target_len = 0
match_len = 0

target_list = []  #每個target連續詞放進來，後面再檢查source的每個連續詞 有沒有在這裡面
match_list = [] #共有的連續詞

n =  int(input())
if n < 2:
    print('ILLEGAL_N')

else:

    target_sentence = input() #讀target

    cnt = 0 
    every_line = ''
    for word in target_sentence:
        if word in punc:
            cnt = 0
            every_line = ''
            continue 
        every_line += word 
        cnt += 1  
        if cnt == n :
            #print(every_line)  
            target_len += 1
            target_list.append(every_line) #把每個連續詞放進來，後面再檢查source的每個連續詞 有沒有在這裡面
            every_line = every_line[1:] 
            cnt -= 1 

        elif word == target_sentence[-1]: 
            #print(every_line)            
            target_len += 1
            target_list.append(every_line) #把每個連續詞放進來，後面再檢查source的每個連續詞 有沒有在這裡面
    
    source_sentence = input() #讀source
    cnt = 0 
    every_line = ''
    for word in source_sentence:
        if word in punc:
            cnt = 0
            every_line = ''
            continue 
        every_line += word 
        cnt += 1  
        if cnt == n :
            
            if every_line in target_list: #如果連續詞在target出現過，就加進去match_list，也加一下match數量
                match_list.append(every_line)
                match_len += 1
            #target_list.append(every_line) #把每個連續詞放進來，後面再檢查source的每個連續詞 有沒有在這裡面
            every_line = every_line[1:] 
            cnt -= 1 

        elif word == source_sentence[-1]: 
            if every_line in target_list: #如果連續詞在target出現過，就加進去match_list，也加一下match數量
                match_list.append(every_line)
                match_len += 1
    print(f'LEN={target_len}')
    print(f'MATCH_COUNT={match_len}')
    print(f'SIMILARITY={match_len/target_len:.4f}')
    print('MATCHED SEGMENTS:')
    for m in match_list:
        print(m)

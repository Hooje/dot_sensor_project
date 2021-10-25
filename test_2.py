
n = int(input())

a = []
b = []
c = []

max_i = [0, 0, 0] # value, p, i
max_value_p = [0,0] # value , p
for i in range(n):
    a_temp = int(input())
    b_temp = int(input())
    c_temp = int(input())
    a.append(a_temp)
    b.append(b_temp)
    c.append(c_temp)

for i in range(n):
    for p in range(c[i]+1, a[i]//b[i]+1):
        now = (a[i] - (b[i]*p))*(p-c[i])
        #print(p, now)
        if now >= max_value_p[0]:
            max_value_p = [now, p] 

    #print(max_value_p)

    if max_value_p[0] > max_i[0]:
        max_i = [max_value_p[0], max_value_p[1], i]

if max_i[1] == 0:
    max_i[1] = 1000
print('%d,%d,%d' % (int(max_i[2]+1), int(max_i[1]),int(max_i[0])))

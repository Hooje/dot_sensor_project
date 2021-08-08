import torch
from torch import nn
import torch.nn as nn 
import pandas as pd
import numpy as np

seq_len = 5
num_each_batch= 20 #0~19  1~20

cols_num = 10
hidden_size= 10 
num_layers = 3
input_size= 15
max_epoch = 100
last_num = 1300 #about 1300~1319
learning_rate = 1

y = []
for i in range(7):
    y += [i+1]*200 

with open('loss_0727', 'a') as f:
    f.write('\n\n**********************\n\n')    

class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTM, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
        )

        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, inputs):
        out, (h_n, c_n) = self.lstm(inputs, None)
        outputs = self.fc(out.squeeze(0))

        return outputs

#f = open("loss_0727", "a") # if not use with open , you have to close.  a means append
#f.write(f'close = {cols_num}\n')
#input()
def data_loader(num_each_batch, fp):

    for f in fp:
        file=pd.read_csv(f)
        df=file[["1_x","1_y","1_z","2_x","2_y","2_z","3_x","3_y","3_z","4_x","4_y","4_z","5_x","5_y","5_z"]]
        y = file[["good_or_bad"]]
        row_count, col_count = df.shape
        encoder_input = []
        
        #print(f'row={row_count}')
        for prev in range(row_count):
            end = prev + num_each_batch
            window = df.iloc[prev:end]

            w = np.array(window, dtype='float64')
            if w.shape[0] != num_each_batch:  break
            encoder_input.append(w)
            if prev == last_num:
                w0 = encoder_input
                encoder_input = []
                yield w0  # the first one in the loader is fp[0], second is fp[1]

                break



fp = ["sit_stand1.csv", "sit_stand3.csv"]

loader = data_loader(num_each_batch=num_each_batch, fp=fp)
lstm = LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers) #use my LSTM

loadlist=list(loader)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(lstm.parameters(), lr=learning_rate)


y=torch.tensor(y,dtype=torch.long)
#input(y.size())
torch.reshape(y,(1,1400))

for epoch in range(max_epoch):
    data = loadlist[0]  #data mean training or testing

    b = torch.tensor(data, dtype=torch.float32)

    output=lstm(b)
    
    output=output.reshape(output.size(),)
    loss = loss_fn(output, torch.reshape(y[:1301],(1301,1))) #means y[0:1301] y from 0 to 1300 (end is not included)
    

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print(f'loss = {loss}')
    with open('loss_0727', 'a') as f:
        f.write(f'epoch : {epoch}  |  lose = {loss} \n')    


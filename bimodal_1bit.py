import math
correct=0
total=0
trace_file_name=input("Trace file name: ")
indexing_bits = int(input("Enter the number of PC bits to be used for Indexing: "))
table_size=pow(2,indexing_bits)
bht_table=[]
btb_table=[]
for i in range(table_size):
    bht_table.append(0)         #initialising or predicting as NT for the very first iteration
    btb_table.append([0,0])
#print(bht_table)
f=open(trace_file_name,'r') #the trace file must be in the same folder as the .py file
lines=f.readlines()
for line in lines:
    sline = line.split()    
    #print(type(sline[0]),sline[2])
    address=int(sline[0],16)
    target=int(sline[2],16) #python treats hex numbers as int... the hex() function will return string type
    #print(sline[0]%16)
    if(bht_table[address % table_size]==1 and sline[1]=="NT"):
        bht_table[address % table_size]=0
    elif(bht_table[address % table_size]==0 and sline[1]=="T"):
        bht_table[address % table_size]=1
    else:
        correct=correct+1
        ### calculating branch target address through btb 
        if(bht_table[address % table_size]==1):
            if(btb_table[address % table_size][0]==sline[0][0:len(sline[0])-int(indexing_bits/4)]):
                target_address=btb_table[address % table_size][1]
            else: ### Appending into BTB (Cache of recently taken target addresses BTB)
                btb_table[address % table_size][0]=sline[0][0:len(sline[0])-int(indexing_bits/4)]
                btb_table[address % table_size][1]=sline[2]
    total=total+1
print("Correct predictions: ",correct," Total predictions: ",total)
print(btb_table)
#print(bht_table)

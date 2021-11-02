correct=0
total=0
trace_file_name=input("Trace file name: ")
pht_indexing_bits = int(input("Enter the number of PC bits to be used for Indexing: "))
bht_indexing_bits=3
bht_table_size=pow(2,bht_indexing_bits)
pht_table_size=pow(2,pht_indexing_bits)
bht_table=[]
pht_table=[]
btb_table=[]
for i in range(bht_table_size):
    bht_table.append("000")         #initially NT
for i in range(pht_table_size):    
    pht_table.append(3)             #initially strongly taken
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
    bht_index=address%8
    pht_sub2_index=bht_table[bht_index]
    pht_sub1_index=str(bin(address % pow(2,pht_indexing_bits-bht_indexing_bits)).replace("0b", ""))
    pht_index=int(pht_sub1_index+pht_sub2_index,2)
    #print(pht_index)
    if(0<pht_table[pht_index] and pht_table[pht_index]<=3 and sline[1]=="NT"):
        if (pht_table[pht_index]<2):
            correct=correct+1
        pht_table[pht_index]=pht_table[pht_index]-1
        bht_table[bht_index]=bht_table[bht_index]+"0"
        bht_table[bht_index]=bht_table[bht_index][1:]
    elif(pht_table[pht_index]>=0 and pht_table[pht_index]<3 and sline[1]=="T"):
        if(pht_table[pht_index]>=2):
            correct=correct+1
        pht_table[pht_index]=pht_table[pht_index]+1
        bht_table[bht_index]=bht_table[bht_index]+"1"
        bht_table[bht_index]=bht_table[bht_index][1:]
    else:
        correct=correct+1
        if(pht_table[pht_index]==0):
            bht_table[bht_index]=bht_table[bht_index]+"0"
            bht_table[bht_index]=bht_table[bht_index][1:]
        if(pht_table[pht_index]==3):
            bht_table[bht_index]=bht_table[bht_index]+"1"
            bht_table[bht_index]=bht_table[bht_index][1:]    
        ######## calculating branch target address through btb 
        if(pht_table[pht_index]>=2):
            if(btb_table[pht_index][0]==sline[0][0:len(sline[0])-int(pht_indexing_bits/4)]):
                target_address=btb_table[pht_index][1]
            else: ### Appending into BTB (Cache of recently taken target addresses BTB)
                btb_table[pht_index][0]=sline[0][0:len(sline[0])-int(pht_indexing_bits/4)]
                btb_table[pht_index][1]=sline[2]
    total=total+1
print("Correct predictions: ",correct," Total predictions: ",total)
print(btb_table)

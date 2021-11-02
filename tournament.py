import math
correct=0
total=0
trace_file_name=input("Trace file name: ")
indexing_bits = int(input("Enter the number of PC bits to be used for Indexing: "))
ext = 0
selector_table = []
bht_indexing_bits=3
pht_indexing_bits=11
bht_table = []
pht_table = []
bht_table_size=pow(2,bht_indexing_bits)
pht_table_size=pow(2,pht_indexing_bits)
for i in range(bht_table_size):
    bht_table.append("000")         #initialising or predicting as T for the very first iteration
for i in range(pht_table_size):    
    pht_table.append(0)                 #initializing predictions as NT
  # btb_table.append([0,0])
for i in range(indexing_bits):
    ext = (ext << 1) | 1
bhr = 0
pht_table_gshare =[]
btb_table_gshare = []
for i in range(2048):
    pht_table_gshare.append(0)
    selector_table.append(0)
f=open(trace_file_name,'r') #the trace file must be in the same folder as the .py file
lines=f.readlines()
for line in lines:
    sline = line.split()
    address=int(sline[0],16)
    target=int(sline[2],16) #python treats hex numbers as int... the hex() function will return string type
    temp = bhr & ext            # and with ext to limit bhr bit length
    #print("TEMP:" + str(temp))
    
    gshare_index = (address%2048) ^ temp 
    selector_index = (address%2048)

    bht_index=address%8
    pht_sub2_index=bht_table[bht_index]
    pht_sub1_index=str(bin(address % pow(2,pht_indexing_bits-bht_indexing_bits)).replace("0b", ""))
    pht_index=int(pht_sub1_index+pht_sub2_index,2)
    
    gshare_pred = pht_table_gshare[gshare_index]
    history_pred = pht_table[pht_index]
    selector_pred = selector_table[selector_index]
    
    if(selector_pred>=0 and selector_pred <2):
        if(((gshare_pred>=0 and gshare_pred<2) and sline[1]=="NT") or (gshare_pred>=2 and gshare_pred<=3 and sline[1] == "T")):
            correct+=1
            if((gshare_pred>=0 and gshare_pred<2) and not(history_pred>=0 and history_pred<2) and sline[1] == "NT"):
                if(selector_table[selector_index] > 0):
                    selector_table[selector_index]-=1
                
            elif((gshare_pred>=2 and gshare_pred<=3) and not(history_pred>=2 and history_pred<=3) and sline[1]=="T"):
                if(selector_table[selector_index]>0):
                    selector_table[selector_index]-=1
            
        else:
            if(not(gshare_pred>=0 and gshare_pred<2) and (history_pred>=0 and history_pred<2) and sline[1] == "NT"):
                if(selector_table[selector_index] < 3):
                    selector_table[selector_index]+=1
                
            elif(not(gshare_pred>=2 and gshare_pred<=3) and (history_pred>=2 and history_pred<=3) and sline[1]=="T"):
                if(selector_table[selector_index]<3):
                    selector_table[selector_index]+=1
    
    elif(selector_pred>=2 and selector_pred<=3):
        if((history_pred>=0 and history_pred<2 and sline[1] == "NT") or (history_pred>=2 and history_pred<=3 and sline[1] == "T")):
            correct+=1
            if((history_pred>=0 and history_pred<2)and not(gshare_pred>=0 and gshare_pred<2) and sline[1]=="NT"):
                if(selector_table[selector_index] <3):
                    selector_table[selector_index]+=1
                
            elif((history_pred>=2 and history_pred<=3) and not(gshare_pred>=2 and gshare_pred<=3) and sline[1]=="T"):
                if(selector_table[selector_index]<3):
                    selector_table[selector_index]+=1
            
        else:
            if(not(history_pred>=0 and history_pred<2) and (gshare_pred>=0 and gshare_pred<2) and sline[1]=="NT"):
                if(selector_table[selector_index]>0):
                    selector_table[selector_index]-=1
            elif(not(history_pred>=2 and history_pred<=3) and (gshare_pred>=2 and gshare_pred<=3) and sline[1]=="T"):
                if(selector_table[selector_index]>0):
                    selector_table[selector_index]-=1
    
    if(sline[1]=="NT"):                 #Storing predictions for future references for a branch
        if(pht_table_gshare[gshare_index]>0):
            pht_table_gshare[gshare_index]-=1
        if(pht_table[pht_index]>0):
            pht_table[pht_index]=pht_table[pht_index]-1
            bht_table[bht_index]=bht_table[bht_index]+"0"
            bht_table[bht_index]=bht_table[bht_index][1:] 

    elif(sline[1]=="T"):
        if(pht_table_gshare[gshare_index]<3):
            pht_table_gshare[gshare_index]+=1
        if(pht_table[pht_index]<3):
            pht_table[pht_index]+=1
            pht_table[pht_index]=pht_table[pht_index]+1
            bht_table[bht_index]=bht_table[bht_index]+"1"
            bht_table[bht_index]=bht_table[bht_index][1:]

    else:
        if(pht_table[pht_index]==0):
            bht_table[bht_index]=bht_table[bht_index]+"0"
            bht_table[bht_index]=bht_table[bht_index][1:]
        if(pht_table[pht_index]==3):
            bht_table[bht_index]=bht_table[bht_index]+"1"
            bht_table[bht_index]=bht_table[bht_index][1:]     
    if(sline[1]=="T"):
        bhr = (bhr <<1 | 1)
    else:
        bhr = bhr << 1
    
    total +=1


print("Correct predictions: ",correct," Total predictions: ",total)
#print(btb_table)

import math
correct=0
total=0
trace_file_name=input("Trace file name: ")
indexing_bits = int(input("Enter the number of PC bits to be used for Indexing: "))
ext = 0
for i in range(indexing_bits):
    ext = (ext << 1) | 1
bhr = 0                 #Branch history register
pht_table =[]               #Pattern history table
btb_table = []
for i in range(2048):
    pht_table.append(3)             #Taking ST initially
    btb_table.append([0,0])
f=open(trace_file_name,'r') #the trace file must be in the same folder as the .py file
lines=f.readlines()
for line in lines:
    #print("BHR:"+ str(bhr))
    sline = line.split()
    address=int(sline[0],16)
    target=int(sline[2],16) #python treats hex numbers as int... the hex() function will return string type
    temp = bhr & ext            # and with ext to limit bhr bit length
    #print("TEMP:" + str(temp))
    index = (address%2048) ^ temp    #XOR address with temp
    if(sline[1] == "T"):
        bhr = (bhr << 1 | 1)
    else:
        bhr = bhr << 1
    if(pht_table[index] > 0 and pht_table[index]<=3 and sline[1] =="NT"):
        if(pht_table[index]<2):
            correct+=1
        pht_table[index]-=1
    elif(pht_table[index]>=0 and pht_table[index]<3 and sline[1] == "T"):
        if(pht_table[index]>=2):
            correct+=1
        pht_table[index]+=1
    else:
        correct+=1
        ### calculating branch target address through btb 
        if(pht_table[index]>=2):
            if(btb_table[index][0]==sline[0][0:len(sline[0])-int(indexing_bits/4)]):
                target_address=btb_table[index][1]
            else: ### Appending into BTB (Cache of recently taken target addresses BTB)
                btb_table[index][0]=sline[0][0:len(sline[0])-int(indexing_bits/4)]
                btb_table[index][1]=sline[2]
    total+=1

print("Correct predictions: ",correct," Total predictions: ",total)
print(btb_table)

from collections import defaultdict 

file1 = open("result.txt", "r")
file2 = open("logs.txt", "w")
lst=file1.readlines()
# print(len(lst))
dictionary1=defaultdict()
dictionary2=defaultdict()
for i in range(len(lst)):
    line=lst[i]
    line=list(line.split(" "))
    dictionary1[i]=((float(line[4])-1000)/200)+1000
    dictionary2[i]=str(line[5]+" "+line[6]+" "+line[7]+" "+line[8]+" "+line[9]+" "+line[10])
    # print(dictionary1)
    # print(line)
file1.close
# print(dictionary1)
sorting=sorted(dictionary1.items(), key=lambda kv:(kv[1], kv[0]))
keylist=[]
for i in sorting:
    keylist.append(i[0])
# print(keylist)
for i in range(len(lst)):
    line=lst[i]
    line=list(line.split(" "))
    file2.writelines(str(i+1)+" "+line[2]+" "+line[3]+" "+str(dictionary1[keylist[i]])+" "+dictionary2[keylist[i]])

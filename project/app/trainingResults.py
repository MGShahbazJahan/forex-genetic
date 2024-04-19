from collections import defaultdict

def get_training_results():
    file = open("logs.txt", "r")
    lst=list(file.readlines())
    dictionary=defaultdict()
    dictionary["generation"]=[]
    dictionary["result"]=[]
    dictionary["rsi_parameter"]=[]
    dictionary["mfi_parameter"]=[]
    dictionary["ma_parameter"]=[]
    dictionary["bbands_parameter"]=[]
    for i in range(len(lst)):
        row=lst[i].split(" ")
        dictionary["generation"].append(i+1)
        dictionary["result"].append(float(row[3]))
        dictionary["rsi_parameter"].append(float(row[4]))
        dictionary["mfi_parameter"].append(float(row[5]))
        dictionary["ma_parameter"].append(float(row[6]))
        dictionary["bbands_parameter"].append(float(row[7]))
    return dictionary

        
get_training_results()
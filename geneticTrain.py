import yfinance as yf
import datetime as dt
import random
from collections import defaultdict 
from project.app.indicator import MFI, RSI, MA, BBANDS

def fetch_weights():
        file = open("weights.txt", "r")
        lst=file.readlines()
        dictionary=defaultdict()
        dictionary["rsi_parameter"]=float(lst[0])
        dictionary["mfi_parameter"]=float(lst[1])
        dictionary["ma_parameter"]=float(lst[2])
        dictionary["bbands_parameter"]=float(lst[3])
        dictionary["capital_percentage"]=float(lst[4])
        dictionary["trade_threshold"]=float(lst[5])
        dictionary["remaining_capital"]=1000
        dictionary["starting_capital"]=1000
        file.close
        return dictionary

def generation(rsi,mfi,bbands,sma,ewma,learning_rate):    
    def populate(weights):
        num_of_players=20
        population=[weights]
        new_weights=defaultdict()
        for i in range(num_of_players):
            new_weights.clear()
            rand_num=random.randint(-1000,1000)
            new_weights["rsi_parameter"]=weights["rsi_parameter"]+rand_num*learning_rate/1000
            rand_num=random.randint(-1000,1000)
            new_weights["mfi_parameter"]=weights["mfi_parameter"]+rand_num*learning_rate/1000
            rand_num=random.randint(-1000,1000)
            new_weights["ma_parameter"]=weights["ma_parameter"]+rand_num*learning_rate/1000
            rand_num=random.randint(-1000,1000)
            new_weights["bbands_parameter"]=weights["bbands_parameter"]+rand_num*learning_rate/1000
            rand_num=random.randint(-1000,1000)
            new_weights["capital_percentage"]=weights["capital_percentage"]+rand_num*learning_rate/1000
            rand_num=random.randint(-1000,1000)
            new_weights["trade_threshold"]=weights["trade_threshold"]+rand_num*learning_rate/1000
            new_weights["remaining_capital"]=weights["starting_capital"]
            new_weights["starting_capital"]=weights["starting_capital"]
            population.append(new_weights)
            # print(new_weights)

        return population

    def play_game(list_of_population,rsi,mfi,bbands,sma,ewma):
        result_of_game=[]
        for i in range(len(list_of_population)):
            weights_of_individual=list_of_population[i]
            individual_portfolio=defaultdict()
            individual_portfolio["remaining_capital"]=weights_of_individual["starting_capital"]
            individual_portfolio["starting_capital"]=weights_of_individual["starting_capital"]
            individual_portfolio["number_of_stock"]=0
            for j in range(len(rsi)):
                buy_sell_signal=rsi[j]*weights_of_individual["rsi_parameter"]
                buy_sell_signal+=mfi[j]*weights_of_individual["mfi_parameter"]
                buy_sell_signal+=(ewma[j]-sma[j]/ewma[j])*weights_of_individual["ma_parameter"]
                buy_sell_signal+=((bbands["MiddleBand"].iloc[j]-bbands["Close"].iloc[j])/(bbands["UpperBand"].iloc[j]-bbands["LowerBand"].iloc[j]))*weights_of_individual["bbands_parameter"]
                if(buy_sell_signal>abs(weights_of_individual["trade_threshold"])):
                    if(individual_portfolio["remaining_capital"]>=(individual_portfolio["starting_capital"]*weights_of_individual["capital_percentage"])):
                        trade_units=(individual_portfolio["starting_capital"]*weights_of_individual["capital_percentage"]*buy_sell_signal)//(bbands["Close"].iloc[j])
                        individual_portfolio["remaining_capital"]-=trade_units*bbands["Close"].iloc[j]
                        individual_portfolio["number_of_stock"]+=trade_units
                if(buy_sell_signal<abs(weights_of_individual["trade_threshold"])*(-1)):
                    if(individual_portfolio["number_of_stock"]>0):
                        trade_units=(individual_portfolio["starting_capital"]*weights_of_individual["capital_percentage"]*abs(buy_sell_signal))//(bbands["Close"].iloc[j])
                        if(individual_portfolio["number_of_stock"]>=trade_units):
                            individual_portfolio["number_of_stock"]-=trade_units
                            individual_portfolio["remaining_capital"]+=trade_units*bbands["Close"].iloc[j]
                        else:
                            individual_portfolio["remaining_capital"]+=individual_portfolio["number_of_stock"]*bbands["Close"].iloc[j]
                            individual_portfolio["number_of_stock"]=0
            final_result_of_individual=(((individual_portfolio["remaining_capital"]+individual_portfolio["number_of_stock"]*bbands["Close"].iloc[-1])-1000)/200)+1000
            result_of_game.append(final_result_of_individual)
        return result_of_game
    
    def find_best(list_of_population,result_of_game):
        maximum=max(result_of_game)
        for i in range(len(result_of_game)):
            if(result_of_game[i]==maximum):
                return list_of_population[i]
        return list_of_population[0]

    def update_weights(new_weights,):
        file = open("weights.txt","w")
        l=[str(new_weights["rsi_parameter"])+"\n",str(new_weights["mfi_parameter"])+"\n",str(new_weights["ma_parameter"])+"\n",str(new_weights["bbands_parameter"])+"\n",str(new_weights["capital_percentage"])+"\n",str(new_weights["trade_threshold"])+"\n"]
        file.writelines(l)
        file.close()

    weights=fetch_weights()
    list_of_population=populate(weights)
    result_of_game=play_game(list_of_population,rsi,mfi,bbands,sma,ewma)
    new_weights=find_best(list_of_population,result_of_game)
    update_weights(new_weights)
    # file = open("logs.txt","a")
    print("result=",max(result_of_game),new_weights["rsi_parameter"],new_weights["mfi_parameter"],new_weights["ma_parameter"],new_weights["bbands_parameter"],new_weights["capital_percentage"],new_weights["trade_threshold"],"lr=",learning_rate)
    # l=["\n ",str(i)," thgen"," result= ",str(max(result_of_game))," ",str(new_weights["rsi_parameter"])," ",str(new_weights["mfi_parameter"])," ",str(new_weights["ma_parameter"])," ",str(new_weights["bbands_parameter"])," ",str(new_weights["capital_percentage"])," ",str(new_weights["trade_threshold"])]
    # file.writelines(l)
    # file.close()
# the below commented code can restart the training of the genetic algorithm
# file = open("weights.txt","w")
# l=["0\n","0\n","0\n","0\n","0\n","0\n"]
# file.writelines(l)
# file.close()
start_date = dt.datetime.today()- dt.timedelta(3000) 
end_date = dt.datetime.today()
stock ="USDINR=X"
data = yf.download(stock, start_date, end_date)
learning_rate=1
# print(data["Open"].iloc[0])
print(len(data))
rsi=RSI(data)
mfi=MFI(data)
bbands=BBANDS(data)
ma=MA(data)
sma=ma[0]
ewma=ma[1]
print("RSI")
print(len(rsi))
print("MFI")
print(len(mfi))
print("BBANDS")
print(len(bbands))
print("MA")
print(len(sma))
print(len(ewma))
smallest_length_data=len(ewma)
rsi=rsi[len(rsi)-len(ewma):]
mfi=mfi[len(mfi)-len(ewma):]
bbands=bbands[len(bbands)-len(ewma):]
sma=sma[len(sma)-len(ewma):]
print("RSI")
print(len(rsi))
print("MFI")
print(len(mfi))
print("BBANDS")
print(len(bbands))
print("MA")
print(len(sma))
print(len(ewma))
for i in range(5000):
    print(i,end=" ")
    generation(rsi,mfi,bbands,sma,ewma,learning_rate)
    learning_rate=learning_rate*1
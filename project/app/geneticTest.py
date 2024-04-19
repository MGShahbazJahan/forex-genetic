import yfinance as yf
import datetime as dt
import random
from collections import defaultdict 
import math
from app.indicator import MFI, RSI, MA, BBANDS

def fetch_weights():
        file = open("weights.txt", "r")
        lst=list(file.readlines())
        dictionary=defaultdict()
        print(lst)
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
    
    def fetch_weights():
        file = open("weights.txt", "r")
        lst=list(file.readlines())
        dictionary=defaultdict()
        print(lst)
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
    
    def play_game(best_individual,rsi,mfi,bbands,sma,ewma):
        result_of_game=[]
        status_portfolio=defaultdict()

        weights_of_individual=best_individual
        individual_portfolio=defaultdict()
        individual_portfolio["remaining_capital"]=weights_of_individual["starting_capital"]
        individual_portfolio["starting_capital"]=weights_of_individual["starting_capital"]
        individual_portfolio["number_of_stock"]=0
        status_portfolio["current_capital"]=[]
        status_portfolio["number_of_stock"]=[]
        status_portfolio["current_stock_price"]=[]
        status_portfolio["total_value"]=[]
        status_portfolio["buy_sell_signal"]=[]
        status_portfolio["buy_sell_signalresult"]=[]


        for j in range(len(rsi)):
            buy_sell_signal=rsi[j]*weights_of_individual["rsi_parameter"]
            buy_sell_signal+=mfi[j]*weights_of_individual["mfi_parameter"]
            buy_sell_signal+=(ewma[j]-sma[j]/ewma[j])*weights_of_individual["ma_parameter"]
            buy_sell_signal+=((bbands["MiddleBand"].iloc[j]-bbands["Close"].iloc[j])/(bbands["UpperBand"].iloc[j]-bbands["LowerBand"].iloc[j]))*weights_of_individual["bbands_parameter"]
            if(buy_sell_signal>abs(weights_of_individual["trade_threshold"])):
                if(individual_portfolio["remaining_capital"]>=abs(individual_portfolio["starting_capital"]*weights_of_individual["capital_percentage"])):
                    trade_units=abs(individual_portfolio["starting_capital"]*weights_of_individual["capital_percentage"]*buy_sell_signal)//(bbands["Close"].iloc[j])
                    individual_portfolio["remaining_capital"]-=trade_units*bbands["Close"].iloc[j]
                    individual_portfolio["number_of_stock"]+=trade_units
            if(buy_sell_signal<abs(weights_of_individual["trade_threshold"])*(-1)):
                if(individual_portfolio["number_of_stock"]>0 and individual_portfolio["remaining_capital"]>=0):
                    trade_units=abs(individual_portfolio["starting_capital"]*weights_of_individual["capital_percentage"]*buy_sell_signal)//(bbands["Close"].iloc[j])
                    if(individual_portfolio["number_of_stock"]-trade_units>=0 and trade_units >=0):
                        individual_portfolio["number_of_stock"]-=trade_units
                        individual_portfolio["remaining_capital"]+=trade_units*bbands["Close"].iloc[j]
                    elif(trade_units >=0):
                        individual_portfolio["remaining_capital"]+=individual_portfolio["number_of_stock"]*bbands["Close"].iloc[j]
                        individual_portfolio["number_of_stock"]=0
            
            status_portfolio["buy_sell_signal"].append(math.log2(buy_sell_signal))

            status_portfolio["current_capital"].append(individual_portfolio["remaining_capital"])
            status_portfolio["number_of_stock"].append(individual_portfolio["number_of_stock"])
            status_portfolio["current_stock_price"].append(bbands["MiddleBand"].iloc[j])
            status_portfolio["total_value"].append(1000+(individual_portfolio["remaining_capital"]+(bbands["MiddleBand"].iloc[j]*individual_portfolio["number_of_stock"]))/500)
        final_result_of_individual=max(0,(((individual_portfolio["remaining_capital"]+individual_portfolio["number_of_stock"]*bbands["Close"].iloc[-1]))/500))+1000
        result_of_game=final_result_of_individual
        print("result=",result_of_game,weights["rsi_parameter"],weights["mfi_parameter"],weights["ma_parameter"],weights["bbands_parameter"],weights["capital_percentage"],weights["trade_threshold"],"lr=",learning_rate)
        return status_portfolio
    
    weights=fetch_weights()
    # list_of_population=populate(weights)
    status_portfolio=play_game(weights,rsi,mfi,bbands,sma,ewma)
    print(len(status_portfolio["total_value"]))
    return status_portfolio
    


def genetic_test(cex):
    start_date = dt.datetime.today()- dt.timedelta(1100)
    end_date = dt.datetime.today()
    data = yf.download(cex, start_date, end_date)
    # print("this is data")
    # print(data)
    learning_rate=1
    # print(data["Open"].iloc[0])
    # print(len(data))
    rsi=RSI(data)
    mfi=MFI(data)
    bbands=BBANDS(data)
    ma=MA(data)
    sma=ma[0]
    ewma=ma[1]
    # print("RSI")
    # print(len(rsi))
    # print("MFI")
    # print(len(mfi))
    # print("BBANDS")
    # print(len(bbands))
    # print("MA")
    # print(len(sma))
    # print(len(ewma))
    smallest_length_data=len(ewma)
    rsi=rsi[len(rsi)-len(ewma):]
    mfi=mfi[len(mfi)-len(ewma):]
    bbands=bbands[len(bbands)-len(ewma):]
    sma=sma[len(sma)-len(ewma):]
    # print("RSI")
    # print(len(rsi))
    # print("MFI")
    # print(len(mfi))
    # print("BBANDS")
    # print(len(bbands))
    # print("MA")
    # print(len(sma))
    # print(len(ewma))
    status_portfolio = generation(rsi,mfi,bbands,sma,ewma,learning_rate)
    return status_portfolio
cex="EURJPY=X"
genetic_test(cex)
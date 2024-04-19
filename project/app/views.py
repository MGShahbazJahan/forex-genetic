from django.shortcuts import render
import datetime as dt 
import yfinance as yf
import plotly.express as px
from app import ml
from app.geneticTest import genetic_test
from app.trainingResults import get_training_results
import statistics
import  json

# Create your views here.
def home(request):
    return render(request,"index.html")

def getdata(request):
    if(request.method=='POST'):
        print("CEX = ",request.POST.get('cex'))
        if request.POST.get('cex'):
            cex=request.POST.get('cex')
            # start_date = dt.datetime.today()- dt.timedelta(5) 
            # end_date = dt.datetime.today()
            # stock ="USDJPY=X"
            # data = yf.download(stock, start_date, end_date)
            # print("downloaded")
            # print(type(data))
            # print(data)
            Indicators=ml.indicators(cex)
            PRICE=Indicators[0]
            SMA=Indicators[1]
            EWMA=Indicators[2]
            RSI=Indicators[3]
            BBANDSLOWER=Indicators[4]
            BBANDSUPPER=Indicators[5]
            BBANDSMIDDLE=Indicators[0]
            MFI=Indicators[6]
            xyear=[x.year for x in list(SMA.keys())]
            xmonth=[x.month for x in list(SMA.keys())]
            xday=[x.day for x in list(SMA.keys())]
            status_portfolio=genetic_test(cex)
            portfolio_value = status_portfolio["total_value"]
            buy_sell_signal = status_portfolio["buy_sell_signal"]
            buy_sell_signal_average=statistics.mean(buy_sell_signal)
            buy_sell_signal=[(x-buy_sell_signal_average)*2 for x in buy_sell_signal]
            true_positive=0
            true_negative=0
            false_positive=0
            false_negative=0
            for i in range(1,len(buy_sell_signal)):
                if(buy_sell_signal[i]>0 and BBANDSMIDDLE[i]-BBANDSMIDDLE[i-1]>0):
                    true_positive+=1
                if(buy_sell_signal[i]<0 and BBANDSMIDDLE[i]-BBANDSMIDDLE[i-1]<0):
                    true_negative+=1
                if(buy_sell_signal[i]<0 and BBANDSMIDDLE[i]-BBANDSMIDDLE[i-1]>0):
                    false_negative+=1
                if(buy_sell_signal[i]>0 and BBANDSMIDDLE[i]-BBANDSMIDDLE[i-1]<0):
                    false_positive+=1
            print(true_positive,false_positive,false_negative,true_negative)
            print("bbands length",len(BBANDSMIDDLE))
            print("buy sell signal",len(buy_sell_signal))
            print("buy sell signal",len(SMA))

            buy_sell_signal_latest=round(buy_sell_signal[-1],3)
            dictionary=get_training_results()
            training_generation=dictionary["generation"]
            training_results=dictionary["result"]
            # print(training_results)
            training_rsi=dictionary["rsi_parameter"]
            training_msi=dictionary["mfi_parameter"]
            training_ma=dictionary["ma_parameter"]
            training_bbands=dictionary["bbands_parameter"]
            cexnice=cex[0:3:]+"-"+cex[3:6:]
            # print(portfolio_value)
            # print(xyear)
            # print(xmonth)
            # print(xday)
            # context={"x":[x.timestamp() for x in list(SMA.keys())],"y":list(SMA),}
            context={
                "buysellsignallatest":buy_sell_signal_latest,
                "yportfoliovalue":portfolio_value,
                "cex":cex,
                "cexnice":cexnice,
                "xday":xday,
                "xmonth":xmonth,
                "xyear":xyear,
                "yprice":list(PRICE),
                "ysma":list(SMA),
                "yewma":list(EWMA),
                "yrsi":list(RSI),
                "ybbandslower":list(BBANDSLOWER),
                "ybbandsupper":list(BBANDSUPPER),
                "ymfi":list(MFI),
                "traininggeneration":training_generation,
                "trainingresult":training_results,
                "trainingrsi":training_rsi,
                "trainingmsi":training_msi,
                "trainingma":training_ma,
                "trainingbbands":training_bbands
                }

            # fig=px.line(
            #     x=list(SMA.keys()),
            #     y=list(SMA),
            #     title='lol',
            # )
            # chart=fig.to_html()
            # context={"chart":chart}
            # print(dir(context["x"][0]))
            # print("done")
            # print(chart)
            return render(request,"chart.html",{'json_data': context})
        else:
            return render(request,"error.html")
    
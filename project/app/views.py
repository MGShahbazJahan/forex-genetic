from django.shortcuts import render
import datetime as dt 
import yfinance as yf
import plotly.express as px
from app import ml
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
            BBANDSMIDDLE=Indicators[5]
            BBANDSUPPER=Indicators[6]
            MFI=Indicators[7]
            xyear=[x.year for x in list(SMA.keys())]
            xmonth=[x.month for x in list(SMA.keys())]
            xday=[x.day for x in list(SMA.keys())]
            # print(xyear)
            # print(xmonth)
            # print(xday)
            # context={"x":[x.timestamp() for x in list(SMA.keys())],"y":list(SMA),}
            context={"cex":cex,"xday":xday,"xmonth":xmonth,"xyear":xyear,"yprice":list(PRICE),"ysma":list(SMA),"yewma":list(EWMA),"yrsi":list(RSI),"ybbandslower":list(BBANDSLOWER),"ybbandsmiddle":list(BBANDSMIDDLE),"ybbandsupper":list(BBANDSUPPER),"ymfi":list(MFI),"cex":cex}

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
    
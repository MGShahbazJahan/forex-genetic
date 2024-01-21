from django.shortcuts import render
import datetime as dt 
import yfinance as yf
import plotly.express as px
from app import ml

# Create your views here.
def home(request):
    return render(request,"index.html")

def getdata(request):
    if(request.method=='POST'):
        print(request.POST.get('cex'))
        if request.POST.get('cex'):

            cex=request.POST.get('cex')
            # start_date = dt.datetime.today()- dt.timedelta(5) 
            # end_date = dt.datetime.today()
            # stock ="USDJPY=X"
            # data = yf.download(stock, start_date, end_date)
            # print("downloaded")
            # print(type(data))
            # print(data)
            SMA=ml.MA(cex)
            print(SMA.keys(),type(SMA),len(SMA))
            context={"date":list(SMA.keys()),"values":list(SMA)}
            fig=px.line(
                x=list(SMA.keys()),
                y=list(SMA),
                title='lol',
            )
            chart=fig.to_html()
            context={"chart":chart}
            return render(request,"chart.html",context)
        else:
            return render(request,"error.html")
    
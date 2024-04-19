import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np




def indicators(cex):
    def downloaddata(cex):
        start_date = dt.datetime.today()- dt.timedelta(1100) 
        end_date = dt.datetime.today()
        data = yf.download(cex, start_date, end_date)
        return data

    # Calculate money flow index
    def MFI(data, n=14):
        high=data['High']
        low=data['Low']
        close=data['Close']
        tr = np.amax(np.vstack(((high - low).to_numpy(), (abs(high - close)).to_numpy(), (abs(low - close)).to_numpy())).T, axis=1)
        return pd.Series(tr).rolling(n).mean().to_numpy()


    def RSI(data, periods = 14):
        close=data['Close']
        close_delta = close.diff()

        # Make two series: one for lower closes and one for higher closes
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)
        
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()

        rsi = ma_up / ma_down
        rsi = 100 - (100/(1 + rsi))
        return rsi


    # Compute the Bollinger Bands 
    def BBANDS(data, ndays=20):
        MA = data['Close'].rolling(window=ndays).mean()
        SD = data['Close'].rolling(window=ndays).std()
        bbands=dict()
        bbands['MiddleBand'] = MA
        bbands['UpperBand'] = MA + (2 * SD) 
        bbands['LowerBand'] = MA - (2 * SD)
        return bbands


    # Simple Moving Average 
    def SMA(data, ndays=20): 
        # Compute the 50-day SMA        
        SMA = pd.Series(data['Close'].ewm(span = ndays, min_periods = ndays - 1).mean(), 
                    name = 'SMA_' + str(ndays)) 
        SMA = data.join(SMA) 
        SMA = SMA.dropna()
        SMA = SMA['SMA_'+ str(ndays)]
        return SMA

    # Exponentially-weighted Moving Average 
    def EMA(data, ndays=200): 
        # Compute the 200-day EWMA
        
        EMA = pd.Series(data['Close'].ewm(span = ndays, min_periods = ndays - 1).mean(), 
                    name = 'EWMA_' + str(ndays)) 
        EMA = data.join(EMA) 
        EMA = EMA.dropna()
        EMA = EMA['EWMA_' + str(ndays)]
        return EMA
    

    data=downloaddata(cex)
    print(len(data))
    rsi=RSI(data)
    mfi=MFI(data)
    bbands=BBANDS(data)
    sma=SMA(data)
    ewma=EMA(data)
    # close=data['Close']
    smallest_length_data=len(ewma)
    rsi=rsi[len(rsi)-len(ewma):]
    mfi=mfi[len(mfi)-len(ewma):]
    bbands['MiddleBand']=bbands['MiddleBand'][len(bbands['MiddleBand'])-len(ewma):]
    bbands['LowerBand']=bbands['LowerBand'][len(bbands['LowerBand'])-len(ewma):]
    bbands['UpperBand']=bbands['UpperBand'][len(bbands['UpperBand'])-len(ewma):]
    # print(bbands['UpperBand'])
    sma=sma[len(sma)-len(ewma):]
    print("RSI")
    print(len(rsi))
    # print(rsi)
    print("MFI")
    print(len(mfi))
    # print(mfi)
    print("BBANDS")
    print(len(bbands['MiddleBand']))
    print(len(bbands['LowerBand']))
    print(len(bbands['UpperBand']))
    # print(bbands)
    print("MA")
    print(len(sma))
    # print(sma)
    print(len(ewma))
    # print(ewma)
    return [bbands['MiddleBand'],sma,ewma,rsi,bbands['LowerBand'],bbands['UpperBand'],mfi]
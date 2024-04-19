import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np



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
def BBANDS(data, n=50):
    MA = data.Close.rolling(window=n).mean()
    SD = data.Close.rolling(window=n).std()
    data['MiddleBand'] = MA
    data['UpperBand'] = MA + (2 * SD) 
    data['LowerBand'] = MA - (2 * SD)
    return data


def MA(data,n=50):
    # Simple Moving Average 
    def SMA(data, ndays): 
        SMA = pd.Series(data['Close'].rolling(ndays).mean(), name = 'SMA') 
        data = data.join(SMA) 
        return data

    # Exponentially-weighted Moving Average 
    def EWMA(data, ndays): 
        EMA = pd.Series(data['Close'].ewm(span = ndays, min_periods = ndays - 1).mean(), 
                    name = 'EWMA_' + str(ndays)) 
        data = data.join(EMA) 
        return data    

    # Compute the 50-day SMA
    SMA = SMA(data,n)
    SMA = SMA.dropna()
    SMA = SMA['SMA']

    # Compute the 200-day EWMA
    ew = 200
    EWMA = EWMA(data,ew)
    EWMA = EWMA.dropna()
    EWMA = EWMA['EWMA_200']
    return SMA,EWMA

start_date = dt.datetime.today()- dt.timedelta(1100) 
end_date = dt.datetime.today()
stock ="USDJPY=X"
data = yf.download(stock, start_date, end_date)
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
# print(rsi)
print("MFI")
print(len(mfi))
# print(mfi)
print("BBANDS")
print(len(bbands))
# print(bbands)
print("MA")
print(len(sma))
# print(sma)
print(len(ewma))
# print(ewma)

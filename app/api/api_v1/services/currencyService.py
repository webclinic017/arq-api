import requests
import json
import yfinance as yf
from datetime import datetime, date, timedelta

class CurrencyService:


    #get complete timeseries
    @classmethod
    def getTimeSeriesFX(cls, ticker = "EURUSD=X", interval = "1d" ,start = None, end = None):
        if interval.upper() not in ['1H', '4H', '1D']:
            interval = "1h" 
        if start is not None:
            start = datetime.strptime(start, '%Y-%m-%d')
        if end is not None:
            end = datetime.strptime(end, '%Y-%m-%d')
        #check hour input
        if interval.upper() == '1H':   
            if end is None:
                end = datetime.today()
            if start is None:
                start = datetime.today() - timedelta(days=729)         
            if start <= datetime.today() - timedelta(days=729):     
                start = datetime.today() - timedelta(days=729)
                if start > end:
                    end = datetime.today()                      
        #check day input       
        elif interval.upper() == '1D':
            firstDate = datetime.strptime('2010-1-1', '%Y-%m-%d') 
            if end is None:
                 end = datetime.today() - timedelta(days=1)
            if start is None:
                start = firstDate 
            if start <= firstDate:
                start = firstDate  
                if start > end:
                    end = datetime.today() - timedelta(days=1)               
        return yf.Ticker(ticker).history(start=start, end=end, interval=interval)




    @classmethod
    def getLastFX(cls, ticker = "EURUSD=X", interval = "1d" ,start = None, end = None):
        df = cls.getTimeSeriesFX(ticker, interval, start, end)
        lastOpen = round(df.iloc[-1, 0], 6)       
        lastClose = round(df.iloc[-1, 3], 6)
        lo = lastOpen if lastOpen < 1000 else round(lastOpen, 2)
        lc = lastClose if lastClose < 1000 else round(lastClose, 2)
        return(lo, lc)
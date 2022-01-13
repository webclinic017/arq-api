import requests
import json
from ..services.currencyService import CurrencyService
from ..services.pipeline import Pipeline
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get(ticker = "EURUSD=X", interval = "1h" ,start = None, end = None):
    results = {} 
    results[ticker] =  Pipeline().run_model(ticker, interval, start, end)
    results['interval'] = interval
    return results

@router.get("/all")
def get_all(interval = "1h" ,start = None, end = None): 
    tickers = ["EURUSD=X", "JPYUSD=X", "BTC-USD"]
    results = {}
    for i in tickers:
        results[i] =  Pipeline().run_model(i, interval, start, end)
    results['interval'] = interval
    return results
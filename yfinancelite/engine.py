from .utils import _calc_time, _parse_quotes, _parse_events
from joblib import Parallel, delayed
import requests
import pandas as pd
import json


QUERY_URL = "https://query2.finance.yahoo.com"
SCRAPE_URL = "https://finance.yahoo.com/quote/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def _download_historical_data(ticker, start = None, end = None, events = False):
    """Downlads historical data optionally events as well.

    Args:
        ticker ([string]): Ticker symbol.
        start ([string], optional): Should be YYYY-MM-DD format. Defaults to None (i.e maximum period of time).
        end ([string], optional): Should be YYYY-MM-DD format. Defaults to None (i.e maximum period of time).
        events (bool, optional): Whether include events. Defaults to False.

    Returns:
        [pd.DataFrame, pd.DataFrame]: Return with events.
        [pd.DataFrame]: Return without events.
    """
    start, end = _calc_time(start, end)
    params = {"period1": start, "period2": end}
    params['interval'] = '1d'
    if events: 
        params["events"] = "div,splits"
    
    url = "{}/v8/finance/chart/{}".format(QUERY_URL, ticker)
    response = requests.get(url=url, params=params, headers=HEADERS)
    
    data = response.json()
    events = _parse_events(data['chart']['result'][0]) if events else None
    df = _parse_quotes(data["chart"]["result"][0])

    if events:
        return df, events
    else:
        return df

def _download_summary_store(ticker):
    """Download whole information about ticker.

    Args:
        ticker ([string]): Ticker symbol.

    Returns:
        [dict]: Information about ticker.
    """
    url = SCRAPE_URL + ticker
    response = requests.request('GET', url=url, headers=HEADERS).text
    json_str = response.split('root.App.main =')[1].split(
            '(this)')[0].split(';\n}')[0].strip()
    data = json.loads(json_str)['context']['dispatcher']['stores']['QuoteSummaryStore']
    return data

def download_batch(tickers, start = None, end = None):
    batch = Parallel(n_jobs=-1, backend='threading')(
        delayed(_download_historical_data)(ticker, start=start, end=end, events=False) for ticker in tickers)
    df = {ticker.upper(): batch[i] for i, ticker in enumerate(tickers)}
    df = pd.concat(df.values(), axis=1, keys=df.keys())
    return df

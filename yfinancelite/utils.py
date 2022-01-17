import pandas as pd
import datetime
import time

def _parse_quotes(data):
    """Parse quotes from raw data.

    Args:
        data ([dict]): Raw data

    Returns:
        [pd.DataFrame]: Contains parsed quotes.
    """
    timestamps = data["timestamp"]
    ohlc = data["indicators"]["quote"][0]
    volumes = ohlc["volume"]
    opens = ohlc["open"]
    closes = ohlc["close"]
    lows = ohlc["low"]
    highs = ohlc["high"]

    adjclose = closes
    if "adjclose" in data["indicators"]:
        adjclose = data["indicators"]["adjclose"][0]["adjclose"]

    quotes = pd.DataFrame({"Open": opens,
                            "High": highs,
                            "Low": lows,
                            "Close": closes,
                            "Adj Close": adjclose,
                            "Volume": volumes})

    quotes.index = pd.to_datetime(timestamps, unit="s")
    quotes.sort_index(inplace=True)
    quotes.index = pd.to_datetime(quotes.index.date)
    quotes.index.name = "Date"
    return quotes

def _parse_events(data):
    """Parse splits and dividends from raw data.

    Args:
        data ([dict]): Raw data that contains actions.

    Returns:
        [dict]: {'dividends' : [pd.Dataframe], 'splits': [pd.DataFrame]}
    """
    if "events" not in data:
        dividends = pd.DataFrame(columns=['dividends'])
        splits = pd.DataFrame(
            columns=["numerator", "denominator", "splitRatio"])
        return {'dividends': dividends, 'splits': splits}
    
    if 'dividends' in data['events']:
        dividends = pd.DataFrame(
            data=list(data["events"]["dividends"].values()))
        dividends.set_index("date", inplace=True)
        dividends.index = pd.to_datetime(dividends.index, unit="s")
        dividends.sort_index(inplace=True)
        dividends.columns = ["Dividends"]
        dividends.index = pd.to_datetime(dividends.index.date)
    else:
        dividends = pd.DataFrame(columns=['dividends'])
        
    if 'splits' in data['events']:
        splits = pd.DataFrame(
            data=list(data["events"]["splits"].values()))
        splits.set_index("date", inplace=True)
        splits.index = pd.to_datetime(splits.index, unit="s")
        splits.index = pd.to_datetime(splits.index.date)
        splits.sort_index(inplace=True)
    else:
        splits = pd.DataFrame(
            columns=["numerator", "denominator", "splitRatio"])
        
    return {'dividends': dividends, 'splits': splits}

def _calc_time(start = None, end = None):
    """Converts time & date to milliseconds

    Args:
        start ([string], optional): Should be YYYY-MM-DD format. Defaults to None.
        end ([string], optional): Should be YYYY-MM-DD format. Defaults to None.

    Returns:
        [int, int]: Dates in milliseconds format.
    """
    if start is None:
        start = -631159200
    elif isinstance(start, datetime.datetime):
        start = int(time.mktime(start.timetuple()))
    else:
        start = int(time.mktime(
            time.strptime(str(start), '%Y-%m-%d')))
    if end is None:
        end = int(time.time())
    elif isinstance(end, datetime.datetime):
        end = int(time.mktime(end.timetuple()))
    else:
        end = int(time.mktime(time.strptime(str(end), '%Y-%m-%d')))
    return start, end

def _convert_earnings(data):
    """Formats raw earnings data.

    Args:
        data ([dict]): Raw data.

    Returns:
        [dict]: Formatted data.
    """
    data['earningsChart']['earningsDate'] = [date['fmt'] for date in data['earningsChart']['earningsDate']]
    if data['earningsChart']['quarterly'] != []:
        df_earnings = pd.DataFrame(data['earningsChart']['quarterly'])
        df_earnings['actual'] = df_earnings['actual'].apply(lambda x: x['raw'])
        df_earnings['estimate'] = df_earnings['estimate'].apply(lambda x: x['raw'])
        df_earnings.set_index('date', inplace=True)
        try:
            data['earningsChart']['currentQuarterEstimate'] = data['earningsChart']['currentQuarterEstimate']['raw']
        except:
            pass
        data['earningsChart']['quarterly'] = df_earnings
    
    if data['financialsChart']['yearly'] != []:
        yearly_financials = pd.DataFrame(data['financialsChart']['yearly'])
        yearly_financials['revenue'] = yearly_financials['revenue'].apply(lambda x: x['raw'])
        yearly_financials['earnings'] = yearly_financials['earnings'].apply(lambda x: x['raw'])
        yearly_financials.set_index('date', inplace=True)
    
    if data['financialsChart']['quarterly'] != []:
        quarterly_financials = pd.DataFrame(data['financialsChart']['quarterly'])
        quarterly_financials['revenue'] = quarterly_financials['revenue'].apply(lambda x: x['raw'])
        quarterly_financials['earnings'] =quarterly_financials['earnings'].apply(lambda x: x['raw'])
        quarterly_financials.set_index('date', inplace=True)
    
    
    data['financialsChart']['yearly'] = yearly_financials
    data['financialsChart']['quarterly'] = quarterly_financials

    return data

def _format_dict(data):
    """Formats raw data.

    Args:
        data ([dict]): Raw data.

    Returns:
        [dict]: Formatted data.
    """
    return {key:value['raw'] if type(value) == dict and value != {} else value for key, value in data.items()}
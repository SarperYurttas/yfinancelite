from .engine import _download_historical_data, _download_summary_store
from .utils import _convert_earnings, _format_dict


class Ticker:
    def __init__(self, ticker) -> None:
        self.ticker = ticker.upper()
        self._full_summary = _download_summary_store(self.ticker)
        self.history = 'call get_history() method first'
        self.events = 'call get_history(events=True) method first'
        self.statistics = _format_dict(self._full_summary['defaultKeyStatistics'])
        self.price_detail = _format_dict(self._full_summary['price'])
        self.summary_detail = _format_dict(self._full_summary['summaryDetail'])
        self.financials = _format_dict(self._full_summary['financialData'])
        self.earnings = _convert_earnings(self._full_summary['earnings'])

    def get_history(self, start=None, end=None, events=False):
        """Get history.

        Args:
            start ([string], optional): Should be YYYY-MM-DD format. Defaults to None (i.e maximum period of time).
            end ([string], optional): Should be YYYY-MM-DD format. Defaults to None (i.e maximum period of time).

        Returns:
            [type]: Detail history of ticker.
        """
        if events:    
            self.history, self.events = _download_historical_data(
                self.ticker, start, end, events)
        else:
            self.history = _download_historical_data(
                self.ticker, start, end)
        return self.history

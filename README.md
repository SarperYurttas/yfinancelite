# Yahoo! Finance Lite
This is the lightweight version of [yfinance](https://github.com/ranaroussi/yfinance). I've developed this for myself, because the original version was seemed slow. This version contains only fundamental and raw information about stocks which found on Yahoo. Therefore runs way faster than the original repo. The data that you access via this repo, is belowed to Yahoo! Inc. and so you must look at the [Yahoo APIs Terms of Use](https://policies.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.htm) before using the data.

## Quick Start
```python
import yfinancelite as yfl

ticker = yfl.Ticker('AAPL')

#When you initialized the Ticker class these information is downloaded automatically with just one request to an endpoint.
ticker.statistics
ticker.price_detail
ticker.summary_detail
ticker.financials
ticker.earnings

#In order to access this features you should call get_history() method.
ticker.history
ticker.events
```

### Legal Disclaimer
As developer, we are not responsible for any legal issue about the using proprietary data. It's intended for research and educational purposes.

class TickerData:
    """
        Main Ticker data API facade. Primarily two function one to get a data range 
        for reading historical data and another to subscribe to live data. 
        Class uses 'data providers' which can be switched out to use different data sources.
    """
    def __init__(self, default_provider):
        self.default_provider = default_provider
    
    def get_data(self, start_time, end_time, provider=None):
        if provider is None:
            provider = self.default_provider
        return provider.get_data(start_time, end_time)

    def subscribe_to_live_data(self, event_handler, provider=None):
        if provider is None:
            provider = self.default_provider
        provider.subscribe_to_live_data(event_handler)

from eod import EodHistoricalData
from pubsub import pub

class EodDataProvider:
    """
        @TODO
    """
    def __init__(self, symbol, timerange, api_key):
        self.api_key = api_key
        self.symbol = symbol
    
    def get_data(self, start_time, end_time):
        #EOD Imlpementation
        pass;

    def subscribe_to_live_data(self, event_handler):
        #EOD Imlpementation
        pass;
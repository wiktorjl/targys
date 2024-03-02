
import pandas as pd;
from pubsub import pub

class CsvDataProvider:
    def __init__(self, symbol, path='./datafiles', stream_start_time=None):
        self.path = path
        self.df = pd.read_csv(self.path + '/' + symbol + '.US.csv')
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df = self.df.set_index('Date')
        self.stream_start_time = stream_start_time

    def get_data(self, start_time, end_time):
        return pd.DataFrame(self.df.loc[start_time:end_time])
    
    def subscribe_to_live_data(self, event_handler):
        pub.subscribe(event_handler, 'live.tick')
        for index, row in self.df.iterrows():
            if self.stream_start_time and index >= self.stream_start_time:
                pub.sendMessage('live.tick', data=row)
import pandas as pd
import numpy as np
from ..services.currencyService import CurrencyService
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, mean_squared_error

class Pipeline:
    
    @classmethod
    def run_model(cls, ticker = "EURUSD=X", interval = "1d" ,start = None, end = None, model = None):
        df = cls.get_data(ticker, interval, start , end)
        if model is None:
            df = cls.prepare_features(df)
            lags = 5
            cols = []
            features = ['dir', 'sma_s', 'sma_m', 'sma_l', 'boll', 'min', 'max', 'mean_return', 'volatility']
            for f in features:
                for lag in range(1, lags +1):
                    col = f'{f}_lag{lag}'
                    df[col] = df[f].shift(lag)
                    cols.append(col)
            df.dropna(inplace = True)
            results = cls.runmodel(df)
            return results
        return {'Error':'unknown'}



            
    def get_data(ticker = "EURUSD=X", interval = "1d" ,start = None, end = None):
        df = CurrencyService().getTimeSeriesFX(ticker, interval, start, end)
        df.index.name='Date'
        df = df[['Open', 'High', 'Low', 'Close']]
        for column in df.columns:
            df[column] = pd.to_numeric(df[column], errors = 'coerce')
        df['returns'] = np.log(df.Close / df.Close.shift(1))
        df.dropna(inplace = True)
        return df

    def prepare_features(df):
        window_s = 9
        window = 50
        window_l = 100
        df['dir'] = np.where(df['returns'] > 0, 1, 0)
        df['sma_s'] = df['Close'].rolling(window_s).mean() - df['Close'].rolling(window_s).std()
        df['sma_m'] = df['Close'].rolling(window).mean() - df['Close'].rolling(window).std()
        df['sma_l'] = df['Close'].rolling(window_l).mean() - df['Close'].rolling(window_l).std()
        df['boll'] = (df['Close'] - df['Close'].rolling(window).mean()) / df['Close'].rolling(window).std()
        df['min'] = df['Close'].rolling(window).min() / df['Close'] - 1
        df['max'] = df['Close'].rolling(window).max() / df['Close'] - 1
        df['mean_return'] = df['returns'].rolling(3).mean()
        df['volatility'] = df['returns'].rolling(window).std()    
        df.dropna(inplace = True)
        return df

    def runmodel(df):
        x = df.drop(['dir', 'returns'], axis = 1).values
        y = df.iloc[:, 5].values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 0)
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)
        classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
        classifier.fit(x_train, y_train)
        y_pred = classifier.predict(x_test)
        ac = accuracy_score(y_test, y_pred)
        pred = classifier.predict(x[[-1]])
        return {'accuracy': str(ac), 'prediction': str(pred[0])}
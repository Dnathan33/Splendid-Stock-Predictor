#LOADING DATASET AND DEFINING TARGET VARIABLE
import requests
import pandas as pd
import numpy as np
import io
import json
from bson import json_util, objectid

def predict(url):

    #plot within the notebook
    # import matplotlib.pyplot as plt

    #setting figure size
    from matplotlib.pylab import rcParams
    rcParams['figure.figsize'] = 20,10

    #for normalizing data
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range = (0,1))

    #read the file
    # response = "https://www.quandl.com/api/v3/datasets/EOD/MSFT.csv?api_key=7HyimRss6EqW7ZhRyUkR"
    response = url
    urlData = requests.get(response).content
    df = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
    #print the head
    print(df.head())

    #setting index as date
    df['Date'] = pd.to_datetime(df.Date, format = '%Y-%m-%d')
    df.index = df['Date']

    #plot
    # plt.figure(figsize=(16,8))
    # plt.plot(df['Close'], label = 'Close Price History')

    #IMPLEMENTING LONG SHORT TERM MEMORY (LSTM)
    #importing required libraries
    from sklearn.preprocessing import MinMaxScaler
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, LSTM

    #creating dataframe
    data = df.sort_index(ascending = True, axis = 0)
    new_data = pd.DataFrame(index = range(0, len(df)), columns = ['Date', 'Close'])
    for i in range(0, len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data['Close'][i] = data['Close'][i]
    print(len(new_data))
    #setting index
    new_data.index = new_data.Date
    new_data.drop('Date', axis = 1, inplace = True)

    #creating train and test sets
    dataset = new_data.values
    train = dataset[0:1000, :]
    valid = dataset[1000:, :]

    #converting dataset into x_train and y_train
    scaler = MinMaxScaler(feature_range = (0,1))
    scaled_data = scaler.fit_transform(dataset)
    x_train, y_train = [], []
    for i in range(60, len(train)):
        x_train.append(scaled_data[i-60:i,0])
        y_train.append(scaled_data[i,0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

    #create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(units = 50, return_sequences = True,
                   input_shape = (x_train.shape[1],1)))
    model.add(LSTM(units = 50))
    model.add(Dense(1))
    model.compile(loss = 'mean_squared_error', optimizer = 'adam')
    model.fit(x_train, y_train, epochs = 1, batch_size = 1, verbose = 2)

    #predicting 246 values, using past 60 from the train data
    inputs = new_data[len(new_data) - len(valid) - 60:].values
    inputs = inputs.reshape(-1,1)
    inputs = scaler.transform(inputs)
    X_test = []
    for i in range(60, inputs.shape[0]):
        X_test.append(inputs[i-60:i,0])

    X_test = np.array(X_test)
    print(X_test.shape[0])
    print(X_test.shape[1])
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1],1))
    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)

    #RESULTS(about 40 second runtime)
    rms = np.sqrt(np.mean(np.power((valid-closing_price), 2)))
    rms

    #plotting
    train = new_data[:1000]
    valid = new_data[1000:]
    valid['Predictions'] = closing_price
    # plt.plot(train['Close'])
    # plt.plot(valid[['Close', 'Predictions']])
    # plt.show()
    return df


def get_data(url):
    valid = predict(url)
    record = json.loads(valid.T.to_json()).values()
    return record


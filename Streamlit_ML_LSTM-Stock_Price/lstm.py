import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn import utils
from keras.layers import Input, LSTM, Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
import tensorflow as tf
import joblib
import investpy
import datetime


def make_model(stock, from_date):
    tf.set_random_seed(777)
    # 과거 데이터 가져오기 
    # from_date = str(from_date)
    # from_date = from_date.replace("-", ".")
    # from_date = from_date.split()
    # from_date = from_date.reverse()
    from_date = from_date.strftime("%d-%m-%Y")
    from_date = from_date.replace("-", "/")

    now = datetime.datetime.now()
    now = now.strftime("%d-%m-%Y")
    now = str(now).replace("-", "/")

    df = investpy.get_stock_historical_data(stock=stock,
                                        country='South Korea',
    									from_date=from_date,
    									to_date=now)
    # test, train set 나누기
    df = df[['Open', 'High', 'Low', 'Close']]
    data = df.values
    train = data[:(len(data) - int(len(data)*0.3))]
    test = data[:int(len(data)*0.3)]

    transformer = MinMaxScaler()
    train = transformer.fit_transform(train)
    test = transformer.transform(test)

    sequence_length = 7
    window_length = sequence_length + 1

    x_train = []
    y_train = []
    for i in range(0, len(train) - window_length + 1):
        window = train[i:i + window_length, :]
        x_train.append(window[:-1, :])
        y_train.append(window[-1, [-1]])
    x_train = np.array(x_train)
    y_train = np.array(y_train)

    x_test = []
    y_test = []
    for i in range(0, len(test) - window_length + 1):
        window = test[i:i + window_length, :]
        x_test.append(window[:-1, :])
        y_test.append(window[-1, [-1]])
    x_test = np.array(x_test)
    y_test = np.array(y_test)

    utils.shuffle(x_train, y_train)

    joblib.dump(transformer, 'models/'+ str(stock) +'_model_transformer.pkl')

    input = Input(shape=(sequence_length, 4))
    net = LSTM(units=512)(input) 
    net = Dense(units=512, activation='relu')(net)
    net = Dense(units=1)(net)
    model = Model(inputs=input, outputs=net)

    model.summary()


    model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.01))
    model.fit(x_train, y_train, epochs=30, validation_data=(x_test, y_test), 
        callbacks=[ModelCheckpoint(filepath='models/'+ str(stock) +'_model.h5', save_best_only=True, verbose=1)]) 

##########모델 예측

    y_test_inverse = []
    for y in y_test:
        inverse = transformer.inverse_transform([[0, 0, 0, y[0]]])
        y_inverse = inverse.flatten()[-1]
        print(y_inverse)
        y_test_inverse.append(y_inverse)

    y_predict = model.predict(x_test)
    y_predict_inverse = []

    for y in y_predict:
        inverse = transformer.inverse_transform([[0, 0, 0, y[0]]])
        y_inverse = inverse.flatten()[-1]
        print(y_inverse)
        y_predict_inverse.append(y_inverse)


    value = data[-7:]
    price_list = [
                [value[0,0], value[0,1], value[0,2], value[0,3]],
                [value[1,0], value[1,1], value[1,2], value[1,3]],
                [value[2,0], value[2,1], value[2,2], value[2,3]],
                [value[3,0], value[3,1], value[3,2], value[3,3]],
                [value[4,0], value[4,1], value[4,2], value[4,3]],
                [value[5,0], value[5,1], value[5,2], value[5,3]],
                [value[6,0], value[6,1], value[6,2], value[6,3]]
            ]
    
    x_test = transformer.transform(price_list)

    x_test = x_test.reshape((1, 7, 4))

    y_predict = model.predict(x_test)


    inverse = transformer.inverse_transform([[0, 0, 0, y_predict.flatten()[0]]])

    return inverse.flatten()[-1]


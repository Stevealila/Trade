
def train_and_save_(steps, X_train, y_train, save_filepath, n_neurons=50, batch_size=32, epochs=20):
    from tensorflow.keras.models import Sequential # type: ignore
    from tensorflow.keras.layers import Input, Dense, LSTM # type: ignore
    from tensorflow.keras.optimizers import Adam # type: ignore
    from tensorflow.keras.metrics import MeanSquaredError # type: ignore

    model = Sequential()

    model.add(Input(shape=(steps, 1)))
    model.add(LSTM(n_neurons, return_sequences=True))
    model.add(LSTM(n_neurons))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.001), metrics=[MeanSquaredError()])
    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=0);
    model.save(save_filepath)

    return model
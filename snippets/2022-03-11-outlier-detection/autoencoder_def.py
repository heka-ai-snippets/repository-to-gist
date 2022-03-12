input_shape = X_train.shape[1]
input_layer = Input(shape = (input_shape,))
hid_layer1 = Dense(6, activation = 'relu', name = 'hid_layer1')(input_layer)
hid_layer2 = Dense(3, activation = 'relu', name = 'hid_layer2')(hid_layer1)
hid_layer3 = Dense(6, activation = 'relu', name = 'hid_layer3')(hid_layer2)
output_layer = Dense(input_shape)(hid_layer3)
model = Model(input = input_layer, output = output_layer)

model.compile(optimizer = 'sgd', loss = 'mean_squared_error')
model.fit(x = X_train, y = X_train, batch_size = 64,
        epochs = 1000, validation_data = [X_test, X_test])
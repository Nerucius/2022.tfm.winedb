# autoencoder_0.0636.h5
data_dim = df_style.shape[1]
encoding_dim = 6
my_regularizer = regularizers.l1(10e-8)


# Autoencoder model
input_layer = Input(shape=(data_dim, ))
encoded = Dense(encoding_dim, activation='relu', activity_regularizer=my_regularizer)(input_layer)
decoded = Dense(data_dim, activation='sigmoid')(encoded)
autoencoder = Model(input_layer, decoded)

# ENCODER
encoder = Model(input_layer, encoded)

# DECODER
# create a placeholder for an encoded (32-dimensional) input
encoded_input = Input(shape=(encoding_dim,))
# retrieve the last layer of the autoencoder model
decoder_layer = autoencoder.layers[-1]
# create the decoder model
decoder = Model(encoded_input, decoder_layer(encoded_input))

es = EarlyStopping(monitor="val_loss", patience=50, verbose=1, mode="min")

# Train to reconstruct Styles
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
autoencoder.fit(x_train, x_train, epochs=2500, batch_size=96, shuffle=True, validation_data=(x_test, x_test),
                 verbose=1, callbacks=[es,])
                 


# 


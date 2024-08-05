import streamlit as st
# import os
# os.environ["KERAS_BACKEND"] = "tensorflow"
from keras.datasets import fashion_mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Input, Flatten
from keras.utils import set_random_seed
from keras.backend import clear_session

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
labels = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
X_train = X_train / 255
X_test = X_test / 255
y_train_ohe = to_categorical(y_train, num_classes=10)
y_test_ohe = to_categorical(y_test, num_classes=10)
clear_session()
set_random_seed(42)
model = Sequential()
model.add(Input(shape=X_train.shape[1:]))
model.add(Flatten())
model.add(Dense(10, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.summary()

with st.spinner('Training'):
	history = model.fit(X_train, y_train_ohe, epochs = 1, verbose=0)

st.info('Model trained')
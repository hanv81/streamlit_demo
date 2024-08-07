import cv2
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import fashion_mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Input, Flatten
from keras.utils import set_random_seed
from keras.backend import clear_session
from keras.models import load_model

st.title('MNIST-Fashion Classification')

tab1, tab2 = st.tabs(['Train', 'Inference'])
with tab1:
	col1, col2 = st.columns(2)
	with col1:
		(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
		fig, axs = plt.subplots(10, 10)
		for i in range(10):
			ids = np.random.choice(np.where(y_train == i)[0], 10, replace=False)
			for j in range(10):
				axs[i][j].axis('off')
				axs[i][j].imshow(X_train[ids[j]], cmap='gray')
		st.text('Dataset')
		st.pyplot(fig)
	with col2:
		epochs = st.number_input('Epochs', value=10, min_value=1)
		if st.button('Train', use_container_width=True):
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
			with st.spinner('Training'):
				history = model.fit(X_train, y_train_ohe, epochs=epochs, verbose=0)
				_, accuracy = model.evaluate(X_test, y_test_ohe)
				st.info(f'Model trained, Test accuracy: {accuracy:.4f}')
				model.save('model.keras')
with tab2:
	uploaded_file = st.file_uploader('Upload Image File', type=['png', 'jpg', 'jpeg'])
	if uploaded_file is not None:
		col1, col2 = st.columns(2)
		bytes_data = uploaded_file.getvalue()
		img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
		with col1:
			st.image(img)
		
		img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		img = cv2.resize(img, dsize=(28,28))
		img = 255 - img
		img = img/255
		img = img.reshape(1,28,28)

		model = load_model('model.keras')
		if model is not None:
			labels = np.array(['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'])
			prop = np.around(model.predict(img)[0]*100, decimals=2)
			ids = np.argsort(prop)[-3:][::-1]
			with col2:
				st.subheader('Prediction')
				for i in ids:
					st.write(labels[i], prop[i], '%')
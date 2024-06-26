from sklearn.cluster import KMeans
from PIL import Image
import streamlit as st
import numpy as np
import requests


st.title('Image Segmentation with kMeans')
col1, col2 = st.columns(2)
with col1:
	url = st.text_input('Image URL (Press Enter to apply)')
with col2:
	k = st.slider('K', min_value=2, max_value=10, value=3)
if len(url) > 0:
	col3, col4 = st.columns(2)
	with col3:
		st.image(url, caption='Original Image')
	with col4:
		img = Image.open(requests.get(url, stream=True).raw)
		img = np.array(img)
		kmeans = KMeans(n_clusters=k, n_init='auto')
		kmeans.fit(img.reshape(-1, img.shape[-1]))
		centers = kmeans.cluster_centers_.astype(int)
		img_new = centers[kmeans.labels_].reshape(img.shape)
		st.image(img_new, caption='Segmented Image')

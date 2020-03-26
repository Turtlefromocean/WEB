import streamlit as st 
from PIL import Image
from classify import predict

st.title("Image Classifier ML Web")
selected_model = st.sidebar.selectbox('모델 선택', ('xception','vgg16'))

uploaded_file = st.file_uploader('이미지 업로드', type=("png", "jpg"))

if uploaded_file is not None:
	image = Image.open(uploaded_file)
	st.image(image, caption='업로드된 이미지', use_column_width=True)
	st.write("")
	st.write("분류중...")
	label = predict(uploaded_file, selected_model)
	st.success('%s (%.2f%%)' %(label[1], label[2]*100))
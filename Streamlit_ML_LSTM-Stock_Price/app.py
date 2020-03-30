import streamlit as st
from lstm import make_model

st.title("주가예측")

st.write("예측하고자 하는 주식 정보와 사용할 주가정보 기준일을 알려주세요")

stock = st.text_input("종목코드를 입력해주세요")


date = st.date_input("데이터 시작일")

if st.button("예측 시작"):
	result = make_model(stock, date)
	st.success('내일 예측주가는 %.2f 원 입니다' % result)
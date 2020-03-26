import streamlit as st

st.title("제목")
st.write("일반텍스트1")
st.text("일반텍스트2")

st.sidebar.title("사이드바제목")
st.sidebar.text("사이드바 텍스트")

a = st.sidebar.selectbox('선택해주세요', ('모델1', '모델2'))
b = st.sidebar.slider('범위를 설정해주세요', 0.0, 100.0, (25.0, 75.0))
c = st.sidebar.slider('특정값 선택', 0.0, 100.0, 50.0, 1.0)


st.write(a)
st.write(b)
st.write(c)
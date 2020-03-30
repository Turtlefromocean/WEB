import streamlit as st
from summarize import get_summary
st.title("뉴스 기사 요약기")
st.write("요약하고자 하는 글의 링크를 넣어주세요")
url = st.text_input('url 링크', value='', key=None, type='default')

ratio = st.slider('요약 분량(비율)을 정해주세요', 0.0,1.0,0.1)

if st.button("요약하기"):
    result = get_summary(url, ratio)
    st.success(result)

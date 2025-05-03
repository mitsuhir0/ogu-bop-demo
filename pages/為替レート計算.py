import streamlit as st

# 為替レート計算機
st.title("為替レート計算機")

# 初期為替レートを設定
exchange_rate = st.number_input("為替レート (1ドルあたりの円)", value=140, step=5)

# Highlight the results using Streamlit's `st.markdown` with custom styling.

st.subheader("ドルから円への変換")
dollar_input = st.number_input("ドルを入力", value=100.0, min_value=0.0, step=1.0, format="%.0f")
yen_output = dollar_input * exchange_rate
st.markdown(f"{dollar_input}ドルは約 <span style='color: green; font-weight: bold;'>{yen_output:.2f}</span> 円です。（1ドル{exchange_rate}円のとき）", unsafe_allow_html=True)

st.subheader("円からドルへの変換")
yen_input = st.number_input("円を入力",value=10000.0, min_value=0.0, step=100.0, format="%.0f")
dollar_output = yen_input / exchange_rate
st.markdown(f"{yen_input}円は約 <span style='color: blue; font-weight: bold;'>{dollar_output:.2f}</span> ドルです。（1ドル{exchange_rate}円のとき）", unsafe_allow_html=True)
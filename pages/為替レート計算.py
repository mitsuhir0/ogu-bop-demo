import streamlit as st

# 為替レート計算機
st.title("為替レート計算機（比較表示）")

# レイアウトを2カラムに分割
col1, col2 = st.columns(2)

with col1:
    st.header("為替レート計算機 1")
    st.markdown("<style>.slider-label { display: flex; justify-content: space-between; }</style>", unsafe_allow_html=True)
    st.markdown("<div class='slider-label'><span>円高</span><span>円安</span></div>", unsafe_allow_html=True)
    exchange_rate_1 = st.slider("為替レート (1ドルあたりの円)", min_value=50, max_value=200, value=140, step=1, key="slider1")

    st.subheader("ドルから円への変換")
    dollar_input_1 = st.number_input("ドルを入力", value=100.0, min_value=0.0, step=1.0, format="%.0f", key="dollar1")
    yen_output_1 = dollar_input_1 * exchange_rate_1
    st.write(f"{dollar_input_1:,.0f}ドルは約 {yen_output_1:,.0f} 円です。（1ドル{exchange_rate_1:,.0f}円のとき）")

    st.subheader("円からドルへの変換")
    yen_input_1 = st.number_input("円を入力", value=10000.0, min_value=0.0, step=100.0, format="%.0f", key="yen1")
    dollar_output_1 = yen_input_1 / exchange_rate_1
    st.write(f"{yen_input_1:,.0f}円は約 {dollar_output_1:,.0f} ドルです。（1ドル{exchange_rate_1:,.0f}円のとき）")

with col2:
    st.header("為替レート計算機 2")
    st.markdown("<style>.slider-label { display: flex; justify-content: space-between; }</style>", unsafe_allow_html=True)
    st.markdown("<div class='slider-label'><span>円高</span><span>円安</span></div>", unsafe_allow_html=True)
    exchange_rate_2 = st.slider("為替レート (1ドルあたりの円)", min_value=50, max_value=200, value=140, step=1, key="slider2")

    st.subheader("ドルから円への変換")
    dollar_input_2 = st.number_input("ドルを入力", value=100.0, min_value=0.0, step=1.0, format="%.0f", key="dollar2")
    yen_output_2 = dollar_input_2 * exchange_rate_2
    st.write(f"{dollar_input_2:,.0f}ドルは約 {yen_output_2:,.0f} 円です。（1ドル{exchange_rate_2:,.0f}円のとき）")

    st.subheader("円からドルへの変換")
    yen_input_2 = st.number_input("円を入力", value=10000.0, min_value=0.0, step=100.0, format="%.0f", key="yen2")
    dollar_output_2 = yen_input_2 / exchange_rate_2
    st.write(f"{yen_input_2:,.0f}円は約 {dollar_output_2:,.0f} ドルです。（1ドル{exchange_rate_2:,.0f}円のとき）")

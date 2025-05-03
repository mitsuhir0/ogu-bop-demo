import streamlit as st

# タイトル
st.title("輸出価格設定シミュレーター")

# 初期値の設定
initial_exchange_rate = 150  # 初期為替レート (1ドル=150円)
car_price_jpy = 1500000  # 日本車の価格 (150万円)
initial_export_price_usd = car_price_jpy / initial_exchange_rate  # 初期輸出ドル価格

# ユーザー入力
new_exchange_rate = st.number_input("新しい為替レート (1ドル=円):", min_value=1.0, value=150.0, step=10.0)

# 価格戦略の選択肢を追加
strategy = st.radio("価格戦略を選択してください:", ("転嫁率を手動で設定", "売上単価を上げる", "日本円売上単価を維持しながらドル建て価格を引き下げる"))

# 売上単価を最大化する転嫁率を計算
if strategy == "売上単価を上げる":
    optimal_pass_through_rate = min(100, max(0, (new_exchange_rate / initial_exchange_rate - 1) * 100))
    pass_through_rate = st.slider("為替変化の転嫁率 (%):", min_value=0, max_value=100, value=int(optimal_pass_through_rate), step=1)
# 日本円売上単価を維持するための転嫁率を計算
elif strategy == "日本円売上単価を維持しながらドル建て価格を引き下げる":
    target_pass_through_rate = (car_price_jpy / (new_exchange_rate * initial_export_price_usd) - 1) * 100
    pass_through_rate = st.slider("為替変化の転嫁率 (%):", min_value=-100, max_value=100, value=int(target_pass_through_rate), step=1)
else:
    pass_through_rate = st.slider("為替変化の転嫁率 (%):", min_value=0, max_value=100, value=50, step=1)

# 計算
exchange_rate_change = new_exchange_rate - initial_exchange_rate
adjusted_export_price_usd = initial_export_price_usd * (1 + (new_exchange_rate - initial_exchange_rate) / initial_exchange_rate * pass_through_rate / 100)
adjusted_revenue_jpy = adjusted_export_price_usd * new_exchange_rate

# 売上単価最大化のための転嫁率を表示
if strategy == "売上単価を上げる":
    st.write(f"売上単価を最大化する転嫁率: {optimal_pass_through_rate:.2f}%")

# 売上単価維持のための転嫁率を表示
if strategy == "日本円売上単価を維持しながらドル建て価格を引き下げる":
    st.write(f"日本円売上単価を維持する転嫁率: {target_pass_through_rate:.2f}%")

# 2カラム構成に戻す
st.write("### 結果")
col1, col2 = st.columns(2)

with col1:
    st.write("#### 初期値")
    st.write(f"為替レート: {initial_exchange_rate} 円/USD")
    st.write(f"輸出ドル価格: {initial_export_price_usd:.2f} USD")
    st.write(f"日本円売上単価: {car_price_jpy} 円")

with col2:
    st.write("#### 新しい値")
    st.write(f"為替レート: {new_exchange_rate:.0f} 円/USD")
    st.write(f"輸出ドル価格: {adjusted_export_price_usd:.2f} USD")
    st.write(f"日本円売上単価: {adjusted_revenue_jpy:.0f} 円")
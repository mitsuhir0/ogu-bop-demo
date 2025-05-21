import streamlit as st

st.title("ビッグマック指数による購買力平価（PPP）デモ")

st.write("""
2国間のビッグマックの価格と為替レートを入力してください。ビッグマック指数に基づく理論為替レートと実際の為替レートを比較します。
""")

col1, col2 = st.columns(2)

with col1:
    price_domestic = st.number_input("自国のビッグマック価格（例: 450）", min_value=0.0, value=480.0)
    currency_domestic = st.text_input("自国通貨名", value="JPY")
with col2:
    price_foreign = st.number_input("外国のビッグマック価格（例: 5.0）", min_value=0.0, value=5.8)
    currency_foreign = st.text_input("外国通貨名", value="USD")

actual_rate = st.number_input(f"現在の為替レート（1 {currency_foreign} = ? {currency_domestic}）", min_value=0.0, value=150.0)

if price_foreign > 0:
    ppp_rate = price_domestic / price_foreign
    converted_foreign_price = price_foreign * actual_rate
    st.subheader("計算結果")
    st.write(f"**ビッグマック指数による理論為替レートの計算式：**")
    st.latex(r'''
    \text{理論為替レート} = \frac{\text{自国のビッグマック価格}}{\text{外国のビッグマック価格}}
    ''')
    st.write(f"ビッグマック指数による理論為替レート: **1 {currency_foreign} = {ppp_rate:.2f} {currency_domestic}**")
    st.write(f"実際の為替レート: **1 {currency_foreign} = {actual_rate:.2f} {currency_domestic}**")
    st.write(f"外国のビッグマック価格（{price_foreign:.2f} {currency_foreign}）を日本円に換算: **{converted_foreign_price:.2f} {currency_domestic}**")
    diff = actual_rate - ppp_rate
    if ppp_rate > 0:
        diff_percent = (diff / ppp_rate) * 100
    else:
        diff_percent = 0
    if diff > 0:
        st.success(
            f"{currency_domestic}は理論値より**{diff_percent:.2f}%安い**です\n\n"
            f"（購買力平価: {ppp_rate:.2f}、実際の為替レート: {actual_rate:.2f}）"
        )
        if currency_domestic == "JPY":
            st.info(
                "【解説】\n"
                "現在の為替レートでは日本円（JPY）は購買力平価（PPP）に比べて割安、つまり過小評価されていると考えられます。\n"
                "この場合、同じ商品（ビッグマック）を買うのに日本では他国よりも安く済むことを意味します。\n"
                "この状況は、輸出には有利（日本製品が海外で安くなる）ですが、輸入や海外旅行には不利（海外の商品やサービスが高く感じられる）となります。\n"
            )
    elif diff < 0:
        st.warning(
            f"{currency_domestic}は理論値より**{abs(diff_percent):.2f}%高い**です\n\n"
            f"（購買力平価: {ppp_rate:.2f}、実際の為替レート: {actual_rate:.2f}）"
        )
    else:
        st.info("理論値と実際の為替レートは一致しています。")
else:
    st.error("外国のビッグマック価格は0より大きい値を入力してください。")

st.markdown("""
---
**注意：**
- ビッグマック指数は購買力平価を直感的に理解するための指標であり、実際の為替レートや経済状況を正確に反映するものではありません。
- 裁定取引による利益は、輸送コストや関税、消費者の嗜好、各国の規制などの影響で現実的には困難です。
- ビッグマックは同じ商品名でも、国ごとに大きさ・調理法・原材料・コスト構造が異なるため、単純な価格比較には限界があります。


## References

- [BigMacIndex\.jp \| ビッグマック指数で世界の物価を日本と比較](https://www.bigmacindex.jp/)
- [ビッグマック指数とは？最新の日本の順位や世界各国の数値を紹介 \| 東証マネ部！](https://money-bu-jpx.com/news/article056848/)
""")
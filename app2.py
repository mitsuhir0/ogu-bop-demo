import streamlit as st

st.title("弾力性計算機（価格・交差・所得・マーシャル・ラーナー条件）")

st.markdown("""
機能一覧：
- 価格弾力性
- 交差価格弾力性
- 所得弾力性
- マーシャル・ラーナー条件の検証
""")

st.subheader("価格弾力性の式")
st.latex(r"E_d = \frac{\Delta Q / Q}{\Delta P / P}")

st.subheader("マーシャル・ラーナー条件")
st.latex(r"|E_x| + |E_m| > 1")
st.markdown("ここで、$E_x$：輸出の価格弾力性、$E_m$：輸入の価格弾力性")

elasticity_type = st.selectbox(
    "計算する項目を選んでください",
    ("価格弾力性", "交差価格弾力性", "所得弾力性", "マーシャル・ラーナー条件")
)

# 共通数量入力
q1 = st.number_input("元の数量（Q1）", value=100.0)
q2 = st.number_input("新しい数量（Q2）", value=120.0)

if elasticity_type == "価格弾力性":
    p1 = st.number_input("元の価格（P1）", value=100.0)
    p2 = st.number_input("新しい価格（P2）", value=80.0)
    if p1 == 0 or q1 == 0 or (p2 - p1) == 0:
        st.error("計算できません：Q1, P1 は 0 ではなく、価格の変化が必要です。")
    else:
        ed = ((q2 - q1) / q1) / ((p2 - p1) / p1)
        st.subheader(f"価格弾力性: {ed:.2f}")
        if abs(ed) > 1:
            st.success("弾力的")
        elif abs(ed) == 1:
            st.info("単位弾力的")
        else:
            st.warning("非弾力的")

elif elasticity_type == "交差価格弾力性":
    p1_other = st.number_input("他商品の元の価格（P1′）", value=100.0)
    p2_other = st.number_input("他商品の新しい価格（P2′）", value=110.0)
    if p1_other == 0 or q1 == 0 or (p2_other - p1_other) == 0:
        st.error("計算できません：Q1, P1′ は 0 ではなく、価格の変化が必要です。")
    else:
        ec = ((q2 - q1) / q1) / ((p2_other - p1_other) / p1_other)
        st.subheader(f"交差価格弾力性: {ec:.2f}")

elif elasticity_type == "所得弾力性":
    y1 = st.number_input("元の所得（Y1）", value=50000.0)
    y2 = st.number_input("新しい所得（Y2）", value=60000.0)
    if y1 == 0 or q1 == 0 or (y2 - y1) == 0:
        st.error("計算できません：Q1, Y1 は 0 ではなく、所得の変化が必要です。")
    else:
        ey = ((q2 - q1) / q1) / ((y2 - y1) / y1)
        st.subheader(f"所得弾力性: {ey:.2f}")

elif elasticity_type == "マーシャル・ラーナー条件":
    st.markdown("以下に輸出と輸入の価格弾力性を入力してください。")
    ex = st.number_input("輸出の価格弾力性（Ex）", value=-1.2)
    em = st.number_input("輸入の価格弾力性（Em）", value=-0.5)
    total_elasticity = abs(ex) + abs(em)
    st.subheader(f"|Ex| + |Em| = {total_elasticity:.2f}")
    if total_elasticity > 1:
        st.success("マーシャル・ラーナー条件は満たされています（経常収支は改善可能）")
    else:
        st.error("マーシャル・ラーナー条件は満たされていません（経常収支の改善は難しい可能性）")



import streamlit as st

st.title("弾力性計算機（価格・交差・所得・マーシャル・ラーナー条件）")

st.markdown("""
機能一覧：
- 価格弾力性
- 交差価格弾力性
- 所得弾力性
- マーシャル・ラーナー条件の検証
""")

# 計算する項目を選択
elasticity_type = st.selectbox(
    "計算する項目を選んでください",
    ("価格弾力性", "交差価格弾力性", "所得弾力性", "マーシャル・ラーナー条件")
)

# 選択に応じて式や解説を表示
if elasticity_type == "価格弾力性":
    st.subheader("価格弾力性の式")
    st.latex(r"E_d = \frac{\Delta Q / Q}{\Delta P / P}")
    q1 = st.number_input("元の数量（Q1）", value=100.0)
    q2 = st.number_input("新しい数量（Q2）", value=120.0)
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
        st.markdown("""
        **価格弾力性の解説**:
        - 価格弾力性が1より大きい場合、需要は価格に対して敏感（弾力的）です。
        - 価格弾力性が1より小さい場合、需要は価格に対して鈍感（非弾力的）です。
        """)

elif elasticity_type == "交差価格弾力性":
    st.subheader("交差価格弾力性の式")
    st.latex(r"E_c = \frac{\Delta Q / Q}{\Delta P' / P'}")
    q1 = st.number_input("元の数量（Q1）", value=100.0)
    q2 = st.number_input("新しい数量（Q2）", value=120.0)
    p1_other = st.number_input("他商品の元の価格（P1′）", value=100.0)
    p2_other = st.number_input("他商品の新しい価格（P2′）", value=110.0)
    if p1_other == 0 or q1 == 0 or (p2_other - p1_other) == 0:
        st.error("計算できません：Q1, P1′ は 0 ではなく、価格の変化が必要です。")
    else:
        ec = ((q2 - q1) / q1) / ((p2_other - p1_other) / p1_other)
        st.subheader(f"交差価格弾力性: {ec:.2f}")
        st.markdown("""
        **交差価格弾力性の解説**:
        - 正の値の場合、2つの商品は代替関係にあります。
        - 負の値の場合、2つの商品は補完関係にあります。
        """)

elif elasticity_type == "所得弾力性":
    st.subheader("所得弾力性の式")
    st.latex(r"E_y = \frac{\Delta Q / Q}{\Delta Y / Y}")
    q1 = st.number_input("元の数量（Q1）", value=100.0)
    q2 = st.number_input("新しい数量（Q2）", value=120.0)
    y1 = st.number_input("元の所得（Y1）", value=50000.0)
    y2 = st.number_input("新しい所得（Y2）", value=60000.0)
    if y1 == 0 or q1 == 0 or (y2 - y1) == 0:
        st.error("計算できません：Q1, Y1 は 0 ではなく、所得の変化が必要です。")
    else:
        ey = ((q2 - q1) / q1) / ((y2 - y1) / y1)
        st.subheader(f"所得弾力性: {ey:.2f}")
        st.markdown("""
        **所得弾力性の解説**:
        - 正の値の場合、商品は正常財です。
        - 負の値の場合、商品は劣等財です。
        """)

elif elasticity_type == "マーシャル・ラーナー条件":
    st.subheader("マーシャル・ラーナー条件")
    st.latex(r"|E_x| + |E_m| > 1")
    st.markdown("ここで、$E_x$：輸出の価格弾力性、$E_m$：輸入の価格弾力性")
    ex = st.number_input("輸出の価格弾力性（Ex）", value=-1.2)
    em = st.number_input("輸入の価格弾力性（Em）", value=-0.5)
    total_elasticity = abs(ex) + abs(em)
    st.subheader(f"|Ex| + |Em| = {total_elasticity:.2f}")
    if total_elasticity > 1:
        st.success("マーシャル・ラーナー条件は満たされています（経常収支は改善可能）")
    else:
        st.error("マーシャル・ラーナー条件は満たされていません（経常収支の改善は難しい可能性）")
    st.markdown("""
    **マーシャル・ラーナー条件の解説**:
    - この条件が満たされる場合、為替レートの変化が経常収支を改善する可能性があります。
    """)



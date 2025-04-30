"""
This Streamlit application provides a calculator for various types of elasticity 
and the Marshall-Lerner condition. Users can select the type of calculation 
they want to perform and input the required parameters to compute the results.

Features:
1. **Price Elasticity of Demand**:
    - Formula: E_d = |(ΔQ / Q1) / (ΔP / P1)|
    - Calculates the responsiveness of quantity demanded to price changes.
    - Provides intermediate calculations and interpretation of results 
      (elastic, unit elastic, inelastic).

2. **Cross-Price Elasticity of Demand**:
    - Formula: E_c = (ΔQ / Q1) / (ΔP' / P1')
    - Measures the responsiveness of the quantity demanded of one good to 
      the price change of another good.
    - Indicates whether goods are substitutes (positive value) or complements 
      (negative value).

3. **Income Elasticity of Demand**:
    - Formula: E_y = (ΔQ / Q1) / (ΔY / Y1)
    - Evaluates how the quantity demanded changes with income changes.
    - Identifies goods as normal (positive value) or inferior (negative value).

4. **Marshall-Lerner Condition**:
    - Formula: E_x + E_m > 1
    - Assesses whether a currency depreciation will improve the current account balance.
    - Requires user input for export and import elasticities to determine if the 
      condition is satisfied.

Inputs:
- Quantities (Q1, Q2)
- Prices (P1, P2, P1', P2')
- Income levels (Y1, Y2)
- Export and import elasticities (Ex, Em)

Outputs:
- Intermediate calculations for better understanding.
- Final elasticity values with interpretations.
- Error handling for invalid inputs (e.g., zero values or no change in variables).

Usage:
- Select the type of elasticity or condition to calculate.
- Input the required parameters.
- View the results, intermediate steps, and explanations.
"""
import streamlit as st
st.title("弾力性計算機")


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
        delta_q = q2 - q1
        delta_p = p2 - p1
        percentage_change_q = delta_q / q1
        percentage_change_p = delta_p / p1
        ed = abs(percentage_change_q / percentage_change_p)  # 絶対値を取ることでプラス表記

        # 途中式と結果を表示
        st.markdown(f"""
        **途中計算**:
        - 数量の変化: ΔQ = Q2 - Q1 = {q2} - {q1} = {delta_q}
        - 価格の変化: ΔP = P2 - P1 = {p2} - {p1} = {delta_p}
        - 数量の変化率: ΔQ / Q1 = {delta_q} / {q1} = {percentage_change_q:.2f}
        - 価格の変化率: ΔP / P1 = {delta_p} / {p1} = {percentage_change_p:.2f}
        - 価格弾力性: E_d = |(ΔQ / Q1) / (ΔP / P1)| = |{percentage_change_q:.2f} / {percentage_change_p:.2f}| = {ed:.2f}
        """)

        st.subheader(f"価格弾力性: {ed:.2f}")
        if ed > 1:
            st.success("弾力的")
        elif ed == 1:
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
        delta_q = q2 - q1
        delta_p_other = p2_other - p1_other
        percentage_change_q = delta_q / q1
        percentage_change_p_other = delta_p_other / p1_other
        ec = percentage_change_q / percentage_change_p_other

        # 途中式と結果を表示
        st.markdown(f"""
        **途中計算**:
        - 数量の変化: ΔQ = Q2 - Q1 = {q2} - {q1} = {delta_q}
        - 他商品の価格の変化: ΔP' = P2' - P1' = {p2_other} - {p1_other} = {delta_p_other}
        - 数量の変化率: ΔQ / Q1 = {delta_q} / {q1} = {percentage_change_q:.2f}
        - 他商品の価格変化率: ΔP' / P1' = {delta_p_other} / {p1_other} = {percentage_change_p_other:.2f}
        - 交差価格弾力性: E_c = (ΔQ / Q1) / (ΔP' / P1') = {percentage_change_q:.2f} / {percentage_change_p_other:.2f} = {ec:.2f}
        """)

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
        delta_q = q2 - q1
        delta_y = y2 - y1
        percentage_change_q = delta_q / q1
        percentage_change_y = delta_y / y1
        ey = percentage_change_q / percentage_change_y

        # 途中式と結果を表示
        st.markdown(f"""
        **途中計算**:
        - 数量の変化: ΔQ = Q2 - Q1 = {q2} - {q1} = {delta_q}
        - 所得の変化: ΔY = Y2 - Y1 = {y2} - {y1} = {delta_y}
        - 数量の変化率: ΔQ / Q1 = {delta_q} / {q1} = {percentage_change_q:.2f}
        - 所得の変化率: ΔY / Y1 = {delta_y} / {y1} = {percentage_change_y:.2f}
        - 所得弾力性: E_y = (ΔQ / Q1) / (ΔY / Y1) = {percentage_change_q:.2f} / {percentage_change_y:.2f} = {ey:.2f}
        """)

        st.subheader(f"所得弾力性: {ey:.2f}")
        st.markdown("""
        **所得弾力性の解説**:
        - 正の値の場合、商品は正常財です。
        - 負の値の場合、商品は劣等財です。
        """)

elif elasticity_type == "マーシャル・ラーナー条件":
    st.subheader("マーシャル・ラーナー条件")
    st.latex(r"E_x + E_m > 1")
    st.markdown("""
    **マーシャル・ラーナー条件の説明**:
    - この条件が満たされる場合、為替レートの変化（例えば、自国通貨の減価）が経常収支を改善する可能性があります。
    """)

    # ユーザー入力
    ex = st.number_input("為替レート変化に対する輸出量の弾力性（Ex）", value=1.2)
    em = st.number_input("為替レート変化に対する輸入量の弾力性（Em）", value=0.8)

    # 弾力性の合計を計算
    total_elasticity = ex + em

    # 結果表示
    st.subheader(f"計算結果: Ex + Em = {ex:.2f} + {em:.2f} = {total_elasticity:.2f}")
    if total_elasticity > 1:
        st.success("マーシャル・ラーナー条件は満たされています（経常収支は改善可能です）")
    else:
        st.error("マーシャル・ラーナー条件は満たされていません（経常収支の改善は難しい可能性があります）")

    # 解説
    st.markdown("""
    **解説**:
    - **為替レート変化に対する輸出量の弾力性（Ex）**: 為替レートが減価した際に輸出量がどれだけ増加するかを示します。
    - **為替レート変化に対する輸入量の弾力性（Em）**: 為替レートが減価した際に輸入量がどれだけ減少するかを示します。
    - **条件の意味**: 自国通貨が減価した場合、輸出が増加し、輸入が減少することで経常収支が改善する可能性があります。ただし、これが成立するためには、Ex + Em > 1 である必要があります。
    """)

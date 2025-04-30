import streamlit as st
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import numpy as np
import matplotlib_fontja

st.set_page_config(page_title="国際収支デモ", layout="wide")
st.title("\U0001F4B0 国際収支・複式簿記体験アプリ")
st.markdown("""
このアプリでは、取引を入力すると国際収支の複式簿記がどのように記録されるかを体験できます。
国際収支は「経常収支」と「金融収支」に大きく分けられ、複式簿記の原則により借方と貸方が常に一致します。
""")


# ヘルプ情報の展開可能セクション
with st.expander("国際収支の基本知識"):
    st.markdown("""
    ### 経常収支の主な項目
    1. **貿易収支** - 財（商品）の輸出入
    2. **サービス収支** - サービスの輸出入（観光、運輸、特許使用料など）
    3. **第一次所得収支** - 投資収益、労働者の賃金など
    4. **第二次所得収支** - 援助、寄付金、仕送りなど
    
    ### 金融収支の主な項目
    1. **直接投資** - 外国企業への出資など
    2. **証券投資** - 外国株式・債券の売買
    3. **その他投資** - 預金、貸付金など
    4. **外貨準備** - 中央銀行の外貨資産
    
    ### 複式簿記の原則
    国際収支は必ず2つの側面から記録され、合計が一致します：
    - 財を輸出すれば、その対価として外貨資産が増加
    - 外国株式を購入すれば、その支払いとして外貨預金が減少
    
    理論上、経常収支と金融収支の合計はゼロになります。実務上の差額は「誤差脱漏」として計上されます。
    """)

# 取引の選択肢
transaction_types = {
    # 貿易収支
    "財の輸出（例：100ドル相当の自動車販売）": {
        "first_account": {"type": "経常収支", "category": "貿易収支", "position": "貸方"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "借方", "detail": "外貨預金増加"}
    },
    "財の輸入（例：50ドル相当の石油輸入）": {
        "first_account": {"type": "経常収支", "category": "貿易収支", "position": "借方"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "貸方", "detail": "外貨預金減少"}
    },
    
    # サービス収支
    "サービス輸出（例：外国人観光客の国内消費）": {
        "first_account": {"type": "経常収支", "category": "サービス収支", "position": "貸方"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "借方", "detail": "外貨預金増加"}
    },
    "サービス輸入（例：海外旅行での支出）": {
        "first_account": {"type": "経常収支", "category": "サービス収支", "position": "借方"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "貸方", "detail": "外貨預金減少"}
    },
    
    # 第一次所得収支
    "投資収益受取（例：海外投資からの配当）": {
        "first_account": {"type": "経常収支", "category": "第一次所得収支", "position": "貸方"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "借方", "detail": "外貨預金増加"}
    },
    "投資収益支払（例：外国投資家への配当）": {
        "first_account": {"type": "経常収支", "category": "第一次所得収支", "position": "借方"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "貸方", "detail": "外貨預金減少"}
    },
    
    # 第二次所得収支
    "海外からの送金受取（例：仕送り）": {
        "first_account": {"type": "経常収支", "category": "第二次所得収支", "position": "貸方"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "借方", "detail": "外貨預金増加"}
    },
    "海外への送金（例：援助や仕送り）": {
        "first_account": {"type": "経常収支", "category": "第二次所得収支", "position": "借方"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "貸方", "detail": "外貨預金減少"}
    },
    
    # 金融収支内の取引
    "外国証券購入（例：米国株式の購入）": {
        "first_account": {"type": "金融収支", "category": "証券投資", "position": "借方", "detail": "外国証券資産増加"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "貸方", "detail": "外貨預金減少"}
    },
    "外国証券売却（例：保有米国債の売却）": {
        "first_account": {"type": "金融収支", "category": "証券投資", "position": "貸方", "detail": "外国証券資産減少"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "借方", "detail": "外貨預金増加"}
    },
    "外国企業への直接投資": {
        "first_account": {"type": "金融収支", "category": "直接投資", "position": "借方", "detail": "直接投資資産増加"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "貸方", "detail": "外貨預金減少"}
    },
    "海外直接投資の売却": {
        "first_account": {"type": "金融収支", "category": "直接投資", "position": "貸方", "detail": "直接投資資産減少"},
        "second_account": {"type": "金融収支", "category": "その他投資", "position": "借方", "detail": "外貨預金増加"}
    },
}

# タブでUIを分割
tab1, tab2 = st.tabs(["取引入力", "国際収支分析"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("1. 取引の入力")
        transaction = st.selectbox("取引の種類を選んでください：", list(transaction_types.keys()))
        amount = st.number_input("金額（ドル）", min_value=1, value=100, step=1)
        memo = st.text_input("取引メモ（任意）", "")
        
        if 'records' not in st.session_state:
            st.session_state.records = []
        
        if st.button("取引を記録"):
            transaction_info = transaction_types[transaction]
            first_account = transaction_info["first_account"]
            second_account = transaction_info["second_account"]
            
            # 取引日付を追加
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # 数値型のフィールドにはfloatを使用し、空のフィールドにはnp.nanを使用
            record = {
                "日時": current_datetime,
                "取引": transaction,
                "金額": float(amount),
                "メモ": memo,
                "経常収支区分": first_account.get("category", "") if first_account["type"] == "経常収支" else (
                              second_account.get("category", "") if second_account["type"] == "経常収支" else ""),
                "経常収支（借方）": float(amount) if first_account["type"] == "経常収支" and first_account["position"] == "借方" else (
                                float(amount) if second_account["type"] == "経常収支" and second_account["position"] == "借方" else np.nan),
                "経常収支（貸方）": float(amount) if first_account["type"] == "経常収支" and first_account["position"] == "貸方" else (
                                float(amount) if second_account["type"] == "経常収支" and second_account["position"] == "貸方" else np.nan),
                "金融収支区分_借方": first_account.get("category", "") if first_account["type"] == "金融収支" and first_account["position"] == "借方" else (
                                  second_account.get("category", "") if second_account["type"] == "金融収支" and second_account["position"] == "借方" else ""),
                "金融収支区分_貸方": first_account.get("category", "") if first_account["type"] == "金融収支" and first_account["position"] == "貸方" else (
                                  second_account.get("category", "") if second_account["type"] == "金融収支" and second_account["position"] == "貸方" else ""),
                "金融収支（借方）": float(amount) if first_account["type"] == "金融収支" and first_account["position"] == "借方" else (
                                float(amount) if second_account["type"] == "金融収支" and second_account["position"] == "借方" else np.nan),
                "金融収支（貸方）": float(amount) if first_account["type"] == "金融収支" and first_account["position"] == "貸方" else (
                                float(amount) if second_account["type"] == "金融収支" and second_account["position"] == "貸方" else np.nan),
                "詳細（借方）": first_account.get("detail", "") if first_account["position"] == "借方" else second_account.get("detail", ""),
                "詳細（貸方）": first_account.get("detail", "") if first_account["position"] == "貸方" else second_account.get("detail", "")
            }
            st.session_state.records.append(record)
            st.success(f"取引が記録されました: {transaction} - {amount} ドル")
    
    with col2:
        st.subheader("取引説明")
        transaction_info = transaction_types.get(transaction, {})
        if transaction_info:
            first_account = transaction_info["first_account"]
            second_account = transaction_info["second_account"]
            
            st.markdown("### 選択中の取引")
            st.write(f"**{transaction}**")
            
            st.markdown("### 仕訳説明")
            if first_account["position"] == "借方":
                st.write(f"**借方**: {first_account['type']}（{first_account.get('category', '')}）")
                st.write(f"**貸方**: {second_account['type']}（{second_account.get('category', '')}）")
            else:
                st.write(f"**借方**: {second_account['type']}（{second_account.get('category', '')}）")
                st.write(f"**貸方**: {first_account['type']}（{first_account.get('category', '')}）")
            
            st.markdown("### 影響")
            if "経常収支" in [first_account["type"], second_account["type"]]:
                ca_effect = "増加" if (first_account["type"] == "経常収支" and first_account["position"] == "貸方") or \
                                    (second_account["type"] == "経常収支" and second_account["position"] == "貸方") else "減少"
                st.write(f"経常収支が**{ca_effect}**します")
    
    st.subheader("2. 複式簿記の記録")
    if st.session_state.records:
        display_columns = ["日時", "取引", "金額", "経常収支区分", "経常収支（借方）", "経常収支（貸方）", 
                          "金融収支区分_借方", "金融収支（借方）", "金融収支区分_貸方", "金融収支（貸方）", "メモ"]
        
        df = pd.DataFrame(st.session_state.records)
        # 集計行の追加
        total_row = {
            "日時": "",
            "取引": "合計",
            "金額": df["金額"].sum(),
            "メモ": "",
            "経常収支区分": "",
            "経常収支（借方）": df["経常収支（借方）"].sum(),
            "経常収支（貸方）": df["経常収支（貸方）"].sum(),
            "金融収支区分_借方": "",
            "金融収支区分_貸方": "",
            "金融収支（借方）": df["金融収支（借方）"].sum(),
            "金融収支（貸方）": df["金融収支（貸方）"].sum(),
            "詳細（借方）": "",
            "詳細（貸方）": ""
        }
        display_df = pd.concat([df[display_columns], pd.DataFrame([total_row])[display_columns]], ignore_index=True)
        st.dataframe(display_df, use_container_width=True)
        
        # CSVエクスポート機能
        def get_csv_download_link(df):
            """データフレームをCSVに変換してダウンロードリンクを生成する"""
            # BOMを追加してUTF-8でエンコードすることで、Excel等での文字化けを防止
            csv = df.to_csv(index=False).encode('utf-8-sig')
            b64 = base64.b64encode(csv).decode()
            filename = "国際収支記録.csv"
            href = f'<a href="data:text/csv;charset=utf-8-sig;base64,{b64}" download="{filename}">取引データをCSVダウンロード</a>'
            return href
        
        st.markdown(get_csv_download_link(df), unsafe_allow_html=True)
        
        if st.button("全ての取引を削除"):
            st.session_state.records = []
            st.experimental_rerun()
    else:
        st.info("まだ取引が記録されていません。")

with tab2:
    if not st.session_state.records:
        st.info("取引を記録すると、ここに分析結果が表示されます。")
    else:
        st.subheader("国際収支の集計と分析")
        
        df = pd.DataFrame(st.session_state.records)
        
        # 経常収支の詳細分析
        ca_credits = df["経常収支（貸方）"].fillna(0)
        ca_debits = df["経常収支（借方）"].fillna(0)
        ca_balance = ca_credits.sum() - ca_debits.sum()
        
        # 金融収支の詳細分析
        fa_credits = df["金融収支（貸方）"].fillna(0)
        fa_debits = df["金融収支（借方）"].fillna(0)
        fa_balance = fa_credits.sum() - fa_debits.sum()
        
        # 誤差脱漏計算
        statistical_discrepancy = ca_balance + fa_balance
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 国際収支の総括")
            st.markdown(f"**経常収支合計**: {ca_balance:,.2f} ドル")
            st.markdown(f"**金融収支合計**: {fa_balance:,.2f} ドル")
            st.markdown(f"**理論上の差額**: {statistical_discrepancy:,.2f} ドル")
            
            if abs(statistical_discrepancy) < 0.001:
                st.success("✅ 複式簿記が正しく機能しています（借方と貸方が一致）")
            else:
                st.warning(f"⚠️ 誤差脱漏が検出されました: {statistical_discrepancy:,.2f} ドル")
        
        with col2:
            # 経常収支の内訳
            st.markdown("### 経常収支の内訳")
            ca_categories = ["貿易収支", "サービス収支", "第一次所得収支", "第二次所得収支"]
            ca_data = {}
            
            for category in ca_categories:
                category_credits = df[df["経常収支区分"] == category]["経常収支（貸方）"].fillna(0).sum()
                category_debits = df[df["経常収支区分"] == category]["経常収支（借方）"].fillna(0).sum()
                ca_data[category] = category_credits - category_debits
            
            ca_df = pd.DataFrame(list(ca_data.items()), columns=["区分", "金額"])
            st.dataframe(ca_df, use_container_width=True)
        
        # チャート表示
        st.subheader("国際収支のビジュアル化")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # 経常収支カテゴリ別の円グラフデータ準備
            ca_categories_data = {}
            for category in ca_categories:
                category_credits = df[df["経常収支区分"] == category]["経常収支（貸方）"].fillna(0).sum()
                category_debits = df[df["経常収支区分"] == category]["経常収支（借方）"].fillna(0).sum()
                ca_categories_data[category] = abs(category_credits - category_debits)  # 絶対値を使用
            
            # 円グラフ
            if sum(ca_categories_data.values()) > 0:  # データがある場合のみ
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.pie(ca_categories_data.values(), labels=ca_categories_data.keys(), autopct='%1.1f%%')
                ax.set_title('経常収支の内訳')
                st.pyplot(fig)
            else:
                st.info("経常収支の取引データがありません")
        
        with col2:
            # 時系列データの準備
            if len(df) >= 2:
                # 時系列データを作成
                df['日時'] = pd.to_datetime(df['日時'])
                df = df.sort_values('日時')
                
                # 経常収支と金融収支の累積推移
                df['経常収支_純額'] = df["経常収支（貸方）"].fillna(0) - df["経常収支（借方）"].fillna(0)
                df['金融収支_純額'] = df["金融収支（貸方）"].fillna(0) - df["金融収支（借方）"].fillna(0)
                
                # 累積データ
                df['経常収支_累積'] = df['経常収支_純額'].cumsum()
                df['金融収支_累積'] = df['金融収支_純額'].cumsum()
                
                # 時系列グラフ
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.plot(df['日時'], df['経常収支_累積'], label='経常収支累積')
                ax.plot(df['日時'], df['金融収支_累積'], label='金融収支累積')
                ax.set_title('国際収支の累積推移')
                ax.legend()
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("時系列分析には2件以上の取引データが必要です")
        
        # 詳細な取引分析
        st.subheader("取引の詳細分析")
        st.markdown("各取引カテゴリごとの収支状況")
        
        # 取引タイプ別の集計
        transaction_summary = df.groupby('取引').agg({
            '金額': 'sum',
            '経常収支（借方）': lambda x: x.fillna(0).sum(),
            '経常収支（貸方）': lambda x: x.fillna(0).sum(),
            '金融収支（借方）': lambda x: x.fillna(0).sum(),
            '金融収支（貸方）': lambda x: x.fillna(0).sum()
        }).reset_index()
        
        transaction_summary['取引回数'] = df.groupby('取引').size().values
        transaction_summary['経常収支への影響'] = transaction_summary['経常収支（貸方）'] - transaction_summary['経常収支（借方）']
        transaction_summary['金融収支への影響'] = transaction_summary['金融収支（貸方）'] - transaction_summary['金融収支（借方）']
        
        st.dataframe(transaction_summary[['取引', '取引回数', '金額', '経常収支への影響', '金融収支への影響']], 
                    use_container_width=True)
        
        # 教育的な説明
        st.subheader("複式簿記と国際収支の理解")
        st.markdown("""
        ### 複式簿記の原則と国際収支の関係
        
        国際収支統計では複式簿記の原則により、すべての国際取引は2つの側面から記録されます：
        
        1. **経常収支** - 財・サービスの取引や所得の移転を記録
        2. **金融収支** - 資金の移動や金融資産・負債の変化を記録
        
        理論上、これらの合計はゼロになります。現実の国際収支統計では計測誤差などにより「誤差脱漏」が生じることがありますが、
        このシミュレーションでは複式簿記の原則が守られていれば差額は発生しません。
        
        ### 黒字と赤字の意味
        
        - **経常収支の黒字** = 国外から得る収入が支出より多い状態（貿易黒字など）
        - **経常収支の赤字** = 国外への支出が収入より多い状態（貿易赤字など）
        - **金融収支の黒字** = 資本の純流入（外国からの投資が国内から外国への投資を上回る）
        - **金融収支の赤字** = 資本の純流出（国内から外国への投資が外国からの投資を上回る）
        
        経常収支と金融収支は原則として互いに相殺関係にあります。例えば、経常収支が黒字の場合、その余剰資金は金融収支を通じて
        海外に投資されるか、外貨準備として蓄積されます。
        """)




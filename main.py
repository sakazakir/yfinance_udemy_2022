import yfinance as yf
import pandas as pd
import streamlit as st
import altair as alt

st.title("米国株価可視アプリ")
st.sidebar.write("""
# GAFA株価
株価可視化ツールです。以下のオプションから表示日数を指定
""")

st.sidebar.write("""
# 表示日数選択
""")
days = st.sidebar.slider("日数", 1, 50, 20)

st.write(f"""
### 過去 **{days}日間** のGAFA物価
""")

st.sidebar.write("""
# 株価の範囲指定
""")
ymin, ymax = st.sidebar.slider("範囲を指定してください", 0.0, 3500.0, (0.0, 3500.0))

tickers = {
    "apple": "AAPL",
    "facebook": "FB",
    "google": "GOOGL",
    "microsoft": "MSFT",
    "netflix": "NFLX",
    "amazon": "AMZN"
}


@st.cache
def get_datas(days, tickers):
    df = pd.DataFrame()

    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])

        hist = tkr.history(period=f"{days}d")
        # 日時のフォーマット変更
        hist.index = hist.index.strftime("%d %B %Y")
        # 行の絞り込み
        hist = hist[["Close"]]
        hist.columns = [company]
        # 転置
        hist = hist.Tgi
        hist.index.name = "Name"
        df = pd.concat([df, hist])
    return df


# 株式取得
df = get_datas(days, tickers)

companies = st.multiselect(
    "会社名を選択してください",
    list(df.index),
    ["google", "amazon", "facebook", "apple"]
)

if not companies:
    st.error("会社が選ばれていません")
else:
    data = df.loc[companies]
    # st.write("### 株価 (USD)", data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["Date"]).rename(
        columns={"value": "Stock Prices(USD)"}
    )
    chart = (
        alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
            x="Date:T",
            y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain = [ymin,ymax])),
            color="Name"
        )

    )
    st.altair_chart(chart, use_container_width=True)

# st.line_chart(df.T)

import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime, timedelta
import seaborn as sns
from tqdm import tqdm


def get_maar(ticker, days=10):
    """
    이동평균 정배열인지 확인
    """

    global ticker_dict

    df = fdr.DataReader(ticker, '2022')

    df["ma5"]=df["Close"].rolling(5).mean()
    df["ma10"]=df["Close"].rolling(10).mean()
    df["ma20"]=df["Close"].rolling(20).mean()
    df["ma60"]=df["Close"].rolling(60).mean()
    df["ma120"]=df["Close"].rolling(120).mean()

    df['maar'] = 0
    df.loc[(df["ma5"]>df["ma10"]) & (df["ma10"]>df["ma20"])
           & (df["ma20"]>df["ma60"]) & (df["ma60"]>df["ma120"]), 'maar'] = 1

    # print(df.query('maar==1'))

    if datetime.now() - timedelta(days=days) < df.query('maar==1').index.max():
        message = f'{ticker} has found. max(Date): {df.query("maar==1").index.max()}'
        print(message)
        return [1, df, message]
    else:
        return [0, df, ""]





if __name__ == '__main__':

    rlt1 = {}
    rlt0 = {}

    ticker_dict = {'006400':'삼성SDI'
                   ,'039310':'세중'}

    message = ""
    
    for ticker in tqdm(ticker_dict):
        print(f'{ticker}: {ticker_dict.get(ticker)} start')
        rlt_code, df, m = get_maar(ticker)

        if rlt_code == 1:
            rlt1.update({ticker:df})
        elif rlt_code == 0:
            rlt0.update({ticker: df})

    df = rlt1['006400'].dropna()
    df = rlt1['006400'].iloc[-90:]
    
    import mplfinance as mpf

    from stkutils import mpf_style

    apd = [mpf.make_addplot(df['ma5'])
          ,mpf.make_addplot(df['ma10'])
          ,mpf.make_addplot(df['ma20'])
          ,mpf.make_addplot(df['ma60'])
          ,mpf.make_addplot(df['ma120'])]
    mpf.plot(df, type='candle', volume=True, style=mpf_style, addplot=apd)  # 최근 60 row data 출력


    # 정배열 주식 백테스트
    from stkutils import backtest
    
    ticker = '006400'
    rlt_code, df, m = get_maar(ticker)

    df[df['maar']==1]
    df.head()

    rlt = backtest(df, 'maar', ticker)
    rlt['days'].value_counts()
    rlt.groupby('days')['yrate'].mean()








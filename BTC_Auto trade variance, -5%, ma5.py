import time
import pyupbit
import datetime
import requests

access = "PYpDOzxic5F46ArXdVHYbrxtgcDBhPkIjxpQ0BN3"
secret = "JskgqE616C3YRxrQBvjKqaDzQrElfxr4M8H9DoFM"
myToken = "xoxb-your-token"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    """ohlcv : 주식의 종가,시가, 최고,최저 정보 불러오는 함수"""
    """iloc : 인덱스 함수 [1]이 오늘, [0]은 어제"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[1]['open'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price
  
def get_open_price(ticker):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    open_price = df.iloc[1]['open']
    return open_price      

def get_target_percent(ticker):
    """변동성 돌파 전략에 전날 변동성 계산"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_percent = (df.iloc[0]['high'] - df.iloc[0]['low'])/df.iloc[0]['close'] 
    return target_percent      

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#crypto", "autotrade start")


while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(hours=12)
        open_price = get_open_price("KRW-BTC")
        current_price = get_current_price("KRW-BTC") 

        if start_time < now < end_time - datetime.timedelta(seconds=10) and current_price > open_price*0.95 :
            target_price = get_target_price("KRW-BTC", 0.5)
            ma5 = get_ma5("KRW-BTC")
            target_percent = get_target_percent("KRW-BTC")
            current_price = get_current_price("KRW-BTC")  
            if target_price < current_price and ma5 < current_price:
                krw = get_balance("KRW")
                btc = get_balance("BTC")
                if target_percent  <= 0.01:
                    if btc < 0.0001:
                        buy_result = upbit.buy_market_order("KRW-BTC", krw*(0.49))
                        post_message(myToken,"#crypto", "BTC buy : " +str(buy_result))
                elif 0.01 < target_percent:
                    if btc < 0.0001:
                        buy_result = upbit.buy_market_order("KRW-BTC", krw*(1/target_percent/200))
                        post_message(myToken,"#crypto", "BTC buy : " +str(buy_result))
                    

        else:
            btc = get_balance("BTC")
            if btc > 0.00004:
                sell_result = upbit.sell_market_order("KRW-BTC", btc*0.9995)
                post_message(myToken,"#crypto", "BTC buy : " +str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken,"#crypto", e)
        time.sleep(1)
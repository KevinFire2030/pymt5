import MetaTrader5 as mt5
import pandas as pd
pd.set_option('display.max_columns', 500) # 표시될 칼럼 수
pd.set_option('display.width', 1500)      # 표시할 최대 표 너비
import time
from datetime import datetime
# 표준 시간대 작업을 위한 pytz 모듈
import pytz

def initialize_mt5():
    #path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"

    login = 100031026
    password = "Hoya1515!!"
    server = "InfinoxLimited-MT5Demo"

    timeout = 10000
    portable = False

    if mt5.initialize(login=login, password=password, server=server, timeout=timeout, portable=portable):
        print("Initialization successful")

        account_info = mt5.account_info()

        if account_info != None:

            print(account_info)
            # 거래 계정 자료를 딕셔너리 형태로 표시
            print("Show account_info()._asdict():")
            account_info_dict = mt5.account_info()._asdict()
            for prop in account_info_dict:
                print("  {}={}".format(prop, account_info_dict[prop]))
            print()

            # 딕셔너리를 데이터프레임으로 변환하여 출력
            df = pd.DataFrame(list(account_info_dict.items()), columns=['property', 'value'])
            print("account_info() as dataframe:")
            print(df)

        # MetaTrader 5 버전에서 데이터 표시
        print(mt5.version())
        # 터미널 설정 및 상태에 대한 정보 표시
        terminal_info = mt5.terminal_info()
        if terminal_info != None:
            # 터미널 데이터를 '있는 그대로' 표시
            print(terminal_info)
            # 목록 형태로 데이터 표시
            print("Show terminal_info()._asdict():")
            terminal_info_dict = mt5.terminal_info()._asdict()
            for prop in terminal_info_dict:
                print("  {}={}".format(prop, terminal_info_dict[prop]))
            print()
            # 딕셔너리를 데이터프레임으로 변환하여 출력
            df = pd.DataFrame(list(terminal_info_dict.items()), columns=['property', 'value'])
            print("terminal_info() as dataframe:")
            print(df)

        # 금융상품의 수 가져오기
        symbols = mt5.symbols_total()
        if symbols > 0:
            print("Total symbols =", symbols)
        else:
            print("심볼을 찾을 수 없습니다")




    else:
        print("Initialize failed", mt5.last_error())
        quit()


initialize_mt5()

"""
# 모든 심볼 가져오기
symbols=mt5.symbols_get()
print('Symbols: ', len(symbols))
count=0
# 첫 다섯 개 표시
for s in symbols:
    count+=1
    print("{}. {}".format(count,s.name))
    #if count==5: break
print()


# 모든 심볼 가져오기
# group = Index-Cash
group_symbols=mt5.symbols_get(group="*USD*")
print('len(*USD*)) ', len(group_symbols))
# 첫 다섯 개 표시
for s in group_symbols:
    print(s.name)
print()

# MarketWatch에서 EURJPY 심볼 활성화 시도
selected = mt5.symbol_select("NAS100", True)
if not selected:
    print("NAS100 선택 실패")
    mt5.shutdown()
    quit()

# EURJPY 심볼 속성 표시
symbol_info = mt5.symbol_info("NAS100")
if symbol_info != None:
    # 터미널 데이터를 '있는 그대로' 표시
    print(symbol_info)
    print("NAS100: spread =", symbol_info.spread, "  digits =", symbol_info.digits)
    # 심볼 속성 표시 목록
    print("Show symbol_info(\"NAS100\")._asdict():")
    symbol_info_dict = mt5.symbol_info("NAS100")._asdict()
    for prop in symbol_info_dict:
        print("  {}={}".format(prop, symbol_info_dict[prop]))

    # 딕셔너리를 데이터프레임으로 변환하여 출력
    df = pd.DataFrame(list(symbol_info_dict.items()), columns=['property', 'value'])
    print("symbol_info_dict() as dataframe:")
    print(df)

# 최근 NAS100 틱 표시
lasttick=mt5.symbol_info_tick("NAS100")
print(lasttick)
# 목록 형식으로 틱 필드 값 표시
print("Show symbol_info_tick(\"NAS100\")._asdict():")
symbol_info_tick_dict = mt5.symbol_info_tick("NAS100")._asdict()
for prop in symbol_info_tick_dict:
    print("  {}={}".format(prop, symbol_info_tick_dict[prop]))
"""

"""
# EURUSD(Depth of Market)에 대한 마켓 심층 업데이트 구독
if mt5.market_book_add('NAS100'):
  # 시장 심층 데이터를 10회 반복 수집
   for i in range(10):
        # 마켓 심층(Depth of Market) 콘텐츠 확보
        items = mt5.market_book_get('NAS100')
        # 마켓의 전체 뎁스를 '있는 그대로' 단일 문자열로 표시
        print(items)
        # 이제 각 주문을 구분하여 표시하여 보다 명확히 확인할 수 있습니다
        if items:
            for it in items:
                # 주문 내용
                print(it._asdict())
        # 마켓 수준 데이터의 다음 요청이 있기 전에 5초간 일시 중지
        time.sleep(5)
  # 시장 수준 업데이트(Depth of Market) 구독을 취소합니다.
   mt5.market_book_release('NAS100')
else:
    print("mt5.market_book_add('NAS100') failed, error code =",mt5.last_error())
"""

"""
# 표준 시간대를 UTC로 설정
timezone = pytz.timezone("Etc/UTC")
# 로컬 시간대 오프셋 구현을 방지하기 위해 UTC 표준 시간대에 'datetime' 개체를 생성합니다.
utc_from = datetime(2024, 7, 24, tzinfo=timezone)
# UTC 표준 시간대로 2020년 1월 10일부터 10개의 EURD H4 막대를 설치
rates = mt5.copy_rates_from("NAS100", mt5.TIMEFRAME_D1, utc_from, 10)

# MetaTrader 5 터미널 연결 종료
#mt5.shutdown()
# 수집된 데이터의 각 요소를 새 줄로 표시
print("수집된 데이터를 '있는 그대로' 표시")
for rate in rates:
    print(rate)

# 가져온 데이터로 DataFrame 생성
rates_frame = pd.DataFrame(rates)
# 시간(초)을 날짜 시간 형식으로 변환
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

# 데이터 표시
print("\n데이터와 함께 dataframe 표시")
print(rates_frame)


# get 10 GBPUSD D1 bars from the current day
rates = mt5.copy_rates_from_pos("NAS100", mt5.TIMEFRAME_H1, 0, 10)

# MetaTrader 5 터미널 연결 종료
#mt5.shutdown()
# 수집된 데이터의 각 요소를 새 줄로 표시
print("수집된 데이터를 '있는 그대로' 표시")


# 가져온 데이터로 DataFrame 생성
rates_frame = pd.DataFrame(rates)
# 시간(초)을 날짜 시간 형식으로 변환
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

# 데이터 표시
print("\n데이터와 함께 dataframe 표시")
print(rates_frame)

"""
"""
# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
# 로컬 표준 시간대를 구현하지 않도록 UTC 표준 시간대에 'datetime' 개체를 생성합니다 offset
utc_from = datetime(2024, 7, 1, tzinfo=timezone)
utc_to = datetime(2024, 7, 23, tzinfo=timezone)
# UTC 표준 시간대에서 2020.01.10 00:00 - 2020.01.11 13:00의 간격 내에 USDJPY M5에서 막대를 가져옵니다
rates = mt5.copy_rates_range("NAS100", mt5.TIMEFRAME_D1, utc_from, utc_to)

# 수집된 데이터의 각 요소를 새 라인로 표시
print("수집된 데이터를 '있는 그대로' 표시")
counter = 0
for rate in rates:
    counter += 1
    if counter <= 10:
        print(rate)

# 가져온 데이터로 DataFrame 생성
rates_frame = pd.DataFrame(rates)
# 시간(초)을 'datetime' 형식으로 변환합니다.
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

# display data
print("\n데이터와 함께 dataframe 표시")
print(rates_frame.head(10))

"""
"""
# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
# 로컬 시간대 오프셋 구현을 방지하기 위해 UTC 표준 시간대에 'datetime' 개체를 생성
utc_from = datetime(2024, 7, 24, tzinfo=timezone)
# UTC 표준 시간대로 2019.10.01.부터 시작하는 100 000 EURUSD 틱 요청
ticks = mt5.copy_ticks_from("NAS100", utc_from, 100000, mt5.COPY_TICKS_ALL)
print("Ticks received:", len(ticks))

# 새 라인의 각 틱에 데이터 표시
print("수집된 틱을 '있는 그대로' 표시")
count = 0
for tick in ticks:
    count += 1
    print(tick)
    if count >= 10:
        break

# 가져온 데이터로 DataFrame 생성
ticks_frame = pd.DataFrame(ticks)
# 시간(초)을 날짜 시간 형식으로 변환
ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')

# display data
print("\n틱과 함께 dataframe 표시")
print(ticks_frame)

# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
# 로컬 시간대 오프셋 구현을 방지하기 위해 UTC 표준 시간대에 'datetime' 개체를 생성합니다
utc_from = datetime(2024, 1, 1, tzinfo=timezone)
utc_to = datetime(2024, 7, 24, tzinfo=timezone)
# request AUDUSD ticks within 11.01.2020 - 11.01.2020
ticks = mt5.copy_ticks_range("NAS100", utc_from, utc_to, mt5.COPY_TICKS_ALL)
print("Ticks received:", len(ticks))

# MetaTrader 5 터미널에 대한 연결 종료
#mt5.shutdown()

# 새 라인의 각 틱에 데이터 표시
print("수집된 틱을 '있는 그대로' 표시합니다.")
count = 0
for tick in ticks:
    count += 1
    print(tick)
    if count >= 10:
        break

# 가져온 데이터로 DataFrame 생성
ticks_frame = pd.DataFrame(ticks)
# 시간(초)을 날짜 시간 형식으로 변환
ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')

# display data
print("\n틱과 함께 dataframe 표시")
print(ticks_frame)


"""

# 계정 통화 가져오기
account_currency=mt5.account_info().currency
print("계정 통화:",account_currency)

# 요청 구조 준비
symbol = "NAS100"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print("심볼 찾을 수 없음, order_check() 호출 불가")
    mt5.shutdown()
    quit()

# 심볼을 MarketWatch에서 사용할 수 없는 경우 추가
if not symbol_info.visible:
    print("심볼 보이지 않음, trying to switch on")
    if not mt5.symbol_select(symbol, True):
        print("symbol_select({}}) failed, exit", symbol)
        mt5.shutdown()
        quit()

# 요청 준비
lot = 10
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 10
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    #"price": price,
    #"sl": price - 100 * point,
    #"tp": price + 100 * point,
    #"deviation": deviation,
    #"magic": 234000,
    #"comment": "python script open",
    #"type_time": mt5.ORDER_TIME_GTC,
    #"type_filling": mt5.ORDER_FILLING_RETURN,
}

# 거래 요청 전송
result = mt5.order_send(request)
# 실행 결과 확인
print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("2. order_send failed, retcode={}".format(result.retcode))
    # 결과를 사전으로 요청하여 요소별로 표시
    result_dict = result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field, result_dict[field]))
        # 거래 요청 구조인 경우 요소별로도 표시
        if field == "request":
            traderequest_dict = result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
    print("shutdown() and quit")
    mt5.shutdown()
    quit()

print("2. order_send done, ", result)
print("   opened position with POSITION_TICKET={}".format(result.order))
print("   sleep 2 seconds before closing position #{}".format(result.order))

time.sleep(2)
# 마감 요청 생성
position_id = result.order
price = mt5.symbol_info_tick(symbol).bid
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_SELL,
    "position": position_id,
    "price": price,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script close",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}
# 거래 요청 전송
result = mt5.order_send(request)
# 실행 결과 확인
print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id, symbol, lot, price,
                                                                                     deviation));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("4. order_send failed, retcode={}".format(result.retcode))
    print("   result", result)
else:
    print("4. position #{} closed, {}".format(position_id, result))
    # 결과를 사전으로 요청하여 요소별로 표시
    result_dict = result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field, result_dict[field]))
        # 거래 요청 구조인 경우 요소별로도 표시
        if field == "request":
            traderequest_dict = result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))

print("된다! 하면된다~!!")
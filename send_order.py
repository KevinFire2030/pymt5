import time
import MetaTrader5 as mt5
import pandas as pd

# MetaTrader 5 패키지에 데이터 표시
print("MetaTrader5 패키지 저자: ", mt5.__author__)
print("MetaTrader5 패키지 버전: ", mt5.__version__)

# MetaTrader 5 터미널과의 연결 설정
if not mt5.initialize():
    print("initialize() 실패, 오류 코드 =", mt5.last_error())
    quit()

"""
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

"""


# 매수 요청 구조를 준비
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

lot = 1.0
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    #"sl": price - 100 * point,
    #"tp": price + 100 * point,
    "sl": price - 50,
    "tp": price + 100,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    #"type_filling": mt5.ORDER_FILLING_RETURN,
    "type_filling": mt5.ORDER_FILLING_IOC,
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
# create a close request
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
    #"type_filling": mt5.ORDER_FILLING_RETURN,
    "type_filling": mt5.ORDER_FILLING_IOC,
}
# send a trading request
result = mt5.order_send(request)
# check the execution result
print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id, symbol, lot, price,
                                                                                     deviation));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("4. order_send failed, retcode={}".format(result.retcode))
    print("   result", result)
else:
    print("4. position #{} closed, {}".format(position_id, result))
    # request the result as a dictionary and display it element by element
    result_dict = result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field, result_dict[field]))
        # if this is a trading request structure, display it element by element as well
        if field == "request":
            traderequest_dict = result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

print("하면된다!")
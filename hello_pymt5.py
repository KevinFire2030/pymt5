import MetaTrader5 as mt5
import pandas as pd


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

mt5.shutdown()

print("된다! 하면된다~!!")
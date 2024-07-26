import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5 import uic
import time
#from datetime import datetime
import datetime
# 표준 시간대 작업을 위한 pytz 모듈
import pytz
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', 500) # 표시될 칼럼 수
pd.set_option('display.width', 1500)      # 표시할 최대 표 너비
import pandas_ta as ta
import MetaTrader5 as mt5


main_form = uic.loadUiType("mainwindow.ui")[0]

class PyMT5(QMainWindow, main_form):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        # MetaTrader 5 패키지에 데이터 표시
        print("MetaTrader5 패키지 저자: ", mt5.__author__)
        print("MetaTrader5 패키지 버전: ", mt5.__version__)

        # MetaTrader 5 터미널과의 연결 설정
        self.initialize_mt5()


        ## 메인윈도우 이벤트 처리
        self.set_event_handler()

    def set_event_handler(self):
        # 주문
        self.menu_order_send.triggered.connect(self.action_order_send)
        self.menu_order_total.triggered.connect(self.action_order_total)
        self.menu_order_get.triggered.connect(self.action_order_get)
        self.menu_order_calc_margin.triggered.connect(self.action_order_calc_margin)
        self.menu_order_calc_profit.triggered.connect(self.action_order_calc_profit)
        self.menu_order_check.triggered.connect(self.action_order_check)

        # 포지션
        self.menu_position_total.triggered.connect(self.action_position_total)
        self.menu_position_get.triggered.connect(self.action_position_get)

        # 히스토리
        self.menu_history_orders_total.triggered.connect(self.action_history_orders_total)
        self.menu_history_orders_get.triggered.connect(self.action_history_orders_get)
        self.menu_history_deals_total.triggered.connect(self.action_history_deals_total)
        self.menu_history_deals_get.triggered.connect(self.action_history_deals_get)

        # 차트
        self.menu_copy_rates_from.triggered.connect(self.action_copy_rates_from)
        self.menu_copy_rates_from_pos.triggered.connect(self.action_copy_rates_from_pos)
        self.menu_copy_rates_range.triggered.connect(self.action_copy_rates_range)
        self.menu_copy_ticks_from.triggered.connect(self.action_copy_ticks_from)
        self.menu_copy_ticks_range.triggered.connect(self.action_copy_ticks_range)
        self.menu_real_time_chart.triggered.connect(self.action_real_time_chart)

        pass


    def action_real_time_chart(self):

        pass

    def action_copy_ticks_range(self):

        # set time zone to UTC
        timezone = pytz.timezone("Etc/UTC")
        # 로컬 표준 시간대를 구현하지 않도록 UTC 표준 시간대에 'datetime' 개체를 생성합니다 offset
        utc_from = datetime.datetime(2024, 7, 26, tzinfo=timezone)
        # utc_to = datetime(2020, 1, 11, hour=13, tzinfo=timezone)
        utc_to = datetime.datetime.now(timezone) + datetime.timedelta(hours=3)
        # UTC 표준 시간대에서 2020.01.10 00:00 - 2020.01.11 13:00의 간격 내에 USDJPY M5에서 막대를 가져옵니다
        rates = mt5.copy_ticks_range("NAS100", utc_from, utc_to, mt5.COPY_TICKS_ALL)
       #rates = mt5.copy_ticks_range("NAS100", utc_from, utc_to, mt5.COPY_TICKS_INFO)

        if rates is None:
            print(f"에러: {mt5.last_error()}")

        else:
            # 가져온 데이터로 DataFrame 생성
            rates_frame = pd.DataFrame(rates)
            # 시간(초)을 날짜 시간 형식으로 변환
            rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

            # 데이터 표시
            print("\n데이터와 함께 dataframe 표시")
            print(rates_frame)

        pass

    def action_copy_ticks_from(self):

        # 표준 시간대를 UTC로 설정
        timezone = pytz.timezone("Etc/UTC")
        #utc_from = datetime.datetime.now(timezone) + datetime.timedelta(hours=3)
        utc_from = datetime.datetime(2024, 1, 1, tzinfo=timezone)
        # UTC 표준 시간대로 2020년 1월 10일부터 10개의 EURD H4 막대를 설치
        rates = mt5.copy_ticks_from("NAS100", utc_from, 10000000, mt5.COPY_TICKS_ALL)

        # 가져온 데이터로 DataFrame 생성
        rates_frame = pd.DataFrame(rates)
        # 시간(초)을 날짜 시간 형식으로 변환
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

        # 데이터 표시
        print("\n데이터와 함께 dataframe 표시")
        print(rates_frame)

        pass

    def action_copy_rates_range(self):

        # set time zone to UTC
        timezone = pytz.timezone("Etc/UTC")
        # 로컬 표준 시간대를 구현하지 않도록 UTC 표준 시간대에 'datetime' 개체를 생성합니다 offset
        utc_from = datetime.datetime(2000, 6, 1, tzinfo=timezone)
        #utc_to = datetime(2020, 1, 11, hour=13, tzinfo=timezone)
        utc_to = datetime.datetime.now(timezone) + datetime.timedelta(hours=3)
        # UTC 표준 시간대에서 2020.01.10 00:00 - 2020.01.11 13:00의 간격 내에 USDJPY M5에서 막대를 가져옵니다
        rates = mt5.copy_rates_range("NAS100", mt5.TIMEFRAME_D1, utc_from, utc_to)

        if rates is None:
            print(f"에러: {mt5.last_error()}")

        else:
            # 가져온 데이터로 DataFrame 생성
            rates_frame = pd.DataFrame(rates)
            # 시간(초)을 날짜 시간 형식으로 변환
            rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

            # 데이터 표시
            print("\n데이터와 함께 dataframe 표시")
            print(rates_frame)


        pass

    def action_copy_rates_from_pos(self):

        # 표준 시간대를 UTC로 설정
        timezone = pytz.timezone("Etc/UTC")
        # 로컬 시간대 오프셋 구현을 방지하기 위해 UTC 표준 시간대에 'datetime' 개체를 생성합니다.
        utc_from = datetime.datetime.now(timezone) + datetime.timedelta(hours=3)

        # 막대의 번호는 현재에서 과거로 매겨집니다. 그러므로, 0 막대는 현재의 것을 의미합니다.
        rates = mt5.copy_rates_from_pos("NAS100", mt5.TIMEFRAME_M1, 0, 10)

        # 2달까지는 되는데 3개월부터는 안되네
        #rates = mt5.copy_rates_from_pos("NAS100", mt5.TIMEFRAME_M1, 0, 1*60*24*30*2)

        if rates is None:
            print(f"에러: {mt5.last_error()}")

        else:
            # 가져온 데이터로 DataFrame 생성
            rates_frame = pd.DataFrame(rates)
            # 시간(초)을 날짜 시간 형식으로 변환
            rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

            # 데이터 표시
            print("\n데이터와 함께 dataframe 표시")
            print(rates_frame)

        pass

    def action_copy_rates_from(self):

        # 표준 시간대를 UTC로 설정
        timezone = pytz.timezone("Etc/UTC")
        #timezone = pytz.timezone("Europe/Moscow")
        #timezone = pytz.timezone('Asia/Seoul')
        # 로컬 시간대 오프셋 구현을 방지하기 위해 UTC 표준 시간대에 'datetime' 개체를 생성합니다.
        #utc_from = datetime(2024, 7, 26, 20, 0, 0, tzinfo=timezone)
        utc_from = datetime.datetime.now(timezone) + datetime.timedelta(hours=3)

        #utc_from = datetime.utcnow()

        #utc_from = datetime(2024, 7, 26, 20, 0, 0)

        #utc_from = datetime(2024, 7, 25, 17, 46)

        # UTC 표준 시간대로 2020년 1월 10일부터 10개의 EURD H4 막대를 설치
        rates = mt5.copy_rates_from("NAS100", mt5.TIMEFRAME_M1, utc_from, 10)

        # 가져온 데이터로 DataFrame 생성
        rates_frame = pd.DataFrame(rates)
        # 시간(초)을 날짜 시간 형식으로 변환
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

        # 데이터 표시
        print("\n데이터와 함께 dataframe 표시")
        print(rates_frame)

        pass

    def action_history_deals_get(self):

        # 내역에서 딜 수 가져오기
        from_date = datetime.datetime(2020, 1, 1)
        to_date = datetime.datetime.now()
        # 이름에 지정된 간격 내에 "GBP"가 포함된 심볼에 대한 딜 가져오기
        deals = mt5.history_deals_get(from_date, to_date, group="*GBP*")
        if deals == None:
            print("No deals with group=\"*USD*\", error code={}".format(mt5.last_error()))
        elif len(deals) > 0:
            print("history_deals_get({}, {}, group=\"*GBP*\")={}".format(from_date, to_date, len(deals)))

        # 이름에 "EUR" 또는 "GBP"가 포함되지 않은 심볼에 대한 거래를 가져오기
        deals = mt5.history_deals_get(from_date, to_date, group="*,!*EUR*,!*GBP*")
        if deals == None:
            print("딜이 없습니다, 에러 코드={}".format(mt5.last_error()))
        elif len(deals) > 0:
            print("history_deals_get(from_date, to_date, group=\"*,!*EUR*,!*GBP*\") =", len(deals))
            # 수집된 딜을 '있는 그대로' 표시
            for deal in deals:
                print("  ", deal)
            print()
            # pandas.DataFrame을 사용하여 테이블로써 이러한 딜을 표시
            df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            print(df)
        print("")

        # 포지션 #530218319와 관련한 딜 가져오기
        position_id = 8570972
        position_deals = mt5.history_deals_get(position=position_id)
        if position_deals == None:
            print("No deals with position #{}".format(position_id))
            print("error code =", mt5.last_error())
        elif len(position_deals) > 0:
            print("Deals with position id #{}: {}".format(position_id, len(position_deals)))
            # pandas.DataFrame을 사용하여 테이블로써 이러한 딜을 표시
            df = pd.DataFrame(list(position_deals), columns=position_deals[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            print(df)

        pass

    def action_history_deals_total(self):

        # 내역에서 딜 수 가져오기
        from_date = datetime.datetime(2020, 1, 1)
        to_date = datetime.datetime.now()
        deals = mt5.history_deals_total(from_date, to_date)
        if deals > 0:
            print("총 딜=", deals)
        else:
            print("내역에서 딜을 찾을 수 없음")

        pass

    def action_history_orders_get(self):

        # 내역에서 주문 수를 가져옵니다
        from_date = datetime.datetime(2020, 1, 1)
        to_date = datetime.datetime.now()
        history_orders = mt5.history_orders_get(from_date, to_date, group="*NAS*")
        if history_orders == None:
            print("No history orders with group=\"*NAS*\", error code={}".format(mt5.last_error()))
        elif len(history_orders) > 0:
            print("history_orders_get({}, {}, group=\"*NAS*\")={}".format(from_date, to_date, len(history_orders)))
        print()

        # 모든 내역상 주문을 포지션별로 표시
        position_id = 8570972
        position_history_orders = mt5.history_orders_get(position=position_id)
        if position_history_orders == None:
            print("No orders with position #{}".format(position_id))
            print("error code =", mt5.last_error())
        elif len(position_history_orders) > 0:
            print("Total history orders on position #{}: {}".format(position_id, len(position_history_orders)))
            # 지정된 포지션을 가지고 있는 모든 과거 주문을 표시
            for position_order in position_history_orders:
                print(position_order)
            print()
            # pandas를 이용해 이 주문들을 표로 표시.DataFrame
            df = pd.DataFrame(list(position_history_orders), columns=position_history_orders[0]._asdict().keys())
            df.drop(['time_expiration', 'type_time', 'state', 'position_by_id', 'reason', 'volume_current',
                     'price_stoplimit', 'sl', 'tp'], axis=1, inplace=True)
            df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
            df['time_done'] = pd.to_datetime(df['time_done'], unit='s')
            print(df)

        pass

    def action_history_orders_total(self):

        # 내역에서 주문 수를 가져옵니다
        from_date = datetime.datetime(2020, 1, 1)
        to_date = datetime.datetime.now()
        history_orders = mt5.history_orders_total(from_date, to_date)
        if history_orders > 0:
            print("Total history orders=", history_orders)
        else:
            print("주문을 내역에서 찾을 수 없습니다")

        pass

    def action_position_get(self):

        # USDCHF에서의 오픈 포지션 가져오기
        positions = mt5.positions_get(symbol="USDCHF")
        if positions == None:
            print("USDCHF에 포지션 없음, 오류 코드={}".format(mt5.last_error()))
        elif len(positions) > 0:
            print("USDCHF에서의 총 포지션 =", len(positions))
            # 모든 오픈 포지션 표시
            for position in positions:
                print(position)

        # 이름에 "*USD*"가 포함된 심볼의 포지션 목록을 가져옵니다
        usd_positions = mt5.positions_get(group="*USD*")
        if usd_positions == None:
            print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error()))
        elif len(usd_positions) > 0:
            print("positions_get(group=\"*USD*\")={}".format(len(usd_positions)))
            # 이러한 포지션을 pandas.DataFrame을 사용해 표로 표시
            df = pd.DataFrame(list(usd_positions), columns=usd_positions[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
            print(df)

        # 이름에 "*USD*"가 포함된 심볼의 포지션 목록을 가져옵니다
        nas100_positions = mt5.positions_get(group="NAS100")
        if nas100_positions == None:
            print("No positions with group=\"NAS100\", error code={}".format(mt5.last_error()))
        elif len(nas100_positions) > 0:
            print("positions_get(group=\"NAS100\")={}".format(len(nas100_positions)))
            # 이러한 포지션을 pandas.DataFrame을 사용해 표로 표시
            df = pd.DataFrame(list(nas100_positions), columns=nas100_positions[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
            print(df)

        pass


    def action_position_total(self):

        # 오픈 포지션 존재 유무 확인
        positions_total = mt5.positions_total()
        if positions_total > 0:
            print("Total positions=", positions_total)
        else:
            print("포지션을 찾을 수 없습니다")


        pass

    def action_order_check(self):

        # 계정 통화 가져오기
        account_currency = mt5.account_info().currency
        print("계정 통화:", account_currency)

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
        point = mt5.symbol_info(symbol).point
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 1.0,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(symbol).ask,
            "sl": mt5.symbol_info_tick(symbol).ask - 100 * point,
            "tp": mt5.symbol_info_tick(symbol).ask + 100 * point,
            "deviation": 10,
            "magic": 234000,
            "comment": "python script",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        # 점검을 수행하고 '있는 그대로' 결과를 표시합니다.
        result = mt5.order_check(request)
        print(result);
        # 결과를 딕셔너리로 요청하여 요소별로 표시
        result_dict = result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field, result_dict[field]))
            # 거래 요청 구조인 경우 요소별로도 표시
            if field == "request":
                traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))

        pass

    def action_order_calc_profit(self):

        # get account currency
        account_currency = mt5.account_info().currency
        print("계정 통화:", account_currency)

        # 심볼 리스트 정렬
        symbols = ("EURUSD", "GBPUSD", "USDJPY", "NAS100")
        print("수익을 확인할 기호:", symbols)
        # 매매이익 추정
        lot = 1.0
        distance = 300
        for symbol in symbols:
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                print("심볼 찾을 수 없음, 스킵")
                continue
            if not symbol_info.visible:
                print("심볼이 보이지 않습니다, trying to switch on")
                if not mt5.symbol_select(symbol, True):
                    print("symbol_select({}}) failed, skipped", symbol)
                    continue
            point = mt5.symbol_info(symbol).point
            symbol_tick = mt5.symbol_info_tick(symbol)
            ask = symbol_tick.ask
            bid = symbol_tick.bid

            buy_profit = mt5.order_calc_profit(mt5.ORDER_TYPE_BUY, symbol, lot, ask, ask + distance * point)
            if buy_profit != None:
                print("   buy {} {} lot: profit on {} points => {} {}".format(symbol, lot, distance, buy_profit,
                                                                              account_currency));
            else:
                print("order_calc_profit(ORDER_TYPE_BUY) 실패, 오류 코드 =", mt5.last_error())

            sell_profit = mt5.order_calc_profit(mt5.ORDER_TYPE_SELL, symbol, lot, bid, bid - distance * point)
            if sell_profit != None:
                print("   sell {} {} lots: profit on {} points => {} {}".format(symbol, lot, distance, sell_profit,
                                                                                account_currency));
            else:
                print("order_calc_profit(ORDER_TYPE_SELL) failed, error code =", mt5.last_error())
            print()


        pass


    def action_order_calc_margin(self):

        # 계정 통화 가져오기
        account_currency = mt5.account_info().currency
        print("계정 통화:", account_currency)

        # 심볼 리스트 정렬
        symbols = ("NAS100", "EURUSD")
        print("마진을 확인할 심볼:", symbols)
        action = mt5.ORDER_TYPE_BUY
        lot = 1.0
        for symbol in symbols:
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                print("심볼 찾을 수 없음, 스킵")
                continue
            if not symbol_info.visible:
                print("심볼이 보이지 않습니다, trying to switch on")
                if not mt5.symbol_select(symbol, True):
                    print("symbol_select({}}) failed, skipped", symbol)
                    continue
            ask = mt5.symbol_info_tick(symbol).ask
            margin = mt5.order_calc_margin(action, symbol, lot, ask)
            if margin != None:
                print("   {} buy {} lot margin: {} {}".format(symbol, lot, margin, account_currency));
            else:
                print("order_calc_margin failed: , error code =", mt5.last_error())

        pass

    def action_order_get(self):

        # GBPUSD에서 활성 주문의 데이터 표시
        orders = mt5.orders_get(symbol="NAS100")
        if orders is None:
            print("NAS100에 새 주문 없음, 에러 코드={}".format(mt5.last_error()))
        else:
            print("NAS100에 대한 총 주문:", len(orders))
            # 모든 활성 주문 표시
            for order in orders:
                print(order)
        print()


        pass

    def action_order_total(self):

        # 주문이 유효한지 확인
        orders = mt5.orders_total()
        if orders > 0:
            print("Total orders=", orders)
        else:
            print("주문을 찾을 수 없습니다")

        pass

    def action_order_send(self):

        #print(f"order_send")

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
            # "sl": price - 100 * point,
            # "tp": price + 100 * point,
            "sl": price - 50,
            "tp": price + 100,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            # "type_filling": mt5.ORDER_FILLING_RETURN,
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

        """
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
            # "type_filling": mt5.ORDER_FILLING_RETURN,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        # send a trading request
        result = mt5.order_send(request)
        # check the execution result
        print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id, symbol, lot,
                                                                                             price,
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
        """
        pass

    def initialize_mt5(self):

        # path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"

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

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        window = PyMT5()
        window.show()

        sys.exit( app.exec_() )
    except Exception as e:
        print(e)

import MetaTrader5 as mt5


def initialize_mt5():
    #path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"

    login = 100031026
    password = "Hoya1515!!"
    server = "InfinoxLimited-MT5Demo"

    timeout = 60000
    portable = False

    if mt5.initialize(login=login, password=password, server=server, timeout=timeout, portable=portable):
        print("Initialization successful")
    else:
        print("Initialize failed", mt5.last_error())


initialize_mt5()

print("된다! 하면된다~!!")
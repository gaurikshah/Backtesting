from Technical_Indicators import sma as sma, rsi as rsi
from Timeframe_Manipulation import series_resampling as series_resampling
from Trade_Generation import trade_generation as tc
from Trade_Generation import creating_individual_trade

import numpy as np


def rsi50_55sma_system(price_data, period_sma=55, period_rsi=14, period="", trade_type="Both_leg",
                       underlying_instrument_data=None):

    period_sma_str=str(period_sma)+"_SMA"

    if period == "":
        price_period = price_data
    else:
        price_period = series_resampling.price_series_periodic(price_data, period)

    sma.sma(price_period, period_sma)
    rsi.rsi(price_period, period_rsi)

    price_signal_period = price_period

    price_signal = price_data

    # price_signal_period[period_sma] = sma_1

    price_signal_period["Signal"] = np.where((price_signal_period[period_sma_str] <= price_signal_period["Close"]) &
                                      (price_signal_period["rsi"] > 50), 1,
                                      np.where((price_signal_period[period_sma_str] > price_signal_period["Close"]) &
                                               (price_signal_period["rsi"] < 50), -1, 0))

    price_signal["Signal"] = price_signal_period["Signal"].resample("D").ffill()
    price_signal["Signal"].fillna(0, inplace=True)

    price_signal["Trades"] = price_signal["Signal"] - price_signal["Signal"].shift(1)

    if trade_type == "Individual":
        trades = creating_individual_trade.creating_individual_trade(price_signal, underlying_instrument_data)
    else:
        trades = tc.trade_generation(price_signal)

    return trades, price_signal

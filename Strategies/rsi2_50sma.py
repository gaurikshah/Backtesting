from Technical_Indicators import sma as sma, rsi as rsi
from Timeframe_Manipulation import series_resampling as series_resampling
from Trade_Generation import trade_close as tc
from Trade_Generation import creating_individual_trade

import numpy as np

previous_signal = 0


def rsi2_50sma_system(price_data, period_sma, period_rsi, period="", trade_type="Both_leg",
                      underlying_instrument_data=None):
    period_sma_str = str(period_sma) + "_SMA"

    if period == "":
        price_period = price_data
    else:
        price_period = series_resampling.price_series_periodic(price_data, period)

    sma.sma(price_period, period_sma)
    rsi.rsi(price_period, period_rsi)

    price_signal_period = price_period

    price_signal = price_data

    # price_signal_period[period_sma] = sma_1

    price_signal_period["Signal_sma"] = np.where((price_signal_period[period_sma_str] <= price_signal_period["Close"]),
                                                 1, -1)

    price_signal_period["rsi_1"] = price_signal_period["rsi"].shift(1)
    price_signal_period["rsi_1"].fillna(0,inplace=True)

    price_signal_period["Signal_rsi"] = np.where(((price_signal_period["rsi"] > 10) & (price_signal_period["rsi_1"] <10)),1, np.where(
        ((price_signal_period["rsi"] < 90) & (price_signal_period["rsi_1"] > 90)),-1,0))

    price_signal_period["Signal_rsi"].replace(to_replace=0,method="ffill",inplace=True)

    price_signal_period["Signal"] = np.where(
        ((price_signal_period["Signal_sma"] == price_signal_period["Signal_rsi"]) & (price_signal_period["Signal_rsi"]== 1)), 1,
        np.where(((price_signal_period["Signal_sma"] == price_signal_period["Signal_rsi"]) & (price_signal_period["Signal_rsi"]== -1)), -1, 0))

    price_signal["Signal"] = price_signal_period["Signal"].resample("D").ffill()
    price_signal["Signal"].fillna(0, inplace=True)

    price_signal["Trades"] = price_signal["Signal"] - price_signal["Signal"].shift(1)

    if trade_type == "Individual":
        trades = creating_individual_trade.creating_individual_trade(price_signal, underlying_instrument_data)
    else:
        trades = tc.trade_close(price_signal)

    return trades, price_signal


def rsi_signal_generation(rsi, rsi_1):
    global previous_signal

    rsi_1.fillna(0, inplace=True)

    if rsi_1 > 90 & rsi < 90:
        signal = -1
    elif rsi_1 < 10 & rsi > 10:
        signal = 1
    else:
        signal = previous_signal

    previous_signal = signal

    return signal

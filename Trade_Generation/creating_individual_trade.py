import pandas as pd


def creating_individual_trade(price_signal, underlying_instrument_data):
    trades = pd.DataFrame(
        columns=["Date", "Price", "Side", "Contract", "Contract_Type", "Qty", "Trading_Cost", "Strike_Price"])

    trade_data = price_signal[price_signal["Trades"] != 0]

    trade_data = trade_data.loc[underlying_instrument_data.index[0]: underlying_instrument_data.index[-1]]

    trades["Date"] = trade_data.index
    trades.set_index("Date", inplace=True)
    trades["Price"] = underlying_instrument_data["Close"].loc[trade_data.index]
    trades["Side"] = trade_data["Signal"]
    trades["Qty"] = trade_data["Trades"].abs()
    trades["Date"] = trades.index
    trades.index = range(len(trades["Date"]))

    # Inserting first day trade
    last_day = price_signal[price_signal.index < underlying_instrument_data.index[0]].index[-1]

    if price_signal["Signal"].loc[last_day] != 0:
        a = {"Date": underlying_instrument_data.index[0],
             "Price": underlying_instrument_data["Open"].iloc[0],
             "Side": price_signal["Signal"].loc[last_day],
             "Qty": 1
             }
        trades_1 = pd.DataFrame(a, index=[0])
        trades = pd.concat([trades, trades_1], axis=0, ignore_index=True)

    # Inserting last day trade

    if price_signal["Signal"].loc[underlying_instrument_data.index[-1]] != 0:
        a = {"Date": underlying_instrument_data.index[-1],
             "Price": underlying_instrument_data["Close"].iloc[-1],
             "Side": price_signal["Signal"].loc[underlying_instrument_data.index[-1]]*-1,
             "Qty": 1
             }
        trades_1 = pd.DataFrame(a, index=[0])
        trades = pd.concat([trades, trades_1], axis=0, ignore_index=True)

    return trades
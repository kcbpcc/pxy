from candlepxy import get_nifty50_data,dayprinter
def main():
    nifty50_ohlc = get_nifty50_data()
    if not nifty50_ohlc.empty:
        today_data = nifty50_ohlc.iloc[-1][OHLC_COLUMNS]
        dayprinter(*today_data)

if __name__ == "__main__":
    main()

deinit()  # Reset Colorama settings

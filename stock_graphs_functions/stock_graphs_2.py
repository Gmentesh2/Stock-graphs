import pandas
import os
import matplotlib.pyplot as plt


def symbol_to_path(symbol,base_dir="data"):
    """This function returns CSV file to ticker given symbol """
    return os.path.join(base_dir,f"{symbol}.csv")


def getting_data(symbols,dates):
    """This function returns (Adj Close) for given symbols from CSV files"""
    data_frame = pandas.DataFrame(index=dates)
    if "AAPL" not in symbols:
        symbols.insert(0,"AAPL")
    for symbol in symbols:
        data_frame1 = pandas.read_csv(
            symbol_to_path(symbol),
            index_col="Date",
            parse_dates=True,
            usecols=["Date","Adj Close"]
            
            
        )
        data_frame1 =data_frame1.rename(columns={"Adj Close": symbol})
        data_frame = data_frame.join(data_frame1, how="inner").dropna()
    return data_frame

def get_rolling_mean(values,window):
    return values.rolling(window).mean()

def get_rolling_std(values,window):
    return values.rolling(window).std()

def get_bollinger_band(rm,rstd):
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2 
    return upper_band, lower_band

def main():
    dates = pandas.date_range("2021-01-01","2021-12-30")
    symbols = ["AAPL"]
    data_frame = getting_data(symbols,dates)
    
    rm_apple = get_rolling_mean(data_frame["AAPL"],window=15)
    
    rstd_apple = get_rolling_std(data_frame["AAPL"], window=15)
    
    upper_band, lower_band = get_bollinger_band(rm_apple,rstd_apple)
    
    ax = data_frame["AAPL"].plot(title="Bollinger band",label="Apple stock price")
    rm_apple.plot(label="Rolling mean", ax=ax)
    rstd_apple.plot(label="Standard devation",ax=ax)
    upper_band.plot(label="Upper band", ax=ax)
    lower_band.plot(label="Lower band", ax=ax)
    
    ax.set_xlabel("Dates")
    ax.set_ylabel("Prices")
    ax.legend()
    plt.savefig("graphs/applecombwithstd.png")

if __name__=="__main__":
    main()
    
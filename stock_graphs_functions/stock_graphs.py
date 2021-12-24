import pandas
import os
import matplotlib.pyplot as plt



def symbol_to_path(symbol,base_dir="data"):
    """This function returns CSV file to ticker given symbol """
    return os.path.join(base_dir,f"{symbol}.csv")


def getting_data(symbols,dates):
    """This function returns (Adj Close) for given symbols from CSV files"""
    data_frame = pandas.DataFrame(index=dates)
    if "DIS" not in symbols:
        symbols.insert(0,"DIS")
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

def main():
    """Main function to see the results"""
    dates = pandas.date_range("2021-01-01","2021-10-30")
    symbols = ["AAPL","FB","WMT"]
    data_frame = getting_data(symbols,dates)
    print(data_frame)
    print(data_frame.mean())
    print(data_frame.median())
    # standard deviation , understanding how risky is stock, depends on its volatility . 
    print(data_frame.std())
    # rolling 5 days - understanding last five days changes in stock prices 
    ax = data_frame["AAPL"].plot(title="Apple rolling mean",label="Apple stock price")
    ax.legend(loc="upper left")
    ax.set_xlabel("dates")
    ax.set_ylabel("Prices")
    rm_apple = data_frame["AAPL"].rolling(window=10).mean()
    rm_apple.plot(label="Rolling mean",ax=ax)
    ax.legend()
    plt.savefig("graphs/apple.png")
    

if __name__=="__main__":
    main()
    
       
    
    
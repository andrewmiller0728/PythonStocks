'''
    AUTHORED:
        Name:   Andrew Miller
        Date:   2021-26-02

    RESOURCES:
        Yahoo Finance (yfinance):
            Documentation:  https://pypi.org/project/yfinance/
            Tutorial:       https://aroussi.com/post/python-yahoo-finance
            GitHub:         https://github.com/ranaroussi/yfinance
        Datetime:
            Documenation:   https://docs.python.org/3/library/datetime.html
        Pandas DataFrame:
            Documentation:  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
'''
 

''' [ IMPORTS ] '''

import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.animation as animation


''' [ TIMES ] '''

tzEST = dt.timezone(offset=dt.timedelta(hours=-5))
dtNow = dt.datetime.now(tz=tzEST)
dtMarketOpen = dt.datetime(year=dtNow.year, month=dtNow.month, day=dtNow.day, hour=9, minute=30, second=0, tzinfo=tzEST)
dtMarketClose = dt.datetime(year=dtNow.year, month=dtNow.month, day=dtNow.day, hour=16, minute=0, second=0, tzinfo=tzEST)


''' [ STONKS ] '''

def getStockHistory(stockSymbol):
    return yf.Ticker(stockSymbol).history(interval="2m", start=dtMarketOpen, end=dtMarketClose).to_records()

def getStockCount(symbols):
    count = 0
    for row in symbols:
        count += len(row)
    return count

stonks = [["GME", "AMC"], ["MSFT", "NOK"]]


''' [ DATA ] '''

def getStockData(stockHistory):
    stockData = {
        "datetimes": [],
        "opens": [],
        "highs": [],
        "lows": [],
        "closes": [],
        "volumes": [],
        "ohlc": [],
        "ohlcAverages": []
    }
    for row in stockHistory:
        stockData["datetimes"].append(row[0])
        stockData["opens"].append(row[1])
        stockData["highs"].append(row[2])
        stockData["lows"].append(row[3])
        stockData["closes"].append(row[4])
        stockData["volumes"].append(row[5])
        ohlcData = [row[1], row[2], row[3], row[4]]
        stockData["ohlc"].append(ohlcData)
        stockData["ohlcAverages"].append(sum(ohlcData) / len(ohlcData))
    return stockData


''' [ PLOTS ] '''

def makeOHLCBoxplot(stockData) :
    darkred = "#FF0000"
    lightred = "#FFAAAA"
    darkgreen = "#00FF00"
    lightgreen = "#AAFFAA"
    darkgray = "#EEEEEE"
    lightgray = "#AAAAAA"
    xticks = []
    xlabels = []
    for i in range(0, len(stockData["datetimes"])) :
        currColors = []

        if stockData["opens"][i] > stockData["closes"][i]:
            currColors = [darkred, lightred]
        elif stockData["opens"][i] < stockData["closes"][i]:
            currColors = [darkgreen, lightgreen]
        else:
            currColors = [darkgray, lightgray]

        boxplotStock = plt.boxplot(stockData["ohlc"][i], positions=[i], patch_artist=True, showfliers=False)
        for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(boxplotStock[element], color=currColors[0])
        for patch in boxplotStock['boxes']:
            patch.set(facecolor=currColors[1])

        tempTime = str(stockData["datetimes"][i]).split("T")[1].split(".")[0].split(":")
        if (int(tempTime[0]) % 1 == 0 and int(tempTime[1]) == 0):
            xticks.append(i)
            xlabels.append(format("%d:%s") % (int(tempTime[0]) - 5, tempTime[1]))
    plt.xticks(xticks, xlabels)

figname = format("StockValues_%s_" % (str(dtNow.date())))
for row in stonks:
    for symbol in row:
        figname += symbol + "_"
plt.figure(figname, figsize=(16, 10))

index = 1
for i in range(len(stonks)):
    for j in range(len(stonks[i])):
        plt.subplot(len(stonks[i]), len(stonks), index)
        plt.title(stonks[i][j] + " Stock Values " + str(dtNow.date()))
        plt.xlabel("Time")
        plt.ylabel("Value")
        makeOHLCBoxplot(getStockData(getStockHistory(stonks[i][j])))
        index += 1

plt.subplots_adjust(wspace=0.25, hspace=0.5)

# plt.show()
plt.savefig(figname + ".png")
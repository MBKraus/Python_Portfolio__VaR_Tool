# Python_Portfolio__VaR_Tool

## Python-based risk management tool which sources data from Yahoo Finance and calculates different types of Value-at-Risk (VaR) metrics and many other risk/return characteristics both on an individual stock and portfolio-basis, stand-alone and vs. a benchmark of choice (constructed with wxPython)

This wxPython Notebook-app / widget allows one to retrieve stock / index data from Yahoo Finance through Pandas Datareader which are in turn combined with initial portfolio weights and a benchmark of choice to calculate the following risk / return metrics:

<br>

 - Historic returns (annual & daily - both an individual stock-, benchmark- and portfolio basis)
 - Historic standard deviation of returns (annual & daily - both an individual stock-, benchmark- and portfolio basis)
 - Annual Sharpe ratios (both an individual stock-, benchmark- and portfolio basis)
 - Beta's (both an individual stock-, benchmark- and portfolio basis)
 - Ex-post tracking error vs. the benchmark of choice
 - Daily return histograms on an individual stock- and portfolio basis
 - Indexed performance charts on an individual stock- and portfolio basis
 
 - 5% (daily) Historical Simulation Value-at-Risk (VaR) on an individual stock- and portfolio basis
 - 5% (daily) Variance-Covariance Value-at-Risk (VaR) on an individual stock- and portfolio basis
 - 5% (daily) Monte Carlo simulated (along Geometric Brownian Motion) Value-at-Risk (VaR) on an individual stock basis

 - stock return correlation heatmap
 <br>
 
In addition, the data retrieved from Yahoo Finance can be exported in CSV-format through the checkbox on the MainFrame.

#### Screenshot MainFrame
![alt text](https://github.com/Weesper1985/Python_Portfolio__VaR_Tool/blob/master/Main3.png)

Please note - this app requires the following packages / modules in order to function properly:

- [Python 3.5.1](https://www.python.org/downloads/release/python-351/)
- [wxPython 4.0.0b2](https://www.wxpython.org/pages/downloads/)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)
- [WxLibPubSub](https://wiki.wxpython.org/WxLibPubSub)
- [Numpy and Scipy](https://docs.scipy.org/doc/)
- [fix-yahoo-finance](https://pypi.org/project/fix-yahoo-finance/)

#### Screenshot Value-at-Risk data
![alt text](https://github.com/Weesper1985/Python_Portfolio__VaR_Tool/blob/master/Tab22.png)

#### Screenshot Descriptive Data
![alt text](https://github.com/Weesper1985/Python_Portfolio__VaR_Tool/blob/master/Tab11.png)

#### Screenshot Correlation heatmap
![alt text](https://github.com/Weesper1985/Python_Portfolio__VaR_Tool/blob/master/Tab33.png)

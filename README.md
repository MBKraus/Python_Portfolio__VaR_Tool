# Python_Portfolio__VaR_Tool

## Python-based portfolio / stock widget(app) which sources data from Yahoo Finance and calculates Value-at-Risk (VaR) estimates and many other risk/return characteristics both on an individual stock and portfolio-basis (constructed with wxPython)

This app allows one to retrieve stock / index data from Yahoo Finance through Pandas Datareader which are in turn combined with portfolio weights to calculate the following risk / return metrics:

 - Expected returns (annual & daily - both an individual stock- and portfolio basis)
 - Expected standard deviation of returns (annual & daily - both an individual stock- and portfolio basis)
 - Annual Sharpe ratios (both an individual stock and portfolio basis)
 - Daily return histograms on an individual stock- basis
 - Adjusted price charts on an individual stock- basis
 
 - 5% Historical Simulation Value-at-Risk (VaR) estimates on an individual stock- and portfolio basis
 - 5% Variance-Covariance Value-at-Risk (VaR) estimates on an individual stock- and portfolio basis
 - 5% Monte Carlo simulated (along Geometric Brownian Motion) Value-at-Risk (VaR) estimates on an individual stock basis
 
 - stock return correlation matrix
 
In addition, the data retrieved from Yahoo Finance can be exported in CSV-format through the checkbox on the MainFrame.

#### Screenshot MainFrame
![alt text](https://raw.githubusercontent.com/Weesper1985/Python_Portfolio__VaR_Tool/blob/master/Main.png)

Please note - this app requires the following packages / modules in order to function properly:

- [Python 3.5.1](https://www.python.org/downloads/release/python-351/)
- [wxPython 4.0.0b2](https://www.wxpython.org/pages/downloads/)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)
- [WxLibPubSub](https://wiki.wxpython.org/WxLibPubSub)
- [Numpy and Scipy](https://docs.scipy.org/doc/)

#### Screenshot Descriptive Data
![alt text](https://raw.githubusercontent.com/Weesper1985/Python_Portfolio__VaR_Tool/blob/master/Tab1.png)

#### Screenshot Value-at-Risk data
![alt text](https://raw.githubusercontent.com/Weesper1985/Python_Portfolio__VaR_Tool/blob/master/Tab2.png)

#### Screenshot Correlation matrix
![alt text](https://raw.githubusercontent.com/Weesper1985/Python_Portfolio__VaR_Tool/blob/master/Tab3.png)

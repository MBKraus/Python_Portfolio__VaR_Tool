
import datetime
import pandas as pd
from pandas.tseries.offsets import BDay
import pandas_datareader.data as web
import numpy as np
import math
import matplotlib as plt
import matplotlib.dates as mdates
from matplotlib import cm as cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import re
import scipy.stats
import time
import wx.lib.pubsub
from wx.lib.pubsub import pub
import wx

# First tab

class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Set first tab input fields + button

        fontbold = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        title = wx.StaticText(self, wx.ID_ANY, 'Portfolio Tool')
        title.SetFont(fontbold)

        stock_a_label = wx.StaticText(self, -1, "Ticker Stock A", (20, 20))
        stock_b_label = wx.StaticText(self, -1, "Ticker Stock B", (20, 20))
        stock_c_label = wx.StaticText(self, -1, "Ticker Stock C", (20, 20))
        stock_d_label = wx.StaticText(self, -1, "Ticker Stock D", (20, 20))

        self.stock_a_ticker_input = wx.TextCtrl(self, size=(60, -1))
        self.stock_b_ticker_input = wx.TextCtrl(self, size=(60, -1))
        self.stock_c_ticker_input = wx.TextCtrl(self, size=(60, -1))
        self.stock_d_ticker_input = wx.TextCtrl(self, size=(60, -1))

        stock_a_weight_label = wx.StaticText(self, -1, "Initial weight Stock A", (20, 20))
        stock_b_weight_label= wx.StaticText(self, -1, "Initial weight Stock B", (20, 20))
        stock_c_weight_label = wx.StaticText(self, -1, "Initial weight Stock C", (20, 20))
        stock_d_weight_label = wx.StaticText(self, -1, "Initial weight Stock D", (20, 20))

        self.stock_a_weight_input = wx.TextCtrl(self, size=(60, -1))
        self.stock_b_weight_input = wx.TextCtrl(self, size=(60, -1))
        self.stock_c_weight_input = wx.TextCtrl(self, size=(60, -1))
        self.stock_d_weight_input = wx.TextCtrl(self, size=(60, -1))

        timeseries_label = wx.StaticText(self, -1, "Time series from: [dd/mm/yyyy]", (20, 20))
        self.timeseries_input = wx.TextCtrl(self, size=(85, -1))

        benchmark_label = wx.StaticText(self, -1, "Benchmark", (20, 20))
        self.benchmark_input = wx.TextCtrl(self, size=(85, -1))

        background_a = wx.StaticText(self, -1, "> Stock weights should be decimals (i.e. 40% = 0.4)", (20, 20))
        background_a.SetForegroundColour(wx.BLUE)

        self.export = wx.CheckBox(self, label = 'Export data to CSV')

        button = wx.Button(self, label="Retrieve data",)
        self.Bind(wx.EVT_BUTTON, self.onRETRIEVE, button)

        # Put all of the above in a Sizer

        self.warning = wx.StaticText(self, -1, "", (20, 20))

        sizer = wx.GridBagSizer(10, 15)

        sizer.Add(title, (1, 0))

        sizer.Add(stock_a_label, (3, 0))
        sizer.Add(stock_b_label, (4, 0))
        sizer.Add(stock_c_label, (5, 0))
        sizer.Add(stock_d_label, (6, 0))

        sizer.Add(self.stock_a_ticker_input, (3, 2))
        sizer.Add(self.stock_b_ticker_input, (4, 2))
        sizer.Add(self.stock_c_ticker_input, (5, 2))
        sizer.Add(self.stock_d_ticker_input, (6, 2))

        sizer.Add(stock_a_weight_label, (3, 5))
        sizer.Add(stock_b_weight_label, (4, 5))
        sizer.Add(stock_c_weight_label, (5, 5))
        sizer.Add(stock_d_weight_label, (6, 5))

        sizer.Add(self.stock_a_weight_input, (3, 7))
        sizer.Add(self.stock_b_weight_input, (4, 7))
        sizer.Add(self.stock_c_weight_input, (5, 7))
        sizer.Add(self.stock_d_weight_input, (6, 7))

        sizer.Add(timeseries_label, (3, 9))
        sizer.Add(self.timeseries_input, (3, 11))

        sizer.Add(benchmark_label, (4, 9))
        sizer.Add(self.benchmark_input, (4, 11))

        sizer.Add(background_a, (5, 9))

        sizer.Add(self.export, (8, 9))

        sizer.Add(button, (9, 0))

        sizer.Add(self.warning, (11, 0))

        self.border = wx.BoxSizer()
        self.border.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(self.border)

    def onRETRIEVE(self, event):

        # Get input values

        stock_a_ticker = self.stock_a_ticker_input.GetValue()
        stock_b_ticker = self.stock_b_ticker_input.GetValue()
        stock_c_ticker = self.stock_c_ticker_input.GetValue()
        stock_d_ticker = self.stock_d_ticker_input.GetValue()

        stock_a_weight = self.stock_a_weight_input.GetValue()
        stock_b_weight = self.stock_b_weight_input.GetValue()
        stock_c_weight = self.stock_c_weight_input.GetValue()
        stock_d_weight = self.stock_d_weight_input.GetValue()

        stocks = [stock_a_ticker, stock_b_ticker, stock_c_ticker, stock_d_ticker, ]

        # Check if the date was inserted correctly

        try:

            datetime.datetime.strptime(self.timeseries_input.GetValue(), '%d/%m/%Y')

            # Check if all stock weights are floats

            if re.match("^\d+?\.\d+?$", stock_a_weight) is None or re.match("^\d+?\.\d+?$", stock_b_weight) is None or re.match("^\d+?\.\d+?$", stock_c_weight) is None or re.match("^\d+?\.\d+?$", stock_d_weight) is None:

                self.warning.SetLabel("Stock weight should be a digit")

                # Check whether all fields are populated

            elif any(x == '' for x in stocks) or any(x == None for x in stocks) or self.benchmark_input.GetValue() == '':

                self.warning.SetLabel("One or more inputs are missing. Please insert all required values")

            else:

                weights = np.asarray([float(stock_a_weight), float(stock_b_weight), float(stock_c_weight), float(stock_d_weight), ])

                # Check whether the portfolio weights sum up to 1

                if sum(weights) != 1:

                    self.warning.SetLabel("Portfolio weights should sum up to 1")

                else:

                    try:

                        self.warning.SetLabel("")

                        # Get stock data

                        data = web.DataReader(stocks, data_source='yahoo', start= self.timeseries_input.GetValue())['Adj Close']

                        data.sort_index(inplace=True, ascending=True)
                        data.index = pd.to_datetime(data.index)

                        time.sleep(5)

                        # Get benchmark data

                        benchmark = web.DataReader(self.benchmark_input.GetValue(), data_source='yahoo', start=self.timeseries_input.GetValue())['Adj Close']

                        benchmark.sort_index(inplace=True, ascending=True)
                        benchmark.index = pd.to_datetime(benchmark.index)

                        # Calculate headline metrics

                        returns = data.pct_change().dropna()
                        mean_daily_returns = returns.mean()
                        std = returns.std()

                        benchmark_returns = benchmark.pct_change().dropna()
                        benchmark_std = benchmark_returns.std()

                        # Create headers

                        mean_daily_return_label = wx.StaticText(self, -1, "Historical mean daily return (%)", (20, 20))
                        expected_annual_return_label = wx.StaticText(self, -1, "Historical annual return (%)", (20, 20))
                        daily_std_label = wx.StaticText(self, -1, "Hist. standard deviation (%, daily)", (20, 20))
                        annual_std_label = wx.StaticText(self, -1, "Hist. standard Deviation (%, annual)", (20, 20))
                        sharpe_label = wx.StaticText(self, -1, "Hist. Sharpe Ratio (annual)", (20, 20))
                        TE_label = wx.StaticText(self, -1, "Ex-post Tracking Error", (20, 20))
                        Beta_label = wx.StaticText(self, -1, "Beta", (20, 20))

                        stock_a_header = wx.StaticText(self, -1, str(stocks[0]), (20, 20))
                        stock_b_header = wx.StaticText(self, -1, str(stocks[1]), (20, 20))
                        stock_c_header = wx.StaticText(self, -1, str(stocks[2]), (20, 20))
                        stock_d_header = wx.StaticText(self, -1, str(stocks[3]), (20, 20))
                        portfolio_header = wx.StaticText(self, -1, "Portfolio", (20, 20))
                        benchmark_header = wx.StaticText(self, -1, "Benchmark("+self.benchmark_input.GetValue()+")", (20, 20))

                        # Calculate basis for portfolio metrics

                        positions = {}
                        positions[stocks[0]] = {returns[stocks[0]].index[0]: float(stock_a_weight)}
                        positions[stocks[1]] = {returns[stocks[1]].index[0]: float(stock_b_weight)}
                        positions[stocks[2]] = {returns[stocks[2]].index[0]: float(stock_c_weight)}
                        positions[stocks[3]] = {returns[stocks[3]].index[0]: float(stock_d_weight)}

                        pos = pd.DataFrame.from_dict(positions).reindex(returns.index).fillna(method="ffill")
                        portfolio = pos.shift() * (1 + returns).cumprod(axis=0)
                        portfolio['total_wealth'] = portfolio[[stocks[0], stocks[1], stocks[2], stocks[3]]].sum(axis=1)
                        portfolio.index = pd.to_datetime(portfolio.index)
                        date = datetime.datetime.strptime(self.timeseries_input.GetValue(), "%d/%m/%Y")
                        start_date = date + BDay(1)
                        portfolio.at[start_date, 'total_wealth'] = 1
                        portfolio["returns"] = portfolio['total_wealth'].pct_change()

                        # Calculate + insert specific stock, benchmark and portfolio metrics

                        stock_a_mean_daily_return = wx.StaticText(self, -1, str(round(mean_daily_returns[stocks[0]]*100, 2)), (20, 20))
                        stock_b_mean_daily_return = wx.StaticText(self, -1, str(round(mean_daily_returns[stocks[1]]*100, 2)), (20, 20))
                        stock_c_mean_daily_return = wx.StaticText(self, -1, str(round(mean_daily_returns[stocks[2]]*100, 2)), (20, 20))
                        stock_d_mean_daily_return = wx.StaticText(self, -1, str(round(mean_daily_returns[stocks[3]]*100, 2)), (20, 20))
                        portfolio_mean_daily_return = portfolio["returns"].mean()
                        portfolio_mean_daily_return_scr = wx.StaticText(self, -1, str(round(portfolio_mean_daily_return * 100, 2)), (20, 20))
                        benchmark_mean_daily_return = wx.StaticText(self, -1, str(round(benchmark_returns.mean() * 100, 2)), (20, 20))

                        stock_a_annual_return = wx.StaticText(self, -1, str(round(mean_daily_returns[stocks[0]]*100*252, 2)), (20, 20))
                        stock_b_annual_return = wx.StaticText(self, -1, str(round(mean_daily_returns[stocks[1]]*100*252, 2)), (20, 20))
                        stock_c_annual_return = wx.StaticText(self, -1, str(round(mean_daily_returns[stocks[2]]*100*252, 2)), (20, 20))
                        stock_d_annual_return = wx.StaticText(self, -1, str(round(mean_daily_returns[stocks[3]]*100*252, 2)), (20, 20))
                        portfolio_annual_return = wx.StaticText(self, -1, str(round(portfolio_mean_daily_return  * 100 * 252, 2)), (20, 20))
                        benchmark_annual_return = wx.StaticText(self, -1, str(round(benchmark_returns.mean()  * 100 * 252, 2)), (20, 20))

                        stock_a_daily_std = wx.StaticText(self, -1, str(round(std[stocks[0]]*100, 2)), (20, 20))
                        stock_b_daily_std = wx.StaticText(self, -1, str(round(std[stocks[1]]*100, 2)), (20, 20))
                        stock_c_daily_std = wx.StaticText(self, -1, str(round(std[stocks[2]]*100, 2)), (20, 20))
                        stock_d_daily_std = wx.StaticText(self, -1, str(round(std[stocks[3]]*100, 2)), (20, 20))
                        portfolio_daily_std = portfolio["returns"].std()
                        portfolio_daily_std_scr = wx.StaticText(self, -1, str(round(portfolio_daily_std * 100, 2)), (20, 20))
                        benchmark_daily_std = wx.StaticText(self, -1, str(round(benchmark_std * 100, 2)), (20, 20))

                        stock_a_annual_std = wx.StaticText(self, -1, str(round(std[stocks[0]] * 100 * np.sqrt(252), 2)), (20, 20))
                        stock_b_annual_std = wx.StaticText(self, -1, str(round(std[stocks[1]] * 100 * np.sqrt(252), 2)), (20, 20))
                        stock_c_annual_std = wx.StaticText(self, -1, str(round(std[stocks[2]] * 100 * np.sqrt(252), 2)), (20, 20))
                        stock_d_annual_std = wx.StaticText(self, -1, str(round(std[stocks[3]] * 100 * np.sqrt(252), 2)), (20, 20))
                        portfolio_annual_std = wx.StaticText(self, -1, str(round(portfolio_daily_std * 100 * np.sqrt(252), 2)), (20, 20))
                        benchmark_annual_std = wx.StaticText(self, -1, str(round(benchmark_std * 100 * np.sqrt(252), 2)), (20, 20))

                        risk_free_rate = 2.25 # 10 year US-treasury rate (annual)

                        sharpe_a = ((mean_daily_returns[stocks[0]] * 100 * 252) -  risk_free_rate ) / (std[stocks[0]] * 100 * np.sqrt(252))
                        sharpe_b = ((mean_daily_returns[stocks[1]] * 100 * 252) - risk_free_rate) / (std[stocks[1]] * 100 * np.sqrt(252))
                        sharpe_c = ((mean_daily_returns[stocks[2]] * 100 * 252) - risk_free_rate) / (std[stocks[2]] * 100 * np.sqrt(252))
                        sharpe_d = ((mean_daily_returns[stocks[3]] * 100 * 252) - risk_free_rate) / (std[stocks[3]] * 100 * np.sqrt(252))
                        sharpe_portfolio = ((portfolio_mean_daily_return * 100 * 252) - risk_free_rate) / (portfolio_daily_std * 100 * np.sqrt(252))
                        sharpe_benchmark = ((benchmark_returns.mean() * 100 * 252) - risk_free_rate) / (benchmark_std * 100 * np.sqrt(252))

                        sharpe_a_scr = wx.StaticText(self, -1, str(round(sharpe_a, 2)),(20, 20))
                        sharpe_b_scr = wx.StaticText(self, -1, str(round(sharpe_b, 2)), (20, 20))
                        sharpe_c_scr = wx.StaticText(self, -1, str(round(sharpe_c, 2)), (20, 20))
                        sharpe_d_scr = wx.StaticText(self, -1, str(round(sharpe_d, 2)), (20, 20))
                        sharpe_portfolio_scr = wx.StaticText(self, -1, str(round(sharpe_portfolio, 2)), (20, 20))
                        sharpe_benchmark_scr = wx.StaticText(self, -1, str(round(sharpe_benchmark, 2)), (20, 20))

                        TE_a = (returns[stocks[0]] - benchmark.pct_change().dropna()).std()
                        TE_b = (returns[stocks[1]] - benchmark.pct_change().dropna()).std()
                        TE_c = (returns[stocks[2]] - benchmark.pct_change().dropna()).std()
                        TE_d = (returns[stocks[3]] - benchmark.pct_change().dropna()).std()
                        TE_p = (portfolio["returns"] - benchmark.pct_change().dropna()).std()

                        TE_stock_a = wx.StaticText(self, -1, str(round(TE_a * 100, 2)), (20, 20))
                        TE_stock_b = wx.StaticText(self, -1, str(round(TE_b * 100, 2)), (20, 20))
                        TE_stock_c = wx.StaticText(self, -1, str(round(TE_c * 100, 2)), (20, 20))
                        TE_stock_d = wx.StaticText(self, -1, str(round(TE_d * 100, 2)), (20, 20))
                        TE_portfolio = wx.StaticText(self, -1, str(round(TE_p * 100, 2)), (20, 20))

                        beta_a = (np.cov(returns[stocks[0]], benchmark_returns)[0][1]) / benchmark_returns.var()
                        beta_b = (np.cov(returns[stocks[1]], benchmark_returns)[0][1]) / benchmark_returns.var()
                        beta_c = (np.cov(returns[stocks[2]], benchmark_returns)[0][1]) / benchmark_returns.var()
                        beta_d = (np.cov(returns[stocks[3]], benchmark_returns)[0][1]) / benchmark_returns.var()
                        beta_p = (np.cov(portfolio["returns"].dropna(), benchmark_returns.iloc[1:])[0][1]) / benchmark_returns.var()

                        beta_a_lab = wx.StaticText(self, -1, str(round(beta_a, 2)), (20, 20))
                        beta_b_lab = wx.StaticText(self, -1, str(round(beta_b, 2)), (20, 20))
                        beta_c_lab = wx.StaticText(self, -1, str(round(beta_c, 2)), (20, 20))
                        beta_d_lab = wx.StaticText(self, -1, str(round(beta_d, 2)), (20, 20))
                        beta_p_lab = wx.StaticText(self, -1, str(round(beta_p, 2)), (20, 20))

                        # Put all the metrics in a Sizer

                        sizer = wx.GridBagSizer(10, 10)

                        sizer.Add(mean_daily_return_label, (12, 0))
                        sizer.Add(expected_annual_return_label, (13, 0))
                        sizer.Add(daily_std_label, (14, 0))
                        sizer.Add(annual_std_label, (15, 0))
                        sizer.Add(sharpe_label, (16, 0))
                        sizer.Add(TE_label, (17, 0))
                        sizer.Add(Beta_label, (18, 0))

                        sizer.Add(stock_a_header, (11, 2))
                        sizer.Add(stock_b_header, (11, 4))
                        sizer.Add(stock_c_header, (11, 6))
                        sizer.Add(stock_d_header, (11, 8))
                        sizer.Add(portfolio_header, (11, 11))
                        sizer.Add(benchmark_header, (11, 13))

                        sizer.Add(stock_a_mean_daily_return, (12, 2))
                        sizer.Add(stock_b_mean_daily_return, (12, 4))
                        sizer.Add(stock_c_mean_daily_return, (12, 6))
                        sizer.Add(stock_d_mean_daily_return, (12, 8))
                        sizer.Add(portfolio_mean_daily_return_scr, (12, 11))
                        sizer.Add(benchmark_mean_daily_return, (12, 13))

                        sizer.Add(stock_a_annual_return, (13, 2))
                        sizer.Add(stock_b_annual_return, (13, 4))
                        sizer.Add(stock_c_annual_return, (13, 6))
                        sizer.Add(stock_d_annual_return, (13, 8))
                        sizer.Add(portfolio_annual_return, (13, 11))
                        sizer.Add(benchmark_annual_return, (13, 13))

                        sizer.Add(stock_a_daily_std, (14, 2))
                        sizer.Add(stock_b_daily_std, (14, 4))
                        sizer.Add(stock_c_daily_std, (14, 6))
                        sizer.Add(stock_d_daily_std, (14, 8))
                        sizer.Add(portfolio_daily_std_scr, (14, 11))
                        sizer.Add(benchmark_daily_std, (14, 13))

                        sizer.Add(stock_a_annual_std, (15, 2))
                        sizer.Add(stock_b_annual_std, (15, 4))
                        sizer.Add(stock_c_annual_std, (15, 6))
                        sizer.Add(stock_d_annual_std, (15, 8))
                        sizer.Add(portfolio_annual_std, (15, 11))
                        sizer.Add(benchmark_annual_std, (15, 13))

                        sizer.Add(sharpe_a_scr, (16, 2))
                        sizer.Add(sharpe_b_scr, (16, 4))
                        sizer.Add(sharpe_c_scr, (16, 6))
                        sizer.Add(sharpe_d_scr, (16, 8))
                        sizer.Add(sharpe_portfolio_scr, (16, 11))
                        sizer.Add(sharpe_benchmark_scr, (16, 13))

                        sizer.Add(TE_stock_a, (17, 2))
                        sizer.Add(TE_stock_b, (17, 4))
                        sizer.Add(TE_stock_c, (17, 6))
                        sizer.Add(TE_stock_d, (17, 8))
                        sizer.Add(TE_portfolio, (17, 11))

                        sizer.Add(beta_a_lab, (18, 2))
                        sizer.Add(beta_b_lab, (18, 4))
                        sizer.Add(beta_c_lab, (18, 6))
                        sizer.Add(beta_d_lab, (18, 8))
                        sizer.Add(beta_p_lab, (18, 11))

                        self.border = wx.BoxSizer()
                        self.border.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)

                        self.SetSizerAndFit(self.border)

                        # Make the headline data available to the other tabs by means of PubSub

                        pub.sendMessage("panelListener", arg1 = data, arg2 = weights, arg3 = stocks, arg4 = portfolio)

                        # Export price-date from Yahoo to CSV if box is ticked

                        if self.export.GetValue() == True:

                            data.to_csv("data"+stock_a_ticker+"to"+stock_d_ticker+".csv", sep=';', encoding='utf-8')

                        else:
                            pass

                    except Exception as e:

                        self.warning.SetLabel(str(e))

        except ValueError:

            self.warning.SetLabel("Date not in the right format")

# Second tab

class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        pub.subscribe(self.myListener, "panelListener")

    def myListener(self, arg1, arg2, arg3, arg4):

        # import variables

        data_2 = arg1
        stocks_2 = arg3
        portfolio_2 = arg4

        portfolio_2.rename(columns={'returns': 'Portfolio',}, inplace=True)

        returns = data_2.pct_change().dropna()

        # Create histogram of daily returns

        figure_1 = Figure(figsize=(7, 2.5))
        canvas_1 = FigureCanvas(self, -1, figure_1)

        axes_1 = figure_1.add_subplot(111)
        axes_2 = figure_1.add_subplot(111)
        axes_3 = figure_1.add_subplot(111)
        axes_4 = figure_1.add_subplot(111)
        axes_5 = figure_1.add_subplot(111)

        axes_1.hist(returns[stocks_2[0]], bins=50, normed=True, histtype='stepfilled', alpha=0.5)
        axes_2.hist(returns[stocks_2[1]], bins=50, normed=True, histtype='stepfilled', alpha=0.5)
        axes_3.hist(returns[stocks_2[2]], bins=50, normed=True, histtype='stepfilled', alpha=0.5)
        axes_4.hist(returns[stocks_2[3]], bins=50, normed=True, histtype='stepfilled', alpha=0.5)
        axes_5.hist(portfolio_2["Portfolio"].dropna(), bins=50, normed=True, histtype='stepfilled', alpha=0.5)
        axes_1.set_title(u"Historic return distribution", weight='bold')
        axes_1.legend(loc='upper left')

        # Create indexed performance chart

        figure_2 = Figure(figsize=(7, 2.5))
        canvas_2 = FigureCanvas(self, -1, figure_2)

        axes_A = figure_2.add_subplot(111)
        axes_B = figure_2.add_subplot(111)
        axes_C = figure_2.add_subplot(111)
        axes_D = figure_2.add_subplot(111)
        axes_E = figure_2.add_subplot(111)

        years = mdates.YearLocator()
        yearsFmt = mdates.DateFormatter("'%y")

        ret_index = (1 + returns).cumprod()
        portfolio_cum = (1 + portfolio_2["Portfolio"].dropna()).cumprod()

        axes_A.plot(ret_index.index, ret_index[stocks_2[0]])
        axes_A.xaxis.set_major_locator(years)
        axes_A.xaxis.set_major_formatter(yearsFmt)

        axes_B.plot(ret_index.index, ret_index[stocks_2[1]])
        axes_B.xaxis.set_major_locator(years)
        axes_B.xaxis.set_major_formatter(yearsFmt)

        axes_C.plot(ret_index.index, ret_index[stocks_2[2]])
        axes_C.xaxis.set_major_locator(years)
        axes_C.xaxis.set_major_formatter(yearsFmt)

        axes_D.plot(ret_index.index, ret_index[stocks_2[3]])
        axes_D.xaxis.set_major_locator(years)
        axes_D.xaxis.set_major_formatter(yearsFmt)

        axes_E.plot(portfolio_cum.index, portfolio_cum)
        axes_E.xaxis.set_major_locator(years)
        axes_E.xaxis.set_major_formatter(yearsFmt)

        axes_A.set_title(u" Indexed Performance (base = 1)", weight='bold')
        axes_A.legend(loc='upper left')

        sizer = wx.GridBagSizer(7, 2.5)
        sizer.Add(canvas_1, (1, 0))
        sizer.Add(canvas_2, (2, 0))

        self.border = wx.BoxSizer()
        self.border.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(self.border)

# Third tab

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        pub.subscribe(self.myListener, "panelListener")

    def myListener(self, arg1, arg2, arg3, arg4):

        fontbold = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        # import variables

        data_3 = arg1
        stocks_3 = arg3
        weights_3 = arg2
        portfolio_3 = arg4

        returns = data_3.pct_change().dropna()

        mean_daily_returns = returns.mean()
        std = returns.std()

        # Calculate daily 5% Historical Simulation VaR for individual stocks and portfolio

        title_historical = wx.StaticText(self, wx.ID_ANY, 'VaR - Historical Simulation')
        title_historical.SetFont(fontbold)

        stock_a_hist_var_lab = wx.StaticText(self, -1, str(stocks_3[0]) + " - Daily VaR (5%)", (20, 20))
        stock_b_hist_var_lab = wx.StaticText(self, -1, str(stocks_3[1]) + " - Daily VaR (5%)", (20, 20))
        stock_c_hist_var_lab = wx.StaticText(self, -1, str(stocks_3[2]) + " - Daily VaR (5%)", (20, 20))
        stock_d_hist_var_lab = wx.StaticText(self, -1, str(stocks_3[3]) + " - Daily VaR (5%)", (20, 20))
        portfolio_hist_var_lab = wx.StaticText(self, -1, "Portfolio - Daily VaR (5%)", (20, 20))

        stock_a_hist_var = wx.StaticText(self, -1, str(round(returns[stocks_3[0]].quantile(0.05) * 100, 2)), (20, 20))
        stock_b_hist_var = wx.StaticText(self, -1, str(round(returns[stocks_3[1]].quantile(0.05) * 100, 2)), (20, 20))
        stock_c_hist_var = wx.StaticText(self, -1, str(round(returns[stocks_3[2]].quantile(0.05) * 100, 2)), (20, 20))
        stock_d_hist_var = wx.StaticText(self, -1, str(round(returns[stocks_3[3]].quantile(0.05) * 100, 2)), (20, 20))

        portfolio_hist_ret = portfolio_3["returns"].dropna()
        portfolio_hist_var = wx.StaticText(self, -1, str(round(portfolio_hist_ret.quantile(0.05) * 100, 2)), (20, 20))

        # Calculate daily 5% Variance-Covariance VaR for individual stocks and portfolio

        title_varcov = wx.StaticText(self, wx.ID_ANY, 'VaR - Variance Covariance')
        title_varcov.SetFont(fontbold)

        stock_a_cov_var_lab = wx.StaticText(self, -1, str(stocks_3[0]) + " - Daily VaR (5%)", (20, 20))
        stock_b_cov_var_lab = wx.StaticText(self, -1, str(stocks_3[1]) + " - Daily VaR (5%)", (20, 20))
        stock_c_cov_var_lab = wx.StaticText(self, -1, str(stocks_3[2]) + " - Daily VaR (5%)", (20, 20))
        stock_d_cov_var_lab = wx.StaticText(self, -1, str(stocks_3[3]) + " - Daily VaR (5%)", (20, 20))

        stock_a_cov_var = wx.StaticText(self, -1, str(round(scipy.stats.norm.ppf(0.05, mean_daily_returns[stocks_3[0]], std[stocks_3[0]]) * 100, 2)))
        stock_b_cov_var = wx.StaticText(self, -1, str(round(scipy.stats.norm.ppf(0.05, mean_daily_returns[stocks_3[1]], std[stocks_3[1]]) * 100, 2)))
        stock_c_cov_var = wx.StaticText(self, -1, str(round(scipy.stats.norm.ppf(0.05, mean_daily_returns[stocks_3[2]], std[stocks_3[2]]) * 100, 2)))
        stock_d_cov_var = wx.StaticText(self, -1, str(round(scipy.stats.norm.ppf(0.05, mean_daily_returns[stocks_3[3]], std[stocks_3[3]]) * 100, 2)))

        portfolio_return_daily = portfolio_3["returns"].dropna().mean()
        portfolio_std = portfolio_3["returns"].dropna().std()

        portfolio_cov_var_lab = wx.StaticText(self, -1, "Portfolio - Daily VaR (5%)", (20, 20))
        portfolio_cov_var = wx.StaticText(self, -1, str(round(scipy.stats.norm.ppf(0.05, portfolio_return_daily, portfolio_std) * 100, 2)))

        # Calculate 5% Monte Carlo Sim Daily VaR for individual stocks - along Geometric Brownian Motion

        title_MC = wx.StaticText(self, wx.ID_ANY, 'VaR - Monte Carlo (along Geometric Brownian Motion')
        title_MC.SetFont(fontbold)

        MC_return =[]

        for item in range(len(stocks_3)):

            result = []

            S = data_3[stocks_3[item]].iloc[-1]
            T = 252
            mu = returns[stocks_3[item]].mean()*252
            vol = returns[stocks_3[item]].std()*np.sqrt(252)

            for i in range(1000):

                daily_returns = np.random.normal(mu/T,vol/math.sqrt(T),T)+1

                price_list = [S]

                price_list.append(price_list[-1] * daily_returns)

                result.append(price_list[-1])

            MC_return.append((np.percentile(result,5) - S) / S)

        stock_a_MC_lab = wx.StaticText(self, -1, str(stocks_3[0]) + " - Daily VaR (5%)", (20, 20))
        stock_b_MC_lab = wx.StaticText(self, -1, str(stocks_3[1]) + " - Daily VaR (5%)", (20, 20))
        stock_c_MC_lab = wx.StaticText(self, -1, str(stocks_3[2]) + " - Daily VaR (5%)", (20, 20))
        stock_d_MC_lab = wx.StaticText(self, -1, str(stocks_3[3]) + " - Daily VaR (5%)", (20, 20))

        stock_a_MC = wx.StaticText(self, -1, str(round(MC_return[0] * 100, 2)), (20, 20))
        stock_b_MC = wx.StaticText(self, -1, str(round(MC_return[1] * 100, 2)), (20, 20))
        stock_c_MC = wx.StaticText(self, -1, str(round(MC_return[2] * 100, 2)), (20, 20))
        stock_d_MC = wx.StaticText(self, -1, str(round(MC_return[3] * 100, 2)), (20, 20))

        MC_assumptions_lab = wx.StaticText(self, -1, "Monte Carlo - Assumptions", (20, 20))

        MC_assumption_1 = wx.StaticText(self, -1, "Geometric Brownian Motion", (20, 20))
        MC_assumption_2 = wx.StaticText(self, -1, "N = 1000", (20, 20))
        MC_assumption_3 = wx.StaticText(self, -1, "μ = mean daily stock return (i.e. drift)", (20, 20))
        MC_assumption_4 = wx.StaticText(self, -1, "σ = standard deviation of returns", (20, 20))

        MC_assumption_1.SetForegroundColour(wx.BLUE)
        MC_assumption_2.SetForegroundColour(wx.BLUE)
        MC_assumption_3.SetForegroundColour(wx.BLUE)
        MC_assumption_4.SetForegroundColour(wx.BLUE)

        # Put all metrics in a Sizer

        sizer = wx.GridBagSizer(10, 15)

        sizer.Add(title_historical, (1, 0))

        sizer.Add(stock_a_hist_var_lab, (3, 0))
        sizer.Add(stock_b_hist_var_lab, (4, 0))
        sizer.Add(stock_c_hist_var_lab, (5, 0))
        sizer.Add(stock_d_hist_var_lab, (6, 0))
        sizer.Add(portfolio_hist_var_lab, (8, 0))

        sizer.Add(stock_a_hist_var, (3, 1))
        sizer.Add(stock_b_hist_var, (4, 1))
        sizer.Add(stock_c_hist_var, (5, 1))
        sizer.Add(stock_d_hist_var, (6, 1))
        sizer.Add(portfolio_hist_var, (8, 1))

        sizer.Add(title_varcov, (10, 0))

        sizer.Add(stock_a_cov_var_lab, (12, 0))
        sizer.Add(stock_b_cov_var_lab, (13, 0))
        sizer.Add(stock_c_cov_var_lab, (14, 0))
        sizer.Add(stock_d_cov_var_lab, (15, 0))
        sizer.Add(portfolio_cov_var_lab, (17, 0))

        sizer.Add(stock_a_cov_var, (12, 1))
        sizer.Add(stock_b_cov_var, (13, 1))
        sizer.Add(stock_c_cov_var, (14, 1))
        sizer.Add(stock_d_cov_var, (15, 1))
        sizer.Add(portfolio_cov_var, (17, 1))

        sizer.Add(title_MC, (1, 8))

        sizer.Add(stock_a_MC_lab, (3, 8))
        sizer.Add(stock_b_MC_lab, (4, 8))
        sizer.Add(stock_c_MC_lab, (5, 8))
        sizer.Add(stock_d_MC_lab, (6, 8))

        sizer.Add(stock_a_MC, (3, 9))
        sizer.Add(stock_b_MC, (4, 9))
        sizer.Add(stock_c_MC, (5, 9))
        sizer.Add(stock_d_MC, (6, 9))

        sizer.Add(MC_assumptions_lab, (8, 8))
        sizer.Add(MC_assumption_1, (10, 8))
        sizer.Add(MC_assumption_2, (11, 8))
        sizer.Add(MC_assumption_3, (12, 8))
        sizer.Add(MC_assumption_4, (13, 8))

        self.border = wx.BoxSizer()
        self.border.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(self.border)

# Fourth tab

class PageFour(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        pub.subscribe(self.myListener, "panelListener")

    def myListener(self, arg1, arg2, arg3, arg4):

        # Import variables

        data_4 = arg1

        returns = data_4.pct_change().dropna()

        # Construct correlation matrix

        figure_3 = Figure(figsize=(6, 4))
        canvas_3 = FigureCanvas(self, -1, figure_3)

        axes_E = figure_3.add_subplot(111)

        axes_E.pcolor(returns.corr(), cmap=plt.cm.Blues)
        axes_E.set_xticks(np.arange(5)+0.5)  # center x ticks
        axes_E.set_yticks(np.arange(5)+0.5)  # center y ticks
        axes_E.set_xticklabels(returns.columns)
        axes_E.set_yticklabels(returns.columns)

        sizer = wx.GridBagSizer(7, 2.5)
        sizer.Add(canvas_3, (1, 0))

        self.border = wx.BoxSizer()
        self.border.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(self.border)

# MainFrame

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Portfolio Tool")

        # Wraps it all up and put everything together

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        page1 = PageOne(nb)
        page2 = PageTwo(nb)
        page3 = PageThree(nb)
        page4 = PageFour(nb)

        nb.AddPage(page1, "Portfolio Data")
        nb.AddPage(page2, "Descriptive Data +")
        nb.AddPage(page3, "VAR")
        nb.AddPage(page4, "Correlation Matrix")

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


if __name__ == "__main__":

    app = wx.App()
    frame = MainFrame()
    frame.SetSize(0, 0, 1200, 750)
    frame.Center()
    frame.Show()
    app.MainLoop()
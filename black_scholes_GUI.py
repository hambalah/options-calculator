import sys
import math
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class OptionCalculator:
    def __init__(self):
        self.r = None
        self.sigma = None
        self.d = None
        
    def get_latest_price_and_data(self, ticker):
        ticker = yf.Ticker(ticker)
        try:
            latest_price = ticker.history(period="1d")['Close'].values[0]
            prices_df = yf.download(ticker, period="1d")
            return round(latest_price, 2), prices_df
        except Exception as e:
            return None, None
        
    def is_valid_date(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def get_volatility(ticker, start_date, end_date):
        # check date format is valid
        if not OptionCalculator.is_valid_date(start_date) or not OptionCalculator.is_valid_date(end_date):
            return None
        if start_date > end_date:
            return None
        
        try:
            prices_df = yf.download(ticker, start=start_date, end=end_date)
        except Exception as e:
            return None
            
        # filter out NaN values
        returns_df = prices_df[['Adj Close']].pct_change()
        returns_df = returns_df.dropna()
        days_count = len(returns_df) 
        
        # lambda function alternative
        # filtered_returns = list(filter(lambda x: not any(pd.isna(x)), returns_df.values))
        # days_count = len(filtered_returns)

        
        # alternative
        # filtered_rows = map(lambda row: row if not any(pd.isna(row)) else None, returns_df.values)
        # valid_rows = filter(lambda x: x is not None, filtered_rows)
        # returns_df = pd.DataFrame(next(zip(*valid_rows)), columns=['Adj Close'])
        # days_count = len(returns_df) 

        annualized_vol = returns_df.std() * np.sqrt(days_count)
        annualized_vol = annualized_vol['Adj Close']

        return round(annualized_vol, 2)

    def get_stock_price_chart(self, ticker, prices_df):
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        prices_df['Adj Close'].plot(
            style='r-', linewidth=1, ax=ax)
        ax.set_title('Stock Price Chart of ' + ticker)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.grid(True)
        
        return fig
    
    def set_input_values(self, inputs):
        for var_name in ['r', 'sigma', 'd']:
            if var_name in inputs:
                setattr(self, var_name, inputs[var_name] / 100)
                
        # list comprehension
        # [setattr(self, var_name, inputs[var_name] / 100) for var_name in ['r', 'sigma', 'd'] if var_name in inputs]
        
    def calculate_option_price(self, inputs):
        self.set_input_values(inputs)
        S, K, T = (
            inputs['S'],
            inputs['K'],
            inputs['T']       
        )

        d1 = (math.log(S / K) + (self.r - self.d + (self.sigma ** 2) / 2) * T) / (self.sigma * (T ** 0.5))
        d2 = d1 - self.sigma * (T ** 0.5)

        call_price = S * math.e**(-self.d * T) * norm.cdf(d1) - K * math.e**(-self.r * T) * norm.cdf(d2)
        put_price = K * math.e**(-self.r * T) * norm.cdf(-d2) - S * math.e**(-self.d * T) * norm.cdf(-d1)

        return (round(call_price, 2), round(put_price, 2))
    

# main GUI class
qtCreatorFile = "black_scholes_calc.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_GetPrice.clicked.connect(self.GetPrice)
        self.pushButton_GetVolatility.clicked.connect(self.GetVolatility)        
        self.pushButton_Calculate.clicked.connect(self.Calculate)
        self.pushButton_Reset.clicked.connect(self.reset_fields)
        self.option_calculator = OptionCalculator()
        self.chart_widget = None

    def GetPrice(self):
        ticker = self.lineEdit_Ticker.text()
        latest_price, prices_df = self.option_calculator.get_latest_price_and_data(ticker)
        if latest_price is not None:
            self.lineEdit_SpotPrice.setText(str(round(latest_price, 2)))
        else:
            self.lineEdit_SpotPrice.clear()
            self.show_error('Error Retrieving Price', 'Please check ticker symbol and try again.')
        
        # show chart
        if prices_df is not None:
            chart_figure = self.option_calculator.get_stock_price_chart(ticker, prices_df)
            # remove existing chart widget if any
            if self.chart_widget:
                self.chart_widget.setParent(None)
            # create new QWidget to display chart
            self.chart_widget = FigureCanvas(chart_figure)
            self.layout().addWidget(self.chart_widget)

    def GetVolatility(self): 
        ticker = self.lineEdit_Ticker.text()
        start_date = self.lineEdit_StartDate.text()
        end_date = self.lineEdit_EndDate.text()
        volatility = self.option_calculator.get_volatility(ticker, start_date, end_date)
        if volatility is not None:
            self.lineEdit_Volatility.setText(str(volatility))
        else:
            self.lineEdit_Volatility.clear()
            self.show_error('Error Calculating Volatility', 'Please check date format or ticker symbol and try again.')
        
    def Calculate(self):
        inputs = {
            'S': float(self.lineEdit_SpotPrice.text()),
            'K': float(self.lineEdit_StrikePrice.text()),
            'T': float(self.lineEdit_TimetoExpiry.text()),
            'r': float(self.lineEdit_InterestRate.text()),
            'sigma': float(self.lineEdit_Volatility.text()),
            'd': float(self.lineEdit_Dividend.text())
        }
        call_price, put_price = self.option_calculator.calculate_option_price(inputs)
        self.lineEdit_CallPrice.setText(str(call_price))
        self.lineEdit_PutPrice.setText(str(put_price))

    def reset_fields(self):
        self.lineEdit_SpotPrice.clear()
        self.lineEdit_StrikePrice.clear()
        self.lineEdit_TimetoExpiry.clear()
        self.lineEdit_InterestRate.clear()
        self.lineEdit_Volatility.clear()
        self.lineEdit_Dividend.clear()
        self.lineEdit_CallPrice.clear()
        self.lineEdit_PutPrice.clear()
        
    def show_error(self, title, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.showMessage(message)
        error_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

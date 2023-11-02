import sys
from math import log, sqrt, exp
import yfinance as yf
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from scipy.stats import norm

class OptionCalculator:
    def get_latest_price(self, ticker):
        ticker = yf.Ticker(ticker)
        latest_price = ticker.history(period="1d")['Close'][0]
        return round(latest_price, 2)
        
    """Black Scholes"""
    def blackscholes_eur(self, inputs):
        S, K, T, r, q, sigma = (
            inputs['S'],
            inputs['K'],
            inputs['T'],
            inputs['r'],
            inputs['q'],
            inputs['sigma']
        )
        
        d1 = (log(S / K) + (r - q + (sigma ** 2) / 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt (T)
        
        call_price = S * exp(-q * T) * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        put_price = K * exp(-r * T) * norm.cdf(-d2) - S * exp(-q * T) * norm.cdf(-d1)

        return (round(call_price, 2), round(put_price, 2))
    
    """Binomial Tree"""
    def binom_amer(self, inputs):
        S, K, T, r, q, sigma = (
            inputs['S'],
            inputs['K'],
            inputs['T'],
            inputs['r'],
            inputs['q'],
            inputs['sigma']
        )
        N = 100 # no. of time steps
        dt= T/N
        u = exp(sigma * sqrt(dt))
        d = 1/u
        p = (exp((r-q) * dt) - d) / (u-d)    

        # create a 2D list using for-loop, for call prices
        fc = []
        for i in range(N+1):
            inner_list = []
            for j in range(i+1):
                inner_list.append(0)
            fc.append(inner_list)

        # create a 2D list using list comprehension, for put prices       
        fp = [[0 for j in range(0,i+1)] for i in range(0,N+1)]

        # calculate option prices at expiration (N)
        for j in range(N+1):
            fc[N][j] = max(0, S * u**j * d**(N-j) - K)
            fp[N][j] = max(0, K - S * u**j *d**(N-j))
        
        # work backwards to calculate option prices at earlier time steps
        for i in range(N-1, -1, -1):
            for j in range(i + 1):
                fc[i][j] = max(S * u**j * d**(i-j) - K, exp(-r*dt) * (p * fc[i+1][j+1] + (1-p) * fc[i+1][j]))
                fp[i][j] = max(K - S * u**j * d**(i-j), exp(-r*dt) * (p * fp[i+1][j+1] + (1-p) * fp[i+1][j]))
                
        return (round(fc[0][0], 2), round(fp[0][0], 2))

"""Main GUI Class"""
qtCreatorFile = "options_calc.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.radioButton_European.clicked.connect(self.European)
        self.radioButton_American.clicked.connect(self.American)
        self.pushButton_GetPrice.clicked.connect(self.GetPrice)
        self.pushButton_Calculate.clicked.connect(self.Calculate)
        self.pushButton_Reset.clicked.connect(self.reset_fields)
        self.option_calculator = OptionCalculator()
        self.chart_widget = None

    def European(self):
        self.optionType = 'European'
        self.textBrowser_CalcMethod.setText("Black Scholes")
        
    def American(self):
        self.optionType = 'American'
        self.textBrowser_CalcMethod.setText("Binomial Tree")
        
    def GetPrice(self):
        ticker = self.lineEdit_Ticker.text()
        latest_price = self.option_calculator.get_latest_price(ticker)
        self.lineEdit_SpotPrice.setText(str(latest_price))
        
    def Calculate(self):
        inputs = {
            'S': float(self.lineEdit_SpotPrice.text()),
            'K': float(self.lineEdit_StrikePrice.text()),
            'T': float(self.lineEdit_TimetoExpiry.text()),
            'r': float(self.lineEdit_InterestRate.text()) / 100,
            'q': float(self.lineEdit_Dividend.text()) / 100,
            'sigma': float(self.lineEdit_Volatility.text()) / 100
        }
        
        if self.optionType == 'European':
            call_price, put_price = self.option_calculator.blackscholes_eur(inputs)
        elif self.optionType == 'American':
            call_price, put_price = self.option_calculator.binom_amer(inputs)
        self.textBrowser_CallPrice.setText(str(call_price))
        self.textBrowser_PutPrice.setText(str(put_price))

    def reset_fields(self):
        self.lineEdit_Ticker.clear()
        self.lineEdit_SpotPrice.clear()
        self.lineEdit_StrikePrice.clear()
        self.lineEdit_TimetoExpiry.clear()
        self.lineEdit_InterestRate.clear()
        self.lineEdit_Volatility.clear()
        self.lineEdit_Dividend.clear()
        self.textBrowser_CallPrice.clear()
        self.textBrowser_PutPrice.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
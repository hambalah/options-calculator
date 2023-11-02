import sys
import math
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from scipy.stats import norm

qtCreatorFile = "black_scholes_calc.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

def calculate_option_price(S, K, T, r, sigma, d):
        r /= 100
        sigma /= 100
        d /= 100
        
        # for loop
        # variables_to_adjust = [r, sigma, d]
        # for variable in variables_to_adjust:
        #     variable /= 100
        
        # list comprehension
        # r, sigma, d = [var / 100 for var in (r, sigma, d)]

        d1 = (math.log(S / K) + (r - d + (sigma ** 2) / 2) * T) / (sigma * (T ** 0.5))
        d2 = d1 - sigma * (T ** 0.5)

        call_price = S * math.e**(-d * T) * norm.cdf(d1) - K * math.e**(-r * T) * norm.cdf(d2)
        put_price = K * math.e**(-r * T) * norm.cdf(-d2) - S * math.e**(-d * T) * norm.cdf(-d1)

        return (round(call_price, 2), round(put_price, 2))
        
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_Calculate.clicked.connect(self.Calculate)
        self.pushButton_Reset.clicked.connect(self.reset_fields)

    def Calculate(self):
        S = float(self.lineEdit_SpotPrice.text())
        K = float(self.lineEdit_StrikePrice.text())
        T = float(self.lineEdit_TimetoExpiry.text())
        r = float(self.lineEdit_InterestRate.text())
        sigma = float(self.lineEdit_Volatility.text())
        d = float(self.lineEdit_Dividend.text())
        
        call_price, put_price = calculate_option_price(S, K, T, r, sigma, d)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
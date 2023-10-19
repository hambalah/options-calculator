import sys
import math
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from scipy.stats import norm

qtCreatorFile = "black_scholes_calc.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_Calculate.clicked.connect(self.calculate_option_price)
        self.pushButton_Reset.clicked.connect(self.reset_fields)

    def calculate_option_price(self):
        S = float(self.lineEdit_SpotPrice.text())
        K = float(self.lineEdit_StrikePrice.text())
        T = float(self.lineEdit_TimetoExpiry.text())
        r = float(self.lineEdit_InterestRate.text()) / 100
        sigma = float(self.lineEdit_Volatility.text()) / 100
        d = float(self.lineEdit_Dividend.text()) / 100

        d1 = (math.log(S / K) + (r - d + (sigma ** 2) / 2) * T) / (sigma * (T ** 0.5))
        d2 = d1 - sigma * (T ** 0.5)

        call_price = S * math.e**(-d * T) * norm.cdf(d1) - K * math.e**(-r * T) * norm.cdf(d2)
        put_price = K * math.e**(-r * T) * norm.cdf(-d2) - S * math.e**(-d * T) * norm.cdf(-d1)

        self.lineEdit_CallPrice.setText(f"{call_price:.2f}")
        self.lineEdit_CallPrice_2.setText(f"{put_price:.2f}")

    def reset_fields(self):
        self.lineEdit_SpotPrice.clear()
        self.lineEdit_StrikePrice.clear()
        self.lineEdit_TimetoExpiry.clear()
        self.lineEdit_InterestRate.clear()
        self.lineEdit_Volatility.clear()
        self.lineEdit_Dividend.clear()
        self.lineEdit_CallPrice.clear()
        self.lineEdit_CallPrice_2.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

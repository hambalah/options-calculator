import tkinter as tk
from tkinter import ttk
from scipy.stats import norm
import math

def calculate_option_price():
    S = float(spot_price_entry.get())
    K = float(strike_price_entry.get())
    T = float(time_to_expiry_entry.get())
    r = float(interest_rate_entry.get())
    sigma = float(volatility_entry.get())
    d = float(dividend_yield_entry.get())

    d1 = (math.log(S / K) + (r - d + (sigma ** 2) / 2) * T) / (sigma * (T ** 0.5))
    d2 = d1 - sigma * (T ** 0.5)

    call_price = S * math.e**(-d * T) * norm.cdf(d1) - K * math.e**(-r * T) * norm.cdf(d2)
    put_price = K * math.e**(-r * T) * norm.cdf(-d2) - S * math.e**(-d * T) * norm.cdf(-d1)

    call_result_label.config(text=f"Call Option Price: {call_price:.2f}")
    put_result_label.config(text=f"Put Option Price: {put_price:.2f}")

    
def reset_fields():
    spot_price_entry.delete(0, tk.END)
    strike_price_entry.delete(0, tk.END)
    time_to_expiry_entry.delete(0, tk.END)
    volatility_entry.delete(0, tk.END)
    interest_rate_entry.delete(0, tk.END)
    dividend_yield_entry.delete(0, tk.END)
    call_result_label.config(text="Call Option Price:")
    put_result_label.config(text="Put Option Price:")
    
app = tk.Tk()
app.title("Options Price Calculator")
app.geometry("400x300")

spot_price_label = ttk.Label(app, text="Spot Price:")
spot_price_label.grid(row=0, column=0)
spot_price_entry = ttk.Entry(app)
spot_price_entry.grid(row=0, column=1)

strike_price_label = ttk.Label(app, text="Strike Price:")
strike_price_label.grid(row=1, column=0)
strike_price_entry = ttk.Entry(app)
strike_price_entry.grid(row=1, column=1)

time_to_expiry_label = ttk.Label(app, text="Time to Expiry (years):")
time_to_expiry_label.grid(row=2, column=0)
time_to_expiry_entry = ttk.Entry(app)
time_to_expiry_entry.grid(row=2, column=1)

volatility_label = ttk.Label(app, text="Volatility (as a decimal):")
volatility_label.grid(row=3, column=0)
volatility_entry = ttk.Entry(app)
volatility_entry.grid(row=3, column=1)

interest_rate_label = ttk.Label(app, text="Interest Rate (as a decimal):")
interest_rate_label.grid(row=4, column=0)
interest_rate_entry = ttk.Entry(app)
interest_rate_entry.grid(row=4, column=1)

dividend_yield_label = ttk.Label(app, text="Dividend Yield (as a decimal):")
dividend_yield_label.grid(row=5, column=0)
dividend_yield_entry = ttk.Entry(app)
dividend_yield_entry.grid(row=5, column=1)

calculate_button = ttk.Button(app, text="Calculate", command=calculate_option_price)
calculate_button.grid(row=6, column=1, sticky="se", padx=10, pady=10)
calculate_button.config(width=20)

reset_button = ttk.Button(app, text="Reset", command=reset_fields)
reset_button.grid(row=7, column=1, sticky="se", padx=10, pady=10)
reset_button.config(width=20)

call_result_label = ttk.Label(app, text="Call Option Price:", font=("Helvetica", 14))
call_result_label.grid(row=0, column=2, columnspan=2, rowspan=3, sticky="ne")
put_result_label = ttk.Label(app, text="Put Option Price:", font=("Helvetica", 14))
put_result_label.grid(row=3, column=2, columnspan=2, rowspan=3, sticky="ne")


app.mainloop()

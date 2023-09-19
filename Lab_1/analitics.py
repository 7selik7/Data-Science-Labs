# from scrapper import scrap_file
# from datetime import datetime
# import tkinter as tk
# from tkinter import ttk
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#
# def show_chart():
#     data = scrap_file(create_file=False)
#
#     dates = [datetime.strptime(d['date'], '%d.%m.%Y').date() for d in data]
#     inflation_values = [float(d['actual_inflation'].replace('%', '').replace(',', '.')) for d in data]
#     print(inflation_values)
#
#     root = tk.Tk()
#     root.title("Dollar inflation chart")
#
#     fig, ax = plt.subplots(figsize=(8, 4))
#     ax.plot(dates, inflation_values, marker='o', linestyle='-', color='black', markersize=3)
#     ax.set_xlabel("Date")
#     ax.set_ylabel("Inflation")
#     plt.xticks(rotation=45)
#     ax.grid(True)
#
#     canvas = FigureCanvasTkAgg(fig, master=root)
#     canvas_widget = canvas.get_tk_widget()
#     canvas_widget.pack()
#
#     root.mainloop()
#
# a = int(input())
#
# if a == 1:
#     show_chart()
# if a == 2:
#     print('trend')

import numpy as np
from scrapper import scrap_file
from datetime import datetime, timedelta
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = scrap_file(create_file=False)
data = data[::-1]
dates = [datetime.strptime(d['date'], '%d.%m.%Y').date() for d in data]
inflation_values = [float(d['actual_inflation'].replace('%', '').replace(',', '.')) for d in data]

root = tk.Tk()
root.title("Dollar inflation chart with trend")

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(dates, inflation_values, marker='o', linestyle='-', color='black', markersize=4)
ax.set_xlabel("Date")
ax.set_ylabel("Inflation")
plt.xticks(rotation=45)
ax.grid(True)

x_values = np.arange(len(dates))

degree = 15
coefficients = np.polyfit(x_values, inflation_values, degree)
polynomial = np.poly1d(coefficients)
print(polynomial)
trend_values = polynomial(x_values)

ax.plot(dates, trend_values, linestyle='--', color='blue', label=f'Trend (degree={degree})')
ax.legend()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

root.mainloop()
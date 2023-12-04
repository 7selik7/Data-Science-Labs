import json

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import tkinter as tk
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV

from Lab_1.analitics import generate_and_analyze_synthetic_data, analyze_real_data


def evaluate_anomaly_detection_performance(parsed_inflation_values, cleaned_inflation_values):
    mse = mean_squared_error(parsed_inflation_values[:len(cleaned_inflation_values)], cleaned_inflation_values)
    rmse = np.sqrt(mse)
    return mse, rmse


if __name__ == '__main__':
    with open('../outputs/output.json', 'r') as file:
        json_data = file.read()

    data = json.loads(json_data)
    data = data[::-1]
    parsed_dates = [datetime.strptime(d['date'], '%d.%m.%Y').date() for d in data]
    parsed_inflation_values = [float(d['actual_inflation'].replace('%', '').replace(',', '.')) for d in data]

    root = tk.Tk()
    root.title("Dollar inflation chart with trend")

    # ______________________________________Parsed Data______________________________________
    frame1 = tk.Frame(root)
    frame1.grid(row=0, column=0)

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(parsed_dates, parsed_inflation_values, marker='o', linestyle='-', color='black', markersize=4,
             label='Parsed Data')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Inflation")
    plt.xticks(rotation=45)
    ax1.grid(True)
    plt.legend()
    plt.title("Dollar Inflation Chart (Parsed)")

    canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
    canvas_widget1 = canvas1.get_tk_widget()
    canvas_widget1.pack()

    frame2 = tk.Frame(root)
    frame2.grid(row=0, column=1)

    # ______________________________________Cleaned Data______________________________________
    X = np.array(parsed_inflation_values).reshape(-1, 1)
    Y = np.arange(len(parsed_dates))

    # _____________________________Find best values for cleaning_______________________________
    clf = IsolationForest()
    contamination_values = np.arange(0.05, 0.3, 0.05)
    param_grid = {'contamination': contamination_values}

    grid_search = GridSearchCV(clf, param_grid, cv=5, scoring='neg_mean_squared_error')

    grid_search.fit(X, Y)

    best_params = grid_search.best_params_
    print("Кращі параметри для очистки функції:", best_params)

    best_contamination = best_params['contamination']
    clf = IsolationForest(contamination=0.5)
    outliers = clf.fit_predict(X)

    cleaned_dates = [parsed_dates[i] for i in range(len(parsed_dates)) if outliers[i] == 1]
    cleaned_inflation_values = [parsed_inflation_values[i] for i in range(len(parsed_inflation_values)) if
                                outliers[i] == 1]

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(cleaned_dates, cleaned_inflation_values, marker='o', linestyle='-', color='blue', markersize=4,
             label='Cleaned Data')
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Inflation")
    plt.xticks(rotation=45)
    ax2.set_ylim(-2, 8)
    ax2.grid(True)
    plt.legend()
    plt.title("Dollar Inflation Chart (Cleaned)")

    canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
    canvas_widget2 = canvas2.get_tk_widget()
    canvas_widget2.pack()

    # ______________________________________Synthetic Data______________________________________
    frame3 = tk.Frame(root)
    frame3.grid(row=1, column=0, columnspan=2)

    synthetic_trend_values, synthetic_inflation_values = generate_and_analyze_synthetic_data(
        dates=cleaned_dates,
        real_inflation_values=cleaned_inflation_values,
        is_printed=False,
        predict=True,
        degree=3,
    )
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.plot(cleaned_dates, synthetic_inflation_values, marker='x', linestyle='--', color='red', markersize=4,
             label='Synthetic Data')
    ax3.plot(cleaned_dates, synthetic_trend_values, linestyle='--', color='blue',
             label='Synthetic Trend')
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Inflation")
    plt.xticks(rotation=45)
    ax3.grid(True)
    plt.legend()
    plt.title("Dollar Inflation Chart (Synthetic)")

    canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
    canvas_widget3 = canvas3.get_tk_widget()
    canvas_widget3.pack()

    analyze_real_data(dates=parsed_dates, real_inflation_values=parsed_inflation_values)
    mse, rmse = evaluate_anomaly_detection_performance(parsed_inflation_values, cleaned_inflation_values)

    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    root.mainloop()

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import tkinter as tk


def analyze_real_data(dates: list, real_inflation_values: list) -> None:
    real_mean_inflation = np.mean(real_inflation_values)
    real_std_deviation_inflation = np.std(real_inflation_values)
    real_median_inflation = np.median(real_inflation_values)
    real_min_inflation = np.min(real_inflation_values)
    real_max_inflation = np.max(real_inflation_values)
    real_variance_inflation = np.var(real_inflation_values)

    print("Real Data Statistics:")
    print("Mean inflation value:", real_mean_inflation)
    print("Standard deviation of inflation:", real_std_deviation_inflation)
    print("Median inflation:", real_median_inflation)
    print("Minimum inflation value:", real_min_inflation)
    print("Maximum inflation value:", real_max_inflation)
    print("Inflation variance:", real_variance_inflation)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, real_inflation_values, marker='o', linestyle='-', color='black', markersize=4)
    ax.set_xlabel("Date")
    ax.set_ylabel("Inflation")
    plt.xticks(rotation=45)
    ax.grid(True)


def generate_and_analyze_synthetic_data(dates: list, real_inflation_values: list, is_printed: bool, predict: bool,
                                        degree=15) -> tuple:
    noise_std = 0.2

    np.random.seed(0)
    coefficients = np.polyfit(np.arange(len(dates)), real_inflation_values, degree)
    if predict:
        last_date = max(dates)
        additional_dates = [last_date + timedelta(days=30 * i) for i in range(1, 41)]
        dates += additional_dates
        synthetic_trend_values = np.polyval(coefficients, np.arange(len(dates)))
    else:
        synthetic_trend_values = np.polyval(coefficients, np.arange(len(dates)))
    print("\nModel:")
    print(np.poly1d(coefficients))
    synthetic_inflation_values = synthetic_trend_values + np.random.normal(0, noise_std, len(dates))

    # Use this if you want to create anomaly
    # anomaly_index = 20
    # anomaly_value = 10.0
    # synthetic_inflation_values[anomaly_index] = anomaly_value

    if is_printed:
        synthetic_mean_inflation = np.mean(synthetic_inflation_values)
        synthetic_std_deviation_inflation = np.std(synthetic_inflation_values)
        synthetic_median_inflation = np.median(synthetic_inflation_values)
        synthetic_min_inflation = np.min(synthetic_inflation_values)
        synthetic_max_inflation = np.max(synthetic_inflation_values)
        synthetic_variance_inflation = np.var(synthetic_inflation_values)

        print("\nSynthetic Data Statistics:")
        print("Mean inflation value:", synthetic_mean_inflation)
        print("Standard deviation of inflation:", synthetic_std_deviation_inflation)
        print("Median inflation:", synthetic_median_inflation)
        print("Minimum inflation value:", synthetic_min_inflation)
        print("Maximum inflation value:", synthetic_max_inflation)
        print("Inflation variance:", synthetic_variance_inflation)

    return synthetic_trend_values, synthetic_inflation_values


if __name__ == '__main__':
    from scrapper import scrap_file
    data = scrap_file(create_file=False)
    data = data[::-1]
    parsed_dates = [datetime.strptime(d['date'], '%d.%m.%Y').date() for d in data]
    parsed_inflation_values = [float(d['actual_inflation'].replace('%', '').replace(',', '.')) for d in data]

    root = tk.Tk()
    root.title("Dollar inflation chart with trend")

    frame1 = tk.Frame(root)
    frame1.pack()

    analyze_real_data(dates=parsed_dates, real_inflation_values=parsed_inflation_values)

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
    frame2.pack()

    synthetic_trend_values, synthetic_inflation_values = generate_and_analyze_synthetic_data(
        dates=parsed_dates,
        real_inflation_values=parsed_inflation_values)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(parsed_dates, synthetic_inflation_values, marker='x', linestyle='--', color='red', markersize=4,
             label='Synthetic Data')
    ax2.plot(parsed_dates, synthetic_trend_values, linestyle='--', color='blue', label='Synthetic Trend')
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Inflation")
    plt.xticks(rotation=45)
    ax2.grid(True)
    plt.legend()
    plt.title("Dollar Inflation Chart (Synthetic)")

    canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
    canvas_widget2 = canvas2.get_tk_widget()
    canvas_widget2.pack()

    root.mainloop()
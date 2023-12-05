import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_data(file_path):
    data_sheet = pd.read_excel(file_path)
    all_columns = list(data_sheet.columns[1:-1])
    return data_sheet, all_columns


def calculate_normalized_matrix(data_sheet, all_columns):
    num_products = len(all_columns)
    num_params = data_sheet.shape[0]

    criteria_matrix = np.zeros((num_params, num_products))
    normalized_matrix = np.zeros((num_params, num_products))

    for product in range(num_products):
        for criterion in range(num_params):
            criteria_matrix[criterion][product] = data_sheet[all_columns[product]][criterion]

    sum_criteria = np.sum(criteria_matrix, axis=1)
    for i in range(num_params):
        normalized_matrix[i] = criteria_matrix[i] / sum_criteria[i]

    return normalized_matrix


def calculate_integral(normalized_matrix):
    num_params, num_products = normalized_matrix.shape

    weights = np.ones(num_params)
    weights_normalized = weights / np.sum(weights)

    integral = np.zeros(num_products)
    for i in range(num_params):
        integral += weights_normalized[i] * (1 - normalized_matrix[i]) ** (-1)

    return integral


def find_optimal_product(integral):
    optimal_product = np.argmax(integral)
    return optimal_product + 1


def plot_integro_bar_chart(x, integral):
    plt.figure(figsize=(10, 6))
    plt.bar(x, integral, color='#4bb2c5')
    plt.xlabel('Products')
    plt.ylabel('Integro')
    plt.title('Integro for each product')
    plt.show()


def plot_3d_bar_chart(criteria_matrix):
    num_params, num_products = criteria_matrix.shape
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    for i in range(num_params):
        xs = np.arange(num_products)
        ys = np.full((num_products,), i)
        zs = criteria_matrix[i]
        ax.bar(xs, zs, zs=i, zdir='y', color=np.random.rand(3, ))

    ax.set_xlabel('Products')
    ax.set_ylabel('Criterias')
    ax.set_zlabel('Values')
    plt.title('3D Bar chart for criteria values')
    plt.show()


if __name__ == "__main__":
    file_path = "input.xlsx"

    data_sheet, all_columns = read_data(file_path)
    print(f"Data sheet\n{data_sheet}\n\n All columns\n {all_columns}")
    normalized_matrix = calculate_normalized_matrix(data_sheet, all_columns)
    print(f"Normilized matrix \n {normalized_matrix}")
    integral = calculate_integral(normalized_matrix)
    optimal_product = find_optimal_product(integral)

    x = np.arange(len(all_columns))

    print('The best product - ', optimal_product)

    plot_integro_bar_chart(x, integral)
    plot_3d_bar_chart(normalized_matrix)

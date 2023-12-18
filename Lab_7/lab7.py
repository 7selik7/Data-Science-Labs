import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Зчитування даних з файлу Excel
file_path = 'Data_Set_6.xlsx'
df = pd.read_excel(file_path)

# Заміна "n.a." або інших значень на NaN
df.replace("n.a.", '0', inplace=True)
df.replace("not avilable", '0', inplace=True)

# Конвертація числових значень з формату строк в числовий формат
numeric_columns = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']

df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Групування за SALES_ID та виведення кругової діаграми для всіх унікальних SALES_ID
grouped_by_id = df.groupby('SALES_ID')[numeric_columns].sum()
total_by_id = grouped_by_id.sum(axis=1)

plt.pie(total_by_id, labels=total_by_id.index, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Зміна цін за місяць (за SALES_ID)')
plt.show()

# Групування за SALES_BY_REGION та виведення графіка
grouped_by_region = df.groupby('SALES_BY_REGION')[numeric_columns].sum()
grouped_by_region.T.plot(kind='line', marker='o', figsize=(10, 6))
plt.title('Зміна цін за місяць (за SALES_BY_REGION)')
plt.xlabel('Місяць')
plt.ylabel('Ціна')
plt.legend(title='SALES_BY_REGION')
plt.show()

# Розрахунок загальної суми продажів за кожний місяць та побудова графіка
total_by_month = df[numeric_columns].sum()
total_by_month.plot(kind='bar', figsize=(10, 6), color='skyblue')
plt.title('Загальні продажі за кожен місяць')
plt.xlabel('Місяць')
plt.ylabel('Загальна ціна')
plt.show()

# Знаходження самого прибуткового та неприбуткового місяця
most_profitable_month = total_by_month.idxmax()
least_profitable_month = total_by_month.idxmin()

print(f"Самий прибутковий місяць: {most_profitable_month}")
print(f"Самий неприбутковий місяць: {least_profitable_month}")

# Знаходження самого прибуткового та неприбуткового місця
grouped_by_region = df.groupby('SALES_BY_REGION')[numeric_columns].sum()
total_by_region = grouped_by_region.sum(axis=1)

most_profitable_region = total_by_region.idxmax()
least_profitable_region = total_by_region.idxmin()

print(f"Саме прибуткове місце: {most_profitable_region}")
print(f"Саме неприбуткове місце: {least_profitable_region}")

# Знаходження самого прибуткового та неприбуткового SALES_ID
grouped_by_id = df.groupby('SALES_ID')[numeric_columns].sum()
total_by_id = grouped_by_id.sum(axis=1)

most_profitable_sales_id = total_by_id.idxmax()
least_profitable_sales_id = total_by_id.idxmin()

print(f"Самий прибутковий SALES_ID: {most_profitable_sales_id}")
print(f"Самий неприбутковий SALES_ID: {least_profitable_sales_id}")

features = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER']
target = 'DECEMBER'

# Побудова моделі Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Цикл для прогнозування для кожного рядка в DataFrame
for index, row in df.iterrows():
    # Розділення даних на тренувальний та тестовий набори
    train_df, test_df = train_test_split(df.drop(index), test_size=0.2, random_state=42)
    X_train, y_train = train_df[features].values, train_df[target].values
    X_test = row[features].values.reshape(1, -1)

    # Навчання моделі
    model.fit(X_train, y_train)

    # Прогноз для поточного рядка
    df.at[index, 'PREDICTION_DECEMBER'] = model.predict(X_test)

print(df)

# Групування за SALES_BY_REGION та виведення графіка
grouped_by_region = df.groupby('SALES_BY_REGION')[numeric_columns + ['PREDICTION_DECEMBER']].sum()
grouped_by_region.T.plot(kind='line', marker='o', figsize=(10, 6))
plt.title('Прогнозовані та реальні значення DECEMBER за місяць (за SALES_BY_REGION)')
plt.xlabel('Місяць')
plt.ylabel('Ціна')
plt.legend(title='SALES_BY_REGION')
plt.show()
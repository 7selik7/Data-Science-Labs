import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

np.random.seed(42)
x = np.linspace(0, 4 * np.pi, 8000)
y_true = np.cos(x) + np.random.uniform(-1 * 0.24, 1 * 0.24, len(x))
anomalies = np.random.choice(len(x), int(0.15 * len(x)), replace=False)
y_true[anomalies] += np.random.uniform(-1, 1, len(anomalies))

plt.plot(x, y_true, label='Дійсні дані')
plt.scatter(x[anomalies], y_true[anomalies], c='r', label='Аномалії')
plt.legend()
plt.show()

model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(32),
    tf.keras.layers.Dense(16),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

epochs = 250
history = model.fit(x, y_true, epochs=epochs, verbose=0)

x_pred = np.linspace(0, 4 * np.pi, 1000)

y_pred = model.predict(x_pred)

plt.plot(x, y_true, label='Дійсні дані')
plt.plot(x_pred, y_pred, label='Прогноз')
plt.legend()
plt.show()

plt.plot(history.history['loss'])
plt.title('Залежність втрат від кількості епох навчання')
plt.xlabel('Епохи')
plt.ylabel('Втрати')
plt.show()

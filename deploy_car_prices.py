# Import pandas and numpy libraries
import pandas as pd
import numpy as np
# Import metrics libraries
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# Train and Test split data
from sklearn.model_selection import train_test_split
# Import Model libraries
from xgboost import XGBRegressor

# Import warnings ignore libraries
import warnings as wg
wg.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
# Import Pickle Libraries for converting model to pickle file
import pickle

df = pd.read_csv(r'C:\Users\HP\OneDrive\İş masası\Car Price Predict\car_sales.csv')
del df['Unnamed: 0']
del df['Car/Suv']
del df['Brand']
del df['Car/Suv_1']
del df['Model']
print(df.head())

# Let's define input and target features
y = df['Price']
X = df.drop(columns = ['Price'])

X_train,X_test,y_train,y_test = train_test_split(X,y, random_state = 42, test_size = 0.2)

# Create an XGBoost classifier
model = XGBRegressor(objective ='reg:squarederror', seed=42)  


# Train the model on the training data
model.fit(X_train, y_train)
# Make predictions on the test data
predictions = model.predict(X_test)
# Evaluate the model
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions, squared=False)
r_squared = r2_score(y_test, predictions)
# Print metrics
print('-------------------------------------------------')
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R-squared (Coefficient of Determination): {r_squared}")
print('=================================================')


print(df.columns)

# ['Year', 'UsedOrNew', 'Transmission', 'Engine',
# 'DriveType', 'FuelType', 'FuelConsumption', 'Kilometres', 'Location',
# 'CylindersinEngine', 'BodyType', 'Doors', 'Seats', 'Price']

newdata = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

# Reshape the data to match the input shape expected by the model
newdata = newdata.reshape(1, -1)

# Make predictions
predictions = model.predict(newdata)
print(predictions)


# # Save the model to a pickle file
# with open('model_car.pkl', 'wb') as file:
#     pickle.dump(model, file)

# # Load the model from the pickle file
# with open('model_car.pkl', 'rb') as file:
#     model = pickle.load(file)
from SQLInterface import SQLInterface
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import queries
import pandas as pd

uk_road_safety = SQLInterface('../uk_road_safety.db')
uk_road_safety.execute_from_query_list([queries.query9])

# Create df
df = uk_road_safety.sql_to_pd_df(queries.query9)
print(df.dtypes)

# Drop rows with any NA values in specific columns
df.dropna(subset=['Urban_or_Rural_Area', 'Age_Band_of_Driver',
       'Age_of_Vehicle', 'Engine_Capacity_.CC.', 'Sex_of_Driver','Accident_Severity'], how='any', inplace=True)
print(df)
# Drop rows where data is out of range
index_names = df[(df['Sex_of_Driver']!='Male') & (df['Sex_of_Driver']!='Female')].index
#print("Other genders: "+str(len(index_names))) 
# Encoding and Normalisation 

# Sex of driver to binary 
df['Sex_of_Driver'] = df['Sex_of_Driver'].apply(lambda x: 1 if x == 'Male' else 0)
# Urban and rural to binary 
df['Urban_or_Rural_Area'] = df['Urban_or_Rural_Area'].apply(lambda x: 1 if x == 'Urban' else 0)

# Scale numerical features 
scaler = StandardScaler()
numerical_features = ['Age_of_Vehicle', 'Engine_Capacity_.CC.']
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Label encoding the categorical variable 'Age Band of Driver'
encoder = OneHotEncoder(sparse=False)
# Fit transform to categorical col 
age_band_encoded = encoder.fit_transform(df[['Age_Band_of_Driver']])
# Convert to DataFrame
age_band_df = pd.DataFrame(age_band_encoded, columns=encoder.get_feature_names_out(['Age_Band_of_Driver']))
# Concatenate with original DataFrame
df = pd.concat([df, age_band_df], axis=1)
# Drop the original 'Age_Band_of_Driver' column
df.drop('Age_Band_of_Driver', axis=1, inplace=True)

# Label encoding the categorical variable 'Accident Severity'
encoder = OneHotEncoder(sparse=False)
# Fit transform to categorical col 
accident_severity_encoded = encoder.fit_transform(df[['Accident_Severity']])
# Convert to DataFrame
accident_severity_df = pd.DataFrame(accident_severity_encoded, columns=encoder.get_feature_names_out(['Accident_Severity']))
# Concatenate with original DataFrame
df = pd.concat([df, accident_severity_df], axis=1)
# Drop the original 'Age_Band_of_Driver' column
df.drop(['Accident_Severity','Accident_Severity_nan'], axis=1, inplace=True)


# NAs are getting introduced, drop NAs again
df.dropna(how='any', inplace=True)

# Check df before feature engineering
print(df)

# Select Features
col_list = df.columns
print(col_list)

column_names = ['Urban_or_Rural_Area', 'Age_of_Vehicle',
       'Engine_Capacity_.CC.', 'Sex_of_Driver', 'Age_Band_of_Driver_26 - 35',
       'Age_Band_of_Driver_36 - 45', 'Age_Band_of_Driver_46 - 55',
       'Age_Band_of_Driver_66 - 75']

features = df[column_names]
target = df[['Accident_Severity_Fatal','Accident_Severity_Serious', 'Accident_Severity_Slight']]

# Split df
X_train, X_test, y_train, y_test = train_test_split(features,target, test_size=0.2)

# Building the model (1st attempt)
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32)

# Evaluate the model
loss = model.evaluate(X_test, y_test)

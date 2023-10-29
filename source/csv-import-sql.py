import sqlite3
import pandas as pd 

accidents_df = pd.read_csv('Accident_Information.csv',dtype={'Accident_Index':'string'},on_bad_lines='skip',low_memory=False)
#vehicles_df = pd.read_csv('Vehicle_Information.csv', dtype={'Accident_Index':'string'}, on_bad_lines='skip', low_memory=False)
vehicles_df = None

with open('Vehicle_Information.csv', 'r', encoding='utf-8', errors='replace') as f:
    vehicles_df = pd.read_csv(f)

# create database 
conn = sqlite3.connect('uk_road_safety.db')

# convert to SQL 
accidents_df.to_sql('accidents', conn, if_exists='replace', index=False)
vehicles_df.to_sql('vehicles', conn, if_exists='replace', index=False)



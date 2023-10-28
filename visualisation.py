# Import required library
import sqlite3
import queries
from pandas import DataFrame
import plotly.express as px

def execute_query(query, cursor):
    try:
        cursor.execute(query)

        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        else:
            print("Query executed successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

# Establish database connection
conn = sqlite3.connect('uk_road_safety.db')
cursor = conn.cursor()

# queryList = [queries.query7]

# for query in queryList:
#     print(query)
#     execute_query(query, cursor)
#     conn.commit()

# while True:
#     # Get SQL query from user
#     user_query = input("Enter your SQL query (or type 'exit' to quit): ")
    
#     if user_query.lower() == 'exit':
#         break
    
#     # Execute the query
#     execute_query(user_query, db_ref)
    
#     # Commit changes
#     conn.commit()


cursor.execute(queries.query7)
rows = cursor.fetchall()
df = DataFrame(rows)
df.columns = ['Accident Number', 'Year']
print(df)
df.to_csv("accidentnoperyear.csv")

# Close connection
conn.close()


# Plot accident counts per year
fig = px.line(df, x='Year', y='Accident Number', title='Accidents per Year')
fig.show()

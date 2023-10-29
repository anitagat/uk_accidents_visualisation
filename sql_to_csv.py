# Import required library
import sqlite3
import queries
from pandas import DataFrame

class SQLInterface:

    def __init__(self, database_name):
        self.conn = None
        self.cursor = None
        self.connect_to_db(database_name)

    # Print query result
    def execute_query(self, query):
        try:
            self.cursor.execute(query)

            if query.strip().lower().startswith("select"):
                rows = self.cursor.fetchall()
                for row in rows:
                    print(row)
            else:
                print("Query executed successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    # Establish database connection
    def connect_to_db(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    # Execute SQL queries from query list 
    def execute_from_query_list(self, queryList):

        for query in queryList:
            print(query)
            self.execute_query(query)
            self.conn.commit()

    # Run queries in terminal 
    def interactive_queries(self):
        while True:
            # Get SQL query from user
            user_query = input("Enter your SQL query (or type 'exit' to quit): ")
        
            if user_query.lower() == 'exit':
                break
        
            # Execute the query
            self.execute_query(user_query)
        
            # Commit changes
            self.conn.commit()

    # From SQL output to csv file
    def sql_to_pd_df(self, query, csv_name):
        self.cursor.execute(query)
        # fetch column names
        colums = []
        for column in self.cursor.description:
            colums.append(column[0])
        rows = self.cursor.fetchall()
        # make df
        df = DataFrame(rows)
        df.columns = colums
        print(df)
        df.to_csv(csv_name+".csv")

    def __del__(self):
        # Close connection
        self.conn.close()

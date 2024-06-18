import os
import psycopg2

# Database credentials from environment variables
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
sql_script_path = os.getenv('SQL_SCRIPT_PATH')

def run_sql_script():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # Read the SQL script
        with open(sql_script_path, 'r') as file:
            sql_script = file.read()
        
        # Execute the SQL script
        cursor.execute(sql_script)
        
        # Commit the transaction
        connection.commit()
        
        print("SQL script executed successfully.")
    
    except Exception as error:
        print(f"Error while executing the SQL script: {error}")
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    run_sql_script()

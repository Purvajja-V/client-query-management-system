import mysql.connector
import pandas as pd

#  Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@27",
    database="client_queries_db"
)

cursor = connection.cursor()

#  Read Excel file
df = pd.read_excel("cleaned_client_queries.xlsx")

#  Convert date columns safely
df['date_raised'] = pd.to_datetime(df['date_raised'], errors='coerce')
df['date_closed'] = pd.to_datetime(df['date_closed'], errors='coerce')

#  Insert rows if not already in MySQL (avoid duplicates)
for _, row in df.iterrows():
    # Check if same mail_id and query_heading already exist
    check_sql = """
        SELECT COUNT(*) FROM queries
        WHERE mail_id = %s AND query_heading = %s
    """
    cursor.execute(check_sql, (row['client_email'], row['query_heading']))
    exists = cursor.fetchone()[0]

    if exists == 0:  # only insert if not exists
        sql = """
            INSERT INTO queries
            (mail_id, mobile_number, query_heading, query_description,
             status, query_created_time, query_closed_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            row['client_email'],
            str(row['client_mobile']),
            row['query_heading'],
            row['query_description'],
            row['status'],
            row['date_raised'].to_pydatetime() if pd.notnull(row['date_raised']) else None,
            row['date_closed'].to_pydatetime() if pd.notnull(row['date_closed']) else None
        ))

#  Commit and close
connection.commit()
cursor.close()
connection.close()

print(" Excel data imported and synced successfully with MySQL!")

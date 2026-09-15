import psycopg2
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="ai_ecommerce",
    user="postgres",
    password="Varadraj"
)

print("PostgreSQL connection successful!")

# Load RFM data from PostgreSQL
query = """
SELECT *
FROM customer_rfm;
"""

rfm = pd.read_sql(query, conn)

# Save RFM data to CSV
rfm.to_csv("rfm_data.csv", index=False)

print("RFM data exported successfully!")
print("File: rfm_data.csv")
print("Rows:", len(rfm))

conn.close()

print("Connection closed.")
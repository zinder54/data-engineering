# Import libraries required for connecting to mysql

# Import libraries required for connecting to DB2 or PostgreSql
# python3 -m pip install ibm-db
#pip install --force-reinstall ibm_db==3.1.0 ibm_db_sa==0.3.3
# python3 -m pip install psycopg2
#python3.11 -m pip install mysql-connector-python;
"""db2 import"""
import ibm_db

"""PostgreSql import"""
import psycopg2

"""MySQL import"""
import mysql.connector

"""Connect to MySQL"""
connection = mysql.connector.connect(user='root', password='*',host='*',database='sales')

"""Connect to DB2"""
# connection details
dsn_hostname = "*"
dsn_uid = "*"        
dsn_pwd = "*"      
dsn_port = "*"                 
dsn_database = "bludb"            
dsn_driver = "{IBM DB2 ODBC DRIVER}"            
dsn_protocol = "TCPIP"            
dsn_security = "SSL"              

#Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)
# create connection
conn_db2 = ibm_db.connect(dsn, "", "")
print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

"""Connect to PostgreSql"""

dsn_hostname = "*"
dsn_user="*"        
dsn_pwd ="*"      
dsn_port ="*"                
dsn_database ="postgres"      
# create connection

conn = psycopg2.connect(
    database=dsn_database, 
    user=dsn_user,
    password=dsn_pwd,
    host=dsn_hostname, 
    port= dsn_port
)

# Find out the last rowid from DB2 data warehouse or PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database or PostgreSql.

"""this is the code i used to get the last row id from db2 table sales_data"""


def get_last_rowid_db2():
    last_row_id = None
    SQL="SELECT MAX(ROWID) FROM sales_data"
    stmt = ibm_db.exec_immediate(conn_db2, SQL)
    result = ibm_db.fetch_tuple(stmt)
    if result:
        last_row_id = result[0]
        

    return last_row_id

last_row_id = get_last_rowid_db2()
print("Last row id on production datawarehouse = ", last_row_id)

"""same thing below but for postgres"""


def get_last_rowid_pg():
     #Create a cursor onject using cursor() method
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(rowid) from public.sales_data;')
    rows = cursor.fetchone()

    last_row_id =rows[0]
    cursor.close()
    return last_row_id

last_row_id = get_last_rowid_pg()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    # create cursor
    cursor = connection.cursor()
    print("running query")
    cursor.execute(
        "SELECT * FROM sales_data WHERE rowid > %s ORDER BY rowid",
        (rowid,)
    )

    latest_records = cursor.fetchall()
    # Get new max rowid if records exist
    if latest_records:
        new_last_row_id = max(row[0] for row in latest_records)  # assumes rowid is first column
    else:
        new_last_row_id = rowid

    print("New rows:", len(latest_records))
    print(latest_records[:5])  # preview first few rows
    cursor.close()
    return latest_records, new_last_row_id

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))
print("Latest row_id now =", last_row_id)

def insert_records_pg(records):
    #Create a cursor onject using cursor() method
    cursor = conn.cursor()

    # records should be a list of tuples like:
    # [(rowid, product_id, customer_id, quantity), ...]
    SQL = """
    INSERT INTO public.sales_data (rowid, product_id, customer_id, quantity)
    VALUES (%s, %s, %s, %s)
    """

    cursor.executemany(SQL, records)
    conn.commit()
    cursor.close()
    
insert_records_pg(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

"""db2 insert rows"""
def insert_records_db2(records):
    # SQL with placeholders
    sql = "INSERT INTO SALES_DATA (ROWID, PRODUCT_ID, CUSTOMER_ID, QUANTITY) VALUES (?, ?, ?, ?)"

    # Insert each record
    for record in records:
        stmt = ibm_db.prepare(conn_db2, sql)
        ibm_db.execute(stmt, record)

    # Commit
    ibm_db.commit(conn_db2)

insert_records_db2(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
"""close MySQL connection"""
connection.close()
# disconnect from DB2 or PostgreSql data warehouse 
"""close DB2 connection"""
ibm_db.close(conn_db2)
"""close PostgreSql connection"""
conn.close()
# End of program

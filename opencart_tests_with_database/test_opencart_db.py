import MySQLdb
"""
Tests for connection, select, delete-insert in Opencart Database (MariaDB)  
"""


db = MySQLdb.connect(host="localhost", user="ocuser", passwd="PASSWORD", db="opencart")
cursor = db.cursor()
# Fetching all table names in database
cursor.execute("""select table_name from information_schema.tables
where table_type = 'BASE TABLE' and table_schema not in ('information_schema','mysql', 'performance_schema','sys')
order by table_schema, table_name;""")
tables = cursor.fetchall()
table_list = []
for i in tables:
    for j in i:
        table_list.append(j)
print("\nOpencart DB tables:", table_list)
# List all columns in currencies table
cursor.execute("""show columns from opencart.oc_currency""")
columns_list = []
for i in cursor.fetchall():
    columns_list.append(i[0])
print("\nColumns list in currencies table:", columns_list)
# List all currencies
cursor.execute("""select currency_id, title, code, symbol_right from opencart.oc_currency""")
print("\nCurrencies in Opencart DB:", cursor.fetchall())
# Inserting Russian Ruble line in currencies
if cursor.execute("""select * from opencart.oc_currency where title='Russian Ruble'"""):
    existing_line = cursor.fetchall()
    cursor.execute("""delete from opencart.oc_currency where title='Russian Ruble'""")
    print("\nDeleted existing line in oc_currency, existed values were:", existing_line)
cursor.execute("""insert into opencart.oc_currency (currency_id, title, code, symbol_right) values
               (4, 'Russian Ruble', 'RUB', 'R')""")
cursor.execute("""select * from opencart.oc_currency where title='Russian Ruble'""")
print("\nRussian Ruble current values:", cursor.fetchall())
db.close()
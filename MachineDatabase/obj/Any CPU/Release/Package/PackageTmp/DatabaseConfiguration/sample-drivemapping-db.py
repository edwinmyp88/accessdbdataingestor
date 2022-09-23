import pyodbc
import subprocess

# Disconnect anything on M
subprocess.call(r'net use m: /del', shell=True)

# Connect to shared drive, use drive letter M
subprocess.call(r'net use m: \\192.168.0.133\database /user:database database', shell=True)

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=M:\db1.mdb;')
cursor = conn.cursor()
cursor.execute('select * from machine')
   
for row in cursor.fetchall():
    print (row)

# Disconnect anything on M
subprocess.call(r'net use m: /del /Y', shell=True)
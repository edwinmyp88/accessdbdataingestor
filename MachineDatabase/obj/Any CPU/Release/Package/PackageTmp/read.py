import sqlite3
import threading
import pyodbc
import subprocess
import datetime
import collections
import json
import requests

def read():
    threading.Timer(10.0, read).start()
    t = datetime.date.today()
    today = t.strftime('%#d/%#m/%Y')
    #connection = sqlite3.connect("db.sqlite3")
    connection = sqlite3.connect("C:\sqlite3\mydb.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM config")
    for config in cursor.fetchall():
        frequency = config[1]
        endpoint = config[2]
        username = config[3]
        password = config[4]

    credential = username + ' ' + password

    cursor.execute("SELECT * FROM machine_db WHERE NOT db_status = 'Stopped' AND status = 'Active'")
    
    now = datetime.datetime.now()
    formatted_now = now.strftime('%Y-%m-%d %H:%M:00')

    for row in cursor.fetchall():
        id = row[0]
        ip_address = row[1]
        filename = row[2]
        selected_table = row[3]
        next_read = row[6]

        if next_read == formatted_now:

            print()
            print(formatted_now)
            print(ip_address + ': Next Read Datetime Match. Retrieve and Insert data.')
            print()

            try:
                # Disconnect anything on M
                subprocess.call(r'net use m: /del', shell=True)

                # Connect to shared drive, use drive letter M
                subprocess.call("net use m: " + ip_address + " /user:" + credential, shell=True)

                conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=M:\\" + filename + ";")
                cursor1 = conn.cursor()
                cursor1.execute("SELECT * FROM " + selected_table + " WHERE [START DATE] LIKE ? ORDER BY id", today + "%")

                objects_list = []

                for row in cursor1.fetchall():

                    obj = collections.OrderedDict()
                    obj['table'] = selected_table
                    obj['ip_address'] = ip_address
                    obj['old_id'] = row[0]
                    obj['start_date'] = datetime.datetime.strftime(row[1], '%Y-%m-%d %H:%M:%S')
                    obj['stop_date'] = datetime.datetime.strftime(row[2], '%Y-%m-%d %H:%M:%S')
                    obj['machine_name'] = row[3]
                    obj['package_name'] = row[4]
                    obj['lot_number'] = row[5]
                    obj['part_number'] = row[6]
                    obj['part_type'] = row[7]
                    obj['quantity_in'] = row[8]
                    obj['operator_id'] = row[9]
                    obj['total_good_qty'] = row[10]
                    obj['total_rej_qty'] = row[11]

                    try:
                        loading = time.strptime(row[12], '%H:%M:%S')
                        obj['loading_time'] = datetime.timedelta(hours=loading.tm_hour, minutes=loading.tm_min, seconds=loading.tm_sec).total_seconds()
                    except:
                        obj['loading_time'] = 0

                    try:
                        operation = time.strptime(row[13], '%H:%M:%S')
                        obj['operation_time'] = datetime.timedelta(hours=operation.tm_hour, minutes=operation.tm_min, seconds=operation.tm_sec).total_seconds()
                    except:
                        obj['operation_time'] = 0

                    try:
                        down = time.strptime(row[14], '%H:%M:%S')
                        obj['down_time'] = datetime.timedelta(hours=down.tm_hour, minutes=down.tm_min, seconds=down.tm_sec).total_seconds()
                    except:
                        obj['down_time'] = 0

                    try:
                        idling = time.strptime(row[15], '%H:%M:%S')
                        obj['idling_time'] = datetime.timedelta(hours=idling.tm_hour, minutes=idling.tm_min, seconds=idling.tm_sec).total_seconds()
                    except:
                        obj['idling_time'] = 0

                    obj['soft_jam'] = row[16]
                    obj['hard_jam'] = row[17]

                    try:
                        mtba = time.strptime(row[18], '%H:%M:%S')
                        obj['mtba'] = datetime.timedelta(hours=mtba.tm_hour, minutes=mtba.tm_min, seconds=mtba.tm_sec).total_seconds()
                    except:
                        obj['mtba'] = 0

                    try:
                        mtbf = time.strptime(row[19], '%H:%M:%S')
                        obj['mtbf'] = datetime.timedelta(hours=mtbf.tm_hour, minutes=mtbf.tm_min, seconds=mtbf.tm_sec).total_seconds()
                    except:
                        obj['mtbf'] = 0

                    obj['initial_v1_yield'] = row[20]
                    obj['v1_yield'] = row[21]
                    obj['initial_v2_yield'] = row[22]
                    obj['v2_yield'] = row[23]
                    obj['initial_v3_yield'] = row[24]
                    obj['v3_yield'] = row[25]
                    obj['initial_v4_yield'] = row[26]
                    obj['v4_yield'] = row[27]
                    obj['initial_v5_yield'] = row[28]
                    obj['v5_yield'] = row[29]
                    obj['initial_v6_yield'] = row[30]
                    obj['v6_yield'] = row[31]
                    obj['initial_v7_yield'] = row[32]
                    obj['v7_yield'] = row[33]
                    obj['bin_1_reject_crack'] = row[34]
                    obj['bin_2_reject_geometric'] = row[35]
                    obj['bin_3_rej'] = row[36]
                    obj['bin_4_rej'] = row[37]
                    obj['good_bin'] = row[38]
                    obj['total_output'] = row[39]
                    obj['initial_yield'] = row[40]
                    obj['overall_yield'] = row[41]
                    obj['initial_uph'] = row[42]
                    obj['lot_uph'] = row[43]
                    obj['rescan'] = row[44]

                    objects_list.append(obj)


                headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

                for object in objects_list:
                    print(json.dumps(object))
                    x = requests.post(endpoint, data=json.dumps(object), headers=headers, verify=False)


                # Disconnect anything on M
                subprocess.call(r'net use m: /del /Y', shell=True)

                cursor.execute("UPDATE machine_db SET db_status = 'Processed' WHERE id = " + str(id))
                connection.commit()

            except:
                print('The network path was not found.')
                cursor.execute("UPDATE machine_db SET db_status = 'Lost Connection' WHERE id = " + str(id))
                connection.commit()

            new_next_read = now + datetime.timedelta(minutes=frequency)
            formatted_new_next_read = datetime.datetime.strftime(new_next_read, '%Y-%m-%d %H:%M:00')
            #print(formatted_new_next_read)
            #cursor.execute("UPDATE machine_db SET next_read = " + "'" + formatted_new_next_read + "'" + " WHERE id = " + str(id))
            #connection.commit()

        else:
            print()
            print(formatted_now)
            print(ip_address + ': Next Read Not Match')
            print()

read()

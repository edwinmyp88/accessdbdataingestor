from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import pyodbc
import subprocess
import collections
import json
import datetime
import time
import requests
import threading

# Create your views here.

litmus_ip_address = 'https://192.168.0.188/'
lastRecordDatetime = litmus_ip_address + 'flows-1/api/lastRecordDatetime'

def printit():
    threading.Timer(10.0, printit).start()
    c = connection.cursor()
    c.execute('SELECT * FROM config')
    for row in c.fetchall():
        print(row)

#print('Program starting...')
#print('Resetting next read datetime...')
#printit()
#print('Resetting completed...')
#print('Program started...')

@csrf_exempt
def index(request):
    
    #conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=\\192.168.0.133\database\db1.mdb;')
    #cursor = conn.cursor()
    #cursor.execute('select * from machine')

    if request.method == 'GET':

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM config')
        config = cursor.fetchall()

        cursor.execute('SELECT * FROM machine_db WHERE status = "Active"')
        data = cursor.fetchall()
        formatted_data = []
    
        for row in data:
            #print (row)
            row_list = list(row)
            row_list[1] = row_list[1].replace('\\', '\\\\') # Replace file path \ with \\
            row_tuple = tuple(row_list)
            formatted_data.append(row_tuple)
        
        return render(request, 'DatabaseConfiguration/index.html', {'config': config, 'data':data})

    elif request.method == 'POST':

        filepath = request.POST.get('filepath')
        filename = request.POST.get('filename')
        selected_table = request.POST.get('selected_table')

        print(filepath)
        print(filename)
        print(selected_table)

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM config')
        config = cursor.fetchall()
        for conf in config:
            frequency = conf[1]
            endpoint = conf[2]
            username = conf[3]
            password = conf[4]

        credential = username + ' ' + password

        t = datetime.date.today()
        today = t.strftime('%#d/%#m/%Y')
        now = datetime.datetime.now()
        formatted_now = now.strftime('%Y-%m-%d %H:%M:00')
        next = now + datetime.timedelta(minutes=frequency)
        formatted_next = datetime.datetime.strftime(next, '%Y-%m-%d %H:%M:00')

        print(formatted_now)
        print(formatted_next)

        # Disconnect anything on K
        subprocess.call(r'net use k: /del', shell=True)

        try:
            # Connect to shared drive, use drive letter K
            subprocess.call("net use k: " + filepath + " /user:" + credential, shell=True)

            conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=K:\\" + filename + ";")
            cursor1 = conn.cursor()
            cursor1.execute("SELECT * FROM " + selected_table)

            objects_list = []

            for row in cursor1.fetchall():

                obj = collections.OrderedDict()
                obj['ip_address'] = filepath
                obj['tables'] = selected_table
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
                #print(json.dumps(object))
                x = requests.post(endpoint, data=json.dumps(object), headers=headers, verify=False)

            # Disconnect anything on K
            subprocess.call(r'net use k: /del /Y', shell=True)

            cursor.execute('INSERT INTO machine_db (path, name, tables, db_status, datetime_processed, next_read, status) VALUES (%s, %s, %s, "Processed", %s, %s, "Active")', [filepath, filename, selected_table, formatted_now, formatted_next])

            return HttpResponse('Complete')

        except Exception as e:
            # Disconnect anything on K
            subprocess.call(r'net use k: /del /Y', shell=True)

            print(e)
            error_code = e.args[0]
            error_msg = 'Something went wrong. Please check and try again.'

            if error_code == 'HY024':
                error_msg = 'The network path was not found.'
            elif error_code == 'HY000':
                error_msg = 'Could not find the file.'
            elif error_code == '42S02':
                error_msg = 'Table name is not exist.'
            elif error_code == 'IM002':
                error_msg = 'Data source name not found and no default driver specified.'

            return HttpResponse(error_msg)
            #return HttpResponse('Something went wrong. Please check again.')

    elif request.method == 'PUT':

        #print(json.loads(request.body))
        #frequency = json.loads(request.body.decode('utf-8'))['frequency']
        frequency = json.loads(request.body)['frequency']
        endpoint = json.loads(request.body)['endpoint']
        username = json.loads(request.body)['username']
        password = json.loads(request.body)['password']

        print(frequency)
        print(endpoint)
        print(username)
        print(password)

        cursor = connection.cursor()
        cursor.execute('UPDATE config SET frequency = %s, endpoint = %s, username = %s, password = %s WHERE id = 1', [frequency, endpoint, username, password])

        return HttpResponse('Configuration updated.')


@csrf_exempt
def refresh(request):

    if request.method == 'POST':

        refresh = request.POST.get('refresh')

        cursor = connection.cursor()
        cursor.execute('UPDATE config SET refresh = ' + str(refresh))

        return HttpResponse('Refresh time changed')

    else:
        return HttpResponse('Invalid URL Request.')

@csrf_exempt
def active(request, id):

    if request.method == 'POST':

        current_status = request.POST.get('current_status')
        cursor = connection.cursor()

        if current_status == 'Start':

            cursor.execute('UPDATE machine_db SET db_status = "Stopped" WHERE id = ' + str(id))

            return HttpResponse("Stopped Read from MS Access DB.")

        elif current_status == 'Stop':

            cursor.execute('SELECT * FROM config')
            for config in cursor.fetchall():
                frequency = config[1]
                endpoint = config[2]
                username = config[3]
                password = config[4]

            credential = username + ' ' + password

            cursor.execute('SELECT * FROM machine_db WHERE id = ' + str(id))
            for db in cursor.fetchall():
                ip_address = db[1]
                filename = db[2]
                selected_table = db[3]

            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            x = requests.get(lastRecordDatetime, params={'ip_address': ip_address, 'tables': selected_table}, headers=headers, verify=False)

            try:
                response = json.loads(x.content)[0]
                start_date = response['start_date'][0:10]
                last_processed = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

                t = datetime.datetime.now(datetime.timezone.utc).date()

                if last_processed <= t:
                
                    try:
                        # Disconnect anything on T
                        subprocess.call(r'net use t: /del', shell=True)

                        # Connect to shared drive, use drive letter T
                        subprocess.call("net use t: " + ip_address + " /user:" + credential, shell=True)

                        conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=T:\\" + filename + ";")
                        cursor1 = conn.cursor()

                        delta = t - last_processed

                        for i in range(delta.days + 1):
                            day = last_processed + datetime.timedelta(days=i)
                            day = day.strftime('%#m/%#d/%Y')
                            print(day)
                   
                            cursor1.execute("SELECT * FROM " + selected_table + " WHERE [START DATE] LIKE ? ORDER BY id", day + "%")

                            objects_list = []

                            for row in cursor1.fetchall():

                                obj = collections.OrderedDict()
                                obj['ip_address'] = ip_address
                                obj['tables'] = selected_table
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


                            for object in objects_list:
                                print(json.dumps(object))
                                try:
                                    x = requests.post(endpoint, data=json.dumps(object), headers=headers, verify=False)
                                except Exception as e:
                                    print(e)
                                    cursor.execute("UPDATE machine_db SET db_status = 'Failed Insert' WHERE id = " + str(id))
                                    connection.commit()


                        # Disconnect anything on T
                        subprocess.call(r'net use t: /del /Y', shell=True)

                        now = datetime.datetime.now()
                        formatted_now = now.strftime('%Y-%m-%d %H:%M:00')
                        new_next_read = now + datetime.timedelta(minutes=frequency)
                        formatted_new_next_read = datetime.datetime.strftime(new_next_read, '%Y-%m-%d %H:%M:00')

                        cursor.execute('UPDATE machine_db SET db_status = "Processed", datetime_processed = ' + '"' + formatted_now + '"' + ', next_read = ' + '"' + formatted_new_next_read + '"' + ' WHERE id = ' + str(id))

                        return HttpResponse("Started Read from MS Access DB.")

                    except:
                        print('The network path was not found.')
                        cursor.execute("UPDATE machine_db SET db_status = 'Lost Connection' WHERE id = " + str(id))
                        connection.commit()
                        return HttpResponse("Cannot start the machine. Please check and try again.")

            except IndexError:
                print("Cannot find previous data")

                try:
                    # Disconnect anything on T
                    subprocess.call(r'net use t: /del', shell=True)

                    # Connect to shared drive, use drive letter K
                    subprocess.call("net use t: " + ip_address + " /user:" + credential, shell=True)

                    conn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=T:\\" + filename + ";")
                    cursor1 = conn.cursor()
                    cursor1.execute("SELECT * FROM " + selected_table)

                    objects_list = []

                    for row in cursor1.fetchall():

                        obj = collections.OrderedDict()
                        obj['ip_address'] = ip_address
                        obj['tables'] = selected_table
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
                        try:
                            x = requests.post(endpoint, data=json.dumps(object), headers=headers, verify=False)
                        except Exception as e:
                            print(e)
                            cursor.execute("UPDATE machine_db SET db_status = 'Failed Insert' WHERE id = " + str(id))
                            connection.commit()

                    # Disconnect anything on T
                    subprocess.call(r'net use t: /del /Y', shell=True)

                    now = datetime.datetime.now()
                    formatted_now = now.strftime('%Y-%m-%d %H:%M:00')
                    new_next_read = now + datetime.timedelta(minutes=frequency)
                    formatted_new_next_read = datetime.datetime.strftime(new_next_read, '%Y-%m-%d %H:%M:00')

                    cursor.execute('UPDATE machine_db SET db_status = "Processed", datetime_processed = ' + '"' + formatted_now + '"' + ', next_read = ' + '"' + formatted_new_next_read + '"' + ' WHERE id = ' + str(id))

                    return HttpResponse("Started Read from MS Access DB.")

                except:
                    print('The network path was not found.')
                    cursor.execute("UPDATE machine_db SET db_status = 'Lost Connection' WHERE id = " + str(id))
                    connection.commit()
                    return HttpResponse("Cannot start the machine. Please check and try again.")


            #now = datetime.datetime.now()
            #new_next_read = now + datetime.timedelta(minutes=frequency)
            #formatted_new_next_read = datetime.datetime.strftime(new_next_read, '%Y-%m-%d %H:%M:00')

            #cursor.execute('UPDATE machine_db SET db_status = "Processed", next_read = ' + '"' + formatted_new_next_read + '"' + ' WHERE id = ' + str(id))

            #return HttpResponse("START for receiving data.")

    else:
        return HttpResponse('Invalid URL Request.')

@csrf_exempt
def edit(request, id):

    if request.method == 'GET':

        cursor = connection.cursor()

        cursor.execute('SELECT name FROM pragma_table_info("machine_db") ORDER BY cid')
        columns = cursor.fetchall()

        cursor.execute('SELECT * FROM machine_db WHERE status = "Active" AND id = ' + str(id))
        data = cursor.fetchall()

        for row in data:
            obj = collections.OrderedDict()
            index = 0
            for column in columns:
                obj[column[0]] = row[index]
                index += 1

        return HttpResponse(json.dumps(obj, default=str))

    elif request.method == 'POST':

        id = request.POST.get('id')
        filepath = request.POST.get('filepath')
        filename = request.POST.get('filename')
        selected_table = request.POST.get('selected_table')

        cursor = connection.cursor()
        cursor.execute('UPDATE machine_db SET path = ' + '"' + filepath + '"' + ', name = ' + '"' + filename + '"' + ', tables = ' + '"' + selected_table + '"' + ' WHERE id = ' + str(id))

        return HttpResponse('New information is updated.')

@csrf_exempt
def delete(request, id):

    if request.method == 'DELETE':

        cursor = connection.cursor()
        cursor.execute('UPDATE machine_db SET status = "Deleted" WHERE id = ' + str(id))

        return HttpResponse("Deleted")

    else:
        return HttpResponse('Invalid URL Request.')
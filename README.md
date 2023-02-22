# accessdbdataingestor

## Prerequisite

1. [Latest Python](https://www.python.org/downloads/)
2. [SQLiteStudio](https://sqlitestudio.pl/)
3. [Microsoft Access Database Engine 2016 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=54920)
4. [SQL Server Management Studio (SSMS)](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16)

## Setup

1. Download zip file from main branch, and extract the zip file.
2. Run `python --version` on Command Prompt to check is python installed.
3. If python is not installed, you can go to [Python Website](https://www.python.org/downloads/) to install the latest version.
4. After open the installer, select the 'Add to PATH' option before installing.
5. Run the following commands on Command Prompt to install necessary python packages.
   - `pip install django`
   - `pip install pyodbc`
   - `pip install requests`
6. Before start the program, run `cd` on Command Prompt to change the directory to where `manage.py` file located.
7. Run `py manage.py runserver 0.0.0.0:8000` on Command Prompt to start the program.
8. Now you can access the program on web browser with `<host ip address>:8000`.
9. If you do not know your ip address, you can run `ipconfig` on Command Prompt to check your device ip address.
10. Then open new Command Prompt, run `cd` to change the directory to where `read.py` file located.
11. Run `py read.py` on Command Prompt to start the program.
12. You can download [SQLiteStudio](https://sqlitestudio.pl/), and then browse `db.sqlite3` to view the database.


###### File Description

1. `manage.py` is the file to start the program that allow us to do the operations by using web browser.
2. `read.py` is the file to read from SQLite database to get Microsoft Access Database filepath, and then retrieve today data from Microsoft Access Database.

## Node-RED

1. Change the HTTP endpoint name if update the endpoint on the webpage.
2. Change the litmus_ip_address variable in views.py to current litmus's ip address.

## Potential Error

1. If the error message **Data source name not found and no default driver specified** is showed when adding new data source.
2. Open ODBC Data Sources and run as administrator, and add **Microsoft Access Driver (*.mdb, *.accdb)**.
3. If the driver is not found, you can download and install [Microsoft Access Database Engine 2016 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=54920).

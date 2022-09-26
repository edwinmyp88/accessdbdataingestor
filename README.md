# accessdbdataingestor

1. Download zip file from main branch.
2. Run `python --version` on Command Prompt to check is python installed.
3. If python is not installed, you can go to [Python Website](https://www.python.org/downloads/) to install the latest version.
4. Run the following commands on Command Prompt to install necessary python packages.
   - `pip install django`
   - `pip install pyodbc`
   - `pip install requests`
5. Before start the program, run `cd` on Command Prompt to change the directory to where `manage.py` file located.
6. Run `py manage.py runserver 0.0.0.0:8000` on Command Prompt to start the program.
7. Now you can access the program on web browser with `<your ip address>:8000`.
8. If you do not know your ip address, you can run `ipconfig` on Command Prompt to check your device ip address.
9. Then open new Command Prompt, run `cd` to change the directory to where `read.py` file located.
10. Run `py read.py` on Command Prompt to start the program.
11. You can download [SQLiteStudio](https://sqlitestudio.pl/), and then browse `db.sqlite3` to view the database.


###### File Description

1. `manage.py` is the file to start the program that allow us to do the operations by using web browser.
2. `read.py` is the file to read from SQLite database to get Microsoft Access Database filepath, and then retrieve today data from Microsoft Access Database.

## Potential Error

1. If the error message **Data source name not found and no default driver specified** is showed when adding new data source.
2. Open ODBC Data Sources and run as administrator, and add **Microsoft Access Driver (*.mdb, *.accdb)**.
3. If the driver is not found, you can download and install [Microsoft Access Database Engine 2016 Redistributable](https://www.microsoft.com/en-us/download/details.aspx?id=54920).

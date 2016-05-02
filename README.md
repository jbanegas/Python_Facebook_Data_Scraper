# -Script_Facebook_Data_Scraper
Script develop in Python 3.3.5 to scrape DATA from Facebook pages and store it in MSSQL tables.


'How to' basics steps:
1. Install Python 3.x.x (on Win10 64 bits)
2. Use the pip (Python package manager) to install the Pyodbc library used to access ODBC databases.
    - Start the command prompt and type: pip install pyodbc
3. The Script needs the facebook page_id and (for now) an access_token that are received as parameters in almost all functions. (the disadvantage of the acces_token is that is reset every hour, the best to do is used app_id + app_secret combination).
    - Get the access_token from https://developers.facebook.com/tools/explorer (be logged to facebook is necessary).

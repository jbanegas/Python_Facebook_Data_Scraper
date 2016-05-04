# Script_Facebook_Data_Scraper
Script develop in Python 3.3.5 to scrape DATA from Facebook pages and store it in MSSQL tables.

'How do' basics steps:
  Note: This script was develop on Win10 and MSSQL 2012 as database server
  1. Install Python 3.x.x 
  2. Use the pip (Python package manager) to install the Pyodbc library used to access ODBC databases.
    - Start the command prompt (CMD) and type: pip install pyodbc
  3. The Script needs the facebook page_id and (for now) an access_token that are received as parameters in almost all functions. (the disadvantage of the acces_token is that it is reseted hourly, the best to do is used app_id + app_secret combination).
    - Get the access_token from https://developers.facebook.com/tools/explorer (Facebook log in is necessary).

As an example of the data, you'll find the CSV file for crhoy.com in this repository.

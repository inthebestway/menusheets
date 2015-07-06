# This is just an excuse to play with

 * [gspread](https://github.com/burnash/gspread) ( with oauth2 ) / maybe this is overkill ? 
 * flask
 * Jinja2
 * foundation

 * using google spreadsheets as a mini-cms ( inspired by NPR's copytext + app rig )
 * creating a responsive / easily edited menu for a local restaurant that I like.. 

# Setup 
install from requirements.txt

to run: 

```
> python flask_gsheet.py 
```

opens to localhost:5000/menu ..

some other testing urls: 
 * localhost:5000/testFoundation
 * localhost:5000/testData


# stuff in here : 

 * gsheets_wrap.py - wraps the oauth2 for accessing the google spreadsheet & pulls the sheet data into a dictionary. Stores the data in a json file & optionally can reload the spreadsheet
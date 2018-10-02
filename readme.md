# World History Timeline
Even though it says world history timeline, it is quite dumb so not all data will make sense. 
The data has been extracted from wikipedia using regular expressions. 

You can grab the database [here](https://mega.nz/#!GVtWQIJB!csOiwXuJP61NjKJLZCbLNprJxHcMyYuu24nteqj8wFU)

To run the crawler, run
```python
from crawler import crawl
crawl(3000) # number of pages to crawl
```
You can quit the program anytime using `Ctrl + C` and resume the next time you crawl again.

## Running it
To run it on powershell:
```
$env:FLASK_APP='index.py'
flask run
```
On Bash:
```
export FALSK_APP=index.py
flask run
```
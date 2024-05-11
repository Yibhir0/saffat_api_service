# saffat_api_service
This repositories contains that scrape the prayer's time , stores it in sqlite database, and exposes that data as an api endpoint.
- Steps to run the project:
- clone the project: git clone git@github.com:Yibhir0/saffat_api_service.git
- install pyhton  : https://www.python.org/downloads/
- instal pip : https://pip.pypa.io/en/stable/installation/
- pip install -r requirements.txt (This command will install all dependencies inside requirements.txt)
- run the file main.py inside scrape folder (This will scrape data and stores it sqlite file)
- run saffat.py inside api folder
- access http://localhost:5001/data/all

# saffat_api_service
# Set up cloud environment
  - Create EC2 instance in aws ubuntu t2.micro
  - ssh to ec2 intance
# Set up python environment
  - adduser saffat
  - usermod -aG sudo saffat
  - su -l saffat
  - ssh-keygen -t rsa -----> add key to github ssh key
  - git clone git@github.com:Yibhir0/saffat_api_service.git
  - sudo apt-get update
  - sudo apt-get install -y python3
  - sudo apt-get install -y python3-venv
  - python3 -m venv ~/env/saffat
  - source ~/env/yass/bin/activate
# set up and run the scrape function in the environment
  - sudo apt-get update
  - sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4
  - sudo apt-get install default-jdk
  - sudo apt-get install -y google-chrome-stable
  - wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
  - unzip chromedriver_linux64.zip
  - sudo mv chromedriver /usr/bin/chromedriver
  - sudo chown root:root /usr/bin/chromedriver
  - sudo chmod +x /usr/bin/chromedriver
  - pip install -r requirements.txt
  - sudo ufw allow ssh
	- sudo ufw allow 5000
  - run flask app
  - http://ip
# set up gunicorn:
	- pip install gunicorn
  - gunicorn --bind 0.0.0.0:5000 wsgi:app
  - sudo fuser -k 5000/tcp ----> to kill all processes associated with 5000
  - http://ip
# Set up the infrastracture:
  - deactivate  ----> deactivate python environment
  - sudo vim /etc/systemd/system/saffat.service
  - paste: <br>
    [Unit]<br>
	  Description=Gunicorn instance to serve saffat Flask app<br>
	  After=network.target<br>
	  [Service]<br>

	User=saffat<br>
	Group=www-data<br>
	WorkingDirectory=/home/saffat/saffat_api_service/api<br>
	Environment="PATH=/home/saffat/env/saffat/bin"<br>
	ExecStart=/home/saffat/env/saffat/bin/gunicorn --workers 3 --bind 	unix:saffat.sock -m 007 wsgi:app<br>
	[Install]<br>
	WantedBy=multi-user.target<br>
 - sudo systemctl daemon-reload
 - sudo systemctl start saffat
 - sudo systemctl enable saffat
 - sudo systemctl status saffat
# Set up Nginx:
 -  sudo apt install nginx
 -   sudo vim /etc/nginx/sites-available/saffat.conf
 -   paste:
   server { <br>
    listen 80;<br>
    server_name <ip/host>;<br>

    location / {<br>
        include proxy_params;<br>
        proxy_pass http://unix:/home/saffat/saffat_api_service/api/saffat.sock;<br>
    }<br>
   }<br>

   - sudo ln -s /etc/nginx/sites-available/saffat.conf /etc/nginx/sites-enabled/
   - sudo nginx -t
   - sudo systemctl restart nginx
   - sudo systemctl status nginx
   - sudo ufw enable
   - sudo ufw status
   - udo ufw delete allow 5000
   - sudo ufw status
   - http://ip
   - //  sudo tail /var/log/nginx/error.log --- > logs
   - update the code:<br>
     sudo systemctl restart saffat <br>
     sudo systemctl enable saffat<br>
   - set time:<br>
     sudo ln -sf /usr/share/zoneinfo/America/Montreal /etc/localtime  <br>
# Schedule with cron:
 - crontab -e
 - 0 0 * * * /home/saffat_api_service/scrape/daily.sh
     
# Run locally:
This repositories contains that scrape the prayer's time , stores it in sqlite database, and exposes that data as an api endpoint.
- Steps to run the project:
- clone the project: git clone git@github.com:Yibhir0/saffat_api_service.git
- install pyhton  : https://www.python.org/downloads/
- instal pip : https://pip.pypa.io/en/stable/installation/
- pip install -r requirements.txt (This command will install all dependencies inside requirements.txt)
- run the file main.py inside scrape folder (This will scrape data and stores it sqlite file)
- run saffat.py inside api folder
- access http://localhost:5001/data/all

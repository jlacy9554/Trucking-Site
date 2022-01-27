# Amazon Linux

initial setup commands: 

	sudo yum update
	sudo yum install python3 python3-devel mysql-devel gcc tree git
	curl -O https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py --user
	rm get-pip.py
	python3 -m pip install --user virtualenv

	python3 -m venv django-env && source django-env/bin/activate

	python3 -m pip install Django && python3 -m pip install mysqlclient

	django-admin startproject testsite

/home/ec2-user/truckingsite/truckingsite/settings.py

	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'DRIVER_DB',
			'USER': 'admin',
			'PASSWORD': 'accesstodb',
			'HOST': 'truckingdb.c9tkxb1tjvpp.us-east-1.rds.amazonaws.com',
			'PORT': '3306',
		}
	}

add public ec2 address to allowed hosts in settings.py

run server:

	python manage.py runserver 0:8000

edit rds inbound rule to include port 3306 and ec2 ipaddress

### APACHE and MOD_WSGI
	sudo yum install httpd mod_wsgi
	sudo systemctl enable httpd && sudo systemctl start httpd

**ran into problems so switched to using Ubuntu**

# Ubuntu 

https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04

initial setup:

	sudo apt-get update && sudo apt-get upgrade
	sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
	sudo pip3 install virtualenv

	git clone https://S21-Team04-Lacy-Patell-Blankenship-Racel-Clemons@dev.azure.com/S21-Team04-Lacy-Patell-Blankenship-Racel-Clemons/S21-Team04-Lacy.Patel.Blankenship.Clemons.Racel/_git/S21-4910-Project

	virtualenv django-env && source django-env/bin/activate
	pip install django mysql-connector-python ebaysdk bs4 reportlab

add public ec2 elastic ip address to allowed hosts in settings.py

run server and deactivate:

	python manage.py runserver 0:8000

	deactivate

/etc/apache2/sites-available/000-default.conf

	Alias /static /home/ubuntu/S21-4910-Project/truckersite/static
	<Directory /home/ubuntu/S21-4910-Project/truckersite/static>
		Require all granted
	</Directory>

	<Directory /home/ubuntu/S21-4910-Project/truckersite/truckersite>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>

	WSGIDaemonProcess truckersite python-home=/home/ubuntu/S21-4910-Project/truckersite/django-env python-path=/home/ubuntu/S21-4910-Project/truckersite
	WSGIProcessGroup truckersite
	WSGIScriptAlias / /home/ubuntu/S21-4910-Project/truckersite/truckersite/wsgi.py

run commands:

	sudo apache2ctl configtest
	sudo systemctl restart apache2

	chmod 664 S21-4910-Project/truckersite/db.sqlite3
	sudo chown :www-data S21-4910-Project/truckersite/db.sqlite3
	sudo chown :www-data S21-4910-Project/truckersite

**Sucessful setup of Django!**
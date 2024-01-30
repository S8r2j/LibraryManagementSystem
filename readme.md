## Steps to run the backend
> I have used MySQL database. So, let's set up the database first.
>- Download and install [Xampp](https://www.apachefriends.org/download.html). Just leave the default settings and at last tick on "Add to bin"
>- Open the xampp control panel and start apache and mysql server
>- Go to [admin](http://localhost/phpmyadmin/index.php) page of MySQL through xampp contol panel.
>- Create a database leaving everything to default

> Your database is all set. Now we need to connect the database with the flask application. Below are the steps:
> - Clone and open the repository in IDE
> - Dowload and install [python](https://www.python.org/downloads/), if you don't have installed
> - Setup the virtual environment
> - Install the requirements.txt using command:<br><b>pip install -r requirements.txt</b>
> - Create ".env" file, in directory where main.py file is located, with the following parameters:<br>host = localhost<br>
user = root<br>
password = ""<br>
database = your_database_name<br>
secret_key = create_secret_key as said below:<br>Open the command prompt and type the command<br> <i>python -c "import secrets; print(secrets.token_hex(16))"</i>
> - Run the backend using the command:<br><b>python main.py</b>
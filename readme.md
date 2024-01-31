## Steps to run the backend
Some basic things you need to know about this backend is my way of thinking and implementing the backend. I came up with the idea that only the admins are  allowed to make changes in the library system. So, I defined the login features for the admins.
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

You can check the APIs [here](https://www.postman.com/red-space-314271/workspace/library-management-system/collection/23667429-92e10b90-2d3a-4179-8f2b-f64f15e41c6b?action=share&creator=23667429) for each of their purposes. If you want to run these APIs you have to do it locally. Before running these APIs here are few things that you need to take care of:
- First of all, one admin account is already created in the backend with which you can create the multiple admins. Login credentials are as:<br><b>Email:</b><i> admin@gmail.com</i><br><b>Password:</b><i> admin@123</i>
- Before using these APIs you need to login with the above credentials which will in return provide you token
- The validation time of token is 4 hours. After 4 hours, you need to regenerate the token.
- And for each of the APIs you need to send token while calling.
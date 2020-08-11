# Require

1.install virtual env.

```bash
sudo pip3 install virtualenv
```

High recommand for python3(pip3), some packet cannot run on python2(pip)!

2.create a virtual envirment for your project.

```bash
cd your_project_bame
python3 -m venv venvname (virtua envir name)
```

3. and you can find a dic named venv.
4. start virtualenv.

```
source venvname/bin/activate
```

5.install all requirments.

```
pip install -r requirements.txt
```

# Reids

<https://redis.io/download>
please download redis server

# Install Redis

```bash

cd project
ls #check redis zip exist ot not
tar xzf redis-6.0.6.tar.gz # or you can double click
ls # there is file named redis-6.0.6
cd redis-6.0.6
make
```

# How to run redis

before you run web server, you need to start redis server first

```bash
cd ....project/redis-6.0.6/src
./redis-server

```

keep redis run!

cd to the root dir which contains manage.py file.<br>
you can run it on django default debugging server:

```
python manage.py runserver
```

and you can run it on uwsgi server:

```
uwsgi --http :8000 --module readbook.wsgi
```

if your default python command is python2, you need use python3 to replace python!<br>
you can use this to know python version:

```
python --version
```

if your terminal show this: Congratulations！your server is running!
![image](https://github.com/unsw-cse-capstone-project/capstone-project-orchid-malevolence/blob/master/Django_and_vue/img.png)

And now, you can check all data with admin account, or get data with your vue with api.

# Account(username and password)

please use normal account priority:
Black,123456<br>
Pink,123456<br>

Superuser account: username: admin, password: 123456<br>
localhost:8000/admin<br>
you can create an new account, do not use complex password, if account be created, password will be Encrypted! you can not check it by /admin!

# Book Database

database have 550+ books information.

these book related to

```python
    # ['python','java','linux','harryporter','Holmes','Django','Twilight','cook',
    # 'Shakespeare','hugo','Algorithm','Vampire','Verne','Ocean','Food','Fruit','Maya','Egypt','Roma',
    # 'Carthage','United Kingdom','Blues','Rock','sex','education','love','friend','countryside','airplane','magic','speaking',
    # 'alcohol','Alexandre Dumas','Goethe','Dante','Tagore','Leo Tolstoy','Maxim Gorky','Hemingway','Balzac','Pushkin',
    #'cat','dog','chocolate','pie','database','IBM','piano','violin','elves','tank','cake','tea',
    #'coffee','pizza','milk','rose','spring','shark','lion','cache','cpu','gpu','intel','newspaper','law','sun','moon','basketball','football']
```

# Api info

Please check Api.md!

# File structure

```
.
├── account
├── backed
├── data
├── readbook
├── uwsgi_conf
├── db.sqlite3
├── edit.py
├── manage.py
├── readme.md
├── requirements.txt
└── test.py
```

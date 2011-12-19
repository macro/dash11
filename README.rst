Bootstrap
=========
::

$ git clone https://github.com/macro/dash11.git
$ easy_install -U virtualenv
$ virtualenv virtualenv
$ source virtualenv/bin/activate
$ easy_install -U pip
$ cd dash_proj
$ pip install -U -r requirements.txt
$ python manage.py syncdb --migrate

Running
=======
::

$ ./bin/run

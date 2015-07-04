===============================
airconapp
===============================

Setting up for development
--------------------------

Get the code, and then ``vagrant do runserver``::

    $ git clone git@bitbucket.org:takeflight/airconapp.git
    $ cd airconapp
    $ vagrant do runserver

This will get the environment up and running.

An administrator account will be created as part of setting up,
username ``admin`` and password ``p``.

Every time you want to work on this project,
you can simply type ``vagrant do runserver`` again to start the development environment.

Compiling assets
~~~~~~~~~~~~~~~~

Frontend assets can be compiled by running::

    $ vagrant do assets

Testing
~~~~~~~

Run the following to reset your database to a know state with test data::

    $ vagrant ssh
    $ reset-db

Deploying
---------

* Get the code and set up the environment::

        $ git clone git@bitbucket.org:takeflight/airconapp.git
        $ cd airconapp
        $ virtualenv venv
        $ source venv/bin/activate
        $ pip install -r setup/pip-requirements/live.txt

* Make a local config::

        $ cp ./settings.py.example ./settings.py
        $ $EDITOR settings.py

* Either:
  * Import an existing database dump, or
  * Create a new DB with the basic site structure::

        $ python manage.py migrate
        $ python manage.py siteskeleton

* Compile and collect the static assets
  * Install node and the dependencies::

        # apt-get install nodejs
        $ npm install

  * Compile the assets and move them in to place::

        $ npm run build
        $ python manage.py collectstatic

* Use your choice of production daemon running/WSGI handler/voodoo incantations to
  connect the app with Nginx/Apache

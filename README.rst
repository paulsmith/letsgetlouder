Let’s Get Louder
================

Source code for letsgetlouder.com, a site where members of the Django
community can pledge that they will only attend conferences with a
clearly stated code of conduct policy which addresses harassment.

Installation
------------

::

    $ git clone https://github.com/paulsmith/letsgetlouder
    $ cd letsgetlouder
    $ virtualenv .
    $ . bin/activate
    $ cp local_settings.example.py local_settings.py
    $ python setup.py develop
    $ python manage.py syncdb
    $ python manage.py runserver

To test the social network integration, add the following line to your
/etc/hosts::

    127.0.0.1 letsgetlouder.com

Obtain the client IDs and consumer keys from Paul or Julia and add them
to your local_settings.py

Deployment
----------

To deploy, run::

    $ pip install -r dev.txt
    $ fab production deploy

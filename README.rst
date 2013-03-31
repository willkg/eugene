==============
 About eugene
==============

eugene is a *really* basic chat system I built to use with `Artemis
<http://www.artemis.eochu.com/>`_ to act as a text-based comms system.

It's got two parts:

1. backend is a really stripped down Flask-based web application that
   has a REST API that does some basic message and participant
   handling

2. HTML5 frontend for "signing in", sending, receiving and handling
   messages


Setting it up
=============

Quick start::

    $ git clone https://github.com/willkg/eugene
    $ cd eugene
    $ mkvritualenv eugene
    $ pip install -r requirements.txt
    $ cp eugene/settings_local.py-dist eugene/settings_local.py
    
    edit eugene/settings_local.py with your favorite editor

    $ python manage.py db_create


To run the server::

    $ python manage.py runserver


To run on a specific host and port::

    $ python manage.py runserver --host <HOST> --port <PORT>


Testing
=======

Tests use nose.

To run tests::

    $ nosetests


License
=======

eugene is distributed under the MIT license. See LICENSE for details.

bootstrap is distributed under the Apache v2 license.

jquery is distributed under the MIT license.

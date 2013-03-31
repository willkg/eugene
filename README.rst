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

Pre-requirements:

* Python 2.7: http://python.org/
* virtualenv with pip: https://pypi.python.org/pypi/virtualenv

  Use the "from source" instructions that don't require pip to install
  it.

* virtualenv-wrapper: http://virtualenvwrapper.readthedocs.org/en/latest/

It doesn't work with prior versions of Python. It also doesn't work with
Python 3.

It requires a recent version of virtualenv, pip and virtualenv-wrapper.
Those are all "standard" things in Python world now. So if you don't
have them, now's the time to install them.


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


That'll tell you the url for your browser. Open one browser tab for each
ship.


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

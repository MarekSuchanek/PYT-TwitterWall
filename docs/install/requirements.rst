Requirements
============

You need **Python 3.4+** to run this app and then there are two options
(examples are for Linux systems, for Windows or OSX find appropriate
equivalents):

Python environment
------------------

Check your ``python3 --version`` first, maybe you will need to use
``python3`` or ``python3.5`` instead or update finally!

You can use system-wide as well as virtual Python environments to
work with **PYT TwitterWall**. See this two options below, all other
commands in this documentation are not dependent on your choice (we
do not remark used environment).

System-wide environment
~~~~~~~~~~~~~~~~~~~~~~~

::

   $ python3 setup.py install
   $ twitterwall ...


Virtual environment
~~~~~~~~~~~~~~~~~~~

::

   $ python3 -m venv env
   $ . env/bin/activate
   (env) $ python3 setup.py install
   (env) $ twitterwall ...

   (env) $ deactivate
   $ rm -r env

Packages
--------

You can see what packages are required for install, testing and docs in files:

- setup.py (``install_requires``, ``setup_requires``, ``tests_require``)
- requirements.txt (read next section)
- docs/requirements.txt


Install tested environment
--------------------------

Thi project is tested in environment with packages & versions noted in
the ``requirements.txt`` file (made by ``pip freeze``). So you can install
identical environment by:

::

    python -m pip -r requirements.txt

Be sure to use correct version of Python (tested with 3.5).

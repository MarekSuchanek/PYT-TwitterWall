Testing
=======

This project uses the most fabulous testing tools for Python:

-  `pytest`_
-  `pytest-cov`_
-  `pytest-pep8`_
-  `pytest-sugar`_
-  `flexmock`_
-  `betamax`_

Run tests
---------

Run tests simply by:

::

    python setup.py test

or (if you have installed dependencies):

::

    python -m pytest [options]
    pytest [options]

Betamax cassettes
-----------------

Betamax cassettes are stored in ``tests/fixtures/cassettes`` directory. If
you are not connected to the internet, Twitter API is not working and/or
you don’t have own API credentials you will use (replay) them in order to
test API client.

If you want to run your own cassettes, you need to setup system
variables

-  ``API_KEY``
-  ``API_SECRET``

Your test command then might look like:

::

    API_KEY=<YOUR_API_KEY> API_SECRET=<YOUR_API_SECRET> \
    python setup.py test

For more information, enjoy reading `Betamax documentation`_.

.. _pytest: http://doc.pytest.org/
.. _pytest-cov: https://pypi.python.org/pypi/pytest-cov
.. _pytest-pep8: https://pypi.python.org/pypi/pytest-pep8
.. _pytest-sugar: https://pypi.python.org/pypi/pytest-sugar
.. _flexmock: http://flexmock.readthedocs.io/en/latest/
.. _betamax: http://betamax.readthedocs.io
.. _Betamax documentation: http://betamax.readthedocs.io/en/latest/introduction.html


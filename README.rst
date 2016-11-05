PYT TwitterWall
===============

|License| |Version| |Build Status|

PYT TwitterWall is simple `Python`_ powered app for displaying `Twitter`_
tweets in CLI. It has the ability to show number of queried tweets (i.e.
selected by search string) at start and then check if new tweets are publish
and display them as well. This project is created as task for subject MI-PYT,
CTU in Prague (`subject repository`_).

Documentation
-------------

Project now use `Sphinx`_ documentation:

* Read documentation online and don't bother with anything:
  - Will be provided soon, stay tuned!
* Build HTML documentation locally:
   - Install all dependencies for ``twitterwall``
   - Run this commands:
    ::

       cd docs/
       pip install -r requirements.txt
       make html
   - Open ``docs/_build/html/index.html`` in your browser
* Run documentation tests:
   - Install all dependencies for ``twitterwall``
   - Run this commands:
    ::

       cd docs/
       pip install -r requirements.txt
       make doctest

Authors
-------

-  Marek Suchánek [`suchama4@fit.cvut.cz`_]

License
-------

This project is licensed under the MIT License - see the `LICENSE`_
file for more details.

.. _Python: https://www.python.org
.. _Twitter: https://twitter.com
.. _subject repository: https://github.com/cvut/MI-PYT
.. _Sphinx: http://www.sphinx-doc.org
.. _suchama4@fit.cvut.cz: mailto:suchama4@fit.cvut.cz
.. _LICENSE: LICENSE

.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: LICENSE
.. |Version| image:: https://img.shields.io/badge/release-v0.5-orange.svg
.. |Build Status| image:: https://travis-ci.com/MarekSuchanek/PYT-TwitterWall.svg?token=XD73y3snHDycemSiHx3H&branch=task04
   :target: https://travis-ci.com/MarekSuchanek/PYT-TwitterWall

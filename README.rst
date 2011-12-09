Ella Category Subdomain
=======================

Ella Category Subdomain is an application for the `Ella`_, a `Django`_ based CMS system.

You can use selected Ella categories as subdomains without the need to create many sites
and for easier administration.

It is usable for SEO, microsites, landing pages and similar things.

.. _Ella: http://www.ellaproject.cz/
.. _Django: http://www.djangoproject.com/


Installation
============

Install via PyPi::

    pip install ella-category-subdomain

Or you can get latest version from GitHub and install it::

    python setup.py install


Tests
=====

You can run tests for this application, here is example::

    # create and acivate virtualenv, then
    pip install -r requirements/base.txt -r requirements/test.txt
    ./tests/unit/run_tests.py


TODO
====

  * caching
  * tests with client (middleware)


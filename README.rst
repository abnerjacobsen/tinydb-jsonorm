========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls| |codecov|
        | |landscape| |codacy| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/tinydb-jsonorm/badge/?style=flat
    :target: https://readthedocs.org/projects/tinydb-jsonorm
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/abnerjacobsen/tinydb-jsonorm.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/abnerjacobsen/tinydb-jsonorm

.. |requires| image:: https://requires.io/github/abnerjacobsen/tinydb-jsonorm/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/abnerjacobsen/tinydb-jsonorm/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/abnerjacobsen/tinydb-jsonorm/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/abnerjacobsen/tinydb-jsonorm

.. |codecov| image:: https://codecov.io/github/abnerjacobsen/tinydb-jsonorm/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/abnerjacobsen/tinydb-jsonorm

.. |landscape| image:: https://landscape.io/github/abnerjacobsen/tinydb-jsonorm/master/landscape.svg?style=flat
    :target: https://landscape.io/github/abnerjacobsen/tinydb-jsonorm/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/82865c7a11ab4336815de7915178c486.svg?style=flat
    :target: https://www.codacy.com/app/abnerjacobsen/tinydb-jsonorm
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/abnerjacobsen/tinydb-jsonorm/badges/gpa.svg
   :target: https://codeclimate.com/github/abnerjacobsen/tinydb-jsonorm
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/tinydb-jsonorm.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/tinydb-jsonorm

.. |downloads| image:: https://img.shields.io/pypi/dm/tinydb-jsonorm.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/tinydb-jsonorm

.. |wheel| image:: https://img.shields.io/pypi/wheel/tinydb-jsonorm.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/tinydb-jsonorm

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tinydb-jsonorm.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/tinydb-jsonorm

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/tinydb-jsonorm.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/tinydb-jsonorm


.. end-badges

A library based on jsonmodels that adds some ORM features and another few conveniences to TinyDB with Json storage and
tinydb-smartcache enabled.

* Free software: BSD license

Installation
============

::

    pip install tinydb-jsonorm

Documentation
=============

https://tinydb-jsonorm.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

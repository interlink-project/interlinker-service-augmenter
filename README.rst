Interlinker Service Augmenter
=============================


The functionality can roughly be separated in the follow parts:

1. A Flask blueprint for a web server that exposes an HTTP API to the annotation
   storage. 

2. An web application which enables the logged user to insert, delete and reply annotations of descriptions.

Getting going
-------------

You'll need a recent version of `Python <http://python.org>`__ (Python 2 >=2.6
or Python 3 >=3.9) and `ElasticSearch <http://elasticsearch.org>`__ (=1.7.6)
installed.

To create and run a image of Elasticsearch: 

.. code-block:: Python

   docker-compose up

The quickest way to get going requires the pipenv
tools and (``pipenv install`` will get all). Run the
following in the repository root:

.. code-block:: Python

    pipenv shell
    pipenv install
    python run.py

You should see something like:

.. code-block:: Python

    * Running on http://localhost:5000/
    * Restarting with reloader...


Additionally, the ``HOST`` and ``PORT`` environment variables override
the default socket binding of address ``127.0.0.1`` and port ``5000``.

Store API
---------

The Store API is designed to be compatible with the
`Annotator <http://okfnlabs.org/annotator>`__. The annotation store, a
JSON-speaking REST API, will be mounted at ``/api`` by default. See the
`Annotator
documentation <http://docs.annotatorjs.org/en/v1.2.x/storage.html>`__ for
details.

The API access point can be found in:
<http://localhost:5000/docs>

Website APP
-----------

The website app allow to annotate website descriptions.

Running tests
-------------

We use ``nosetests`` to run tests. You can just
``pip install -e .[testing]``, ensure ElasticSearch is running, and
then:

.. code-block:: 

    $ nosetests


    Ran 86 tests in 19.171s

    OK

Alternatively (and preferably), you should install
`Tox <http://tox.testrun.org/>`__, and then run ``tox``. This will run
the tests against multiple versions of Python (if you have them
installed).

Please `open an issue <http://github.com/openannotation/annotator-store/issues>`__
if you find that the tests don't all pass on your machine, making sure to include
the output of ``pip freeze``.

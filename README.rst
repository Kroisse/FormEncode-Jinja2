FormEncode-Jinja2
=================

.. image:: https://travis-ci.org/Kroisse/FormEncode-Jinja2.png?branch=master
  :alt: Build Status
  :target: https://travis-ci.org/Kroisse/FormEncode-Jinja2

FormEncode-Jinja2 is a `Jinja2`_ extension for filling HTML forms via `FormEncode`_.

You can install it from `PyPI`_::

   $ pip install FormEncode-Jinja2  # or
   $ easy_install FormEncode-Jinja2

.. _Jinja2: http://jinja.pocoo.org/
.. _FormEncode: http://www.formencode.org/
.. _PyPI: https://pypi.python.org/pypi/FormEncode-Jinja2


Usage
-----

Simple example in the interactive mode:

.. sourcecode:: pycon

   >>> import jinja2
   >>> import formencode_jinja2
   >>> env = jinja2.Environment(extensions=[formencode_jinja2.formfill])
   >>> # or if there is already the Jinja environment:
   >>> env.add_extension(formencode_jinja2.formfill)
   >>> template = '''
   ... {%- formfill {'username': 'robert', 'email': 'robert153@usrobots.com'}
   ...        with {'username': 'This name is invalid'} -%}
   ...     <input type="text" name="username" />
   ...     <form:error name="username">
   ...     <input type="password" name="password" />
   ...     <input type="email" name="email" />
   ... </form>
   ... {%- endformfill -%}
   ... '''
   >>> print env.from_string(template).render()
   <input type="text" name="username" class="error" value="robert" />
       <span class="error-message">This name is invalid</span>
       <input type="password" name="password" value="" />
       <input type="email" name="email" value="robert153@usrobots.com" />
   </form>


on `Flask`_

.. sourcecode:: python

   from flask import Flask
   import formencode_jinja2

   app = Flask(__name__)
   app.jinja_env.add_extension(formencode_jinja2.formfill)


.. _Flask: http://flask.pocoo.org/


License
-------

Distributed under `MIT license <http://kroisse.mit-license.org/>`_.
See also ``LICENSE`` file.

Written by `Eunchong Yu <http://krois.se/>`_.

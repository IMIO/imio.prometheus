.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

===============
imio.prometheus
===============

This package add a view "/@@metrics" used to prometheus.

Features
--------

- Add metrics view.

Installation
------------

Install imio.prometheus by adding it to your buildout::

    [buildout]

    ...

    eggs =
        imio.prometheus


and then running ``bin/buildout``

License
-------

The project is licensed under the GPLv2.

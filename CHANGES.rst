Changelog
=========

.. towncrier release notes start

2.0.1 (unreleased)
------------------

- Nothing changed yet.


2.0.0 (2026-11-20)
------------------

- Breaking: replace the ``pkg_resources`` namespace of ``imio`` with a PEP 420
  native namespace. Support Plone 6.2 only, on Python 3.10 to 3.14.
  Python 2 and Plone 4.3 to 6.1 sites stay on 1.0.x.
  [remdub]

- Breaking: drop the dependencies the code never imported (``z3c.jbot``,
  ``plone.app.dexterity``, ``plone.restapi``) and the unused robot
  ``IMIO_PROMETHEUS_ACCEPTANCE_TESTING`` layer.
  [remdub]

- Import ``INonInstallable`` from ``plone.base`` instead of the alias Plone 6.2
  deprecates, and make ``update_locale`` work without ``pkg_resources``.
  [remdub]

- Configure the package with plone.meta 2.12.0 (test matrix on Plone 6.2.3,
  Python 3.10 to 3.14), move its metadata to ``pyproject.toml`` and run the
  development environment on Plone 6.2.3 with uv instead of buildout.
  [remdub]

- Fix list and `im_self` for Python 3
  [laulaz]


1.0.1 (2022-02-01)
------------------

- Update classifiers to accept python 2.7.
  [bsuttor & odelaere]

- Add object_counts gauge.
  [bsuttor]


1.0.0 (2020-11-10)
------------------

- Update package to pypi.
  [bsuttor]


1.0b1 (2020-04-15)
------------------

- Use Hostname to get docker-compose name to become more explicit.
  [bsuttor]


1.0a5 (2020-04-03)
------------------

- Add number of zope threads for python 2 instances.
  [bsuttor]


1.0a4 (2020-04-02)
------------------

- Add docker-compose name on label.
  [bsuttor]


1.0a3 (2020-04-02)
------------------

- Reformatting to add attributes to metric.
  [bsuttor]


1.0a2 (2020-04-02)
------------------

- Add type and help text.
  [bsuttor]


1.0a1 (2020-04-01)
------------------

- Initial release.
  [bsuttor]

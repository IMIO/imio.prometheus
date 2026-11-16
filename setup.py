# -*- coding: utf-8 -*-
"""Installer for the imio.prometheus package."""

from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="imio.prometheus",
    version="2.0.0.dev0",
    description="Add some iMio informations on prometheus metrics view",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Addon",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Benoît Suttor",
    author_email="benoit.suttor@imio.be",
    url="https://github.com/IMIO/imio.prometheus",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/imio.prometheus",
        "Source": "https://github.com/IMIO/imio.prometheus",
        "Tracker": "https://github.com/IMIO/imio.prometheus/issues",
        # 'Documentation': 'https://imio.prometheus.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        # -*- Extra requirements: -*-
        "z3c.jbot",
        "plone.api>=1.8.4",
        "plone.restapi",
        "plone.app.dexterity",
        "collective.prometheus",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ]
    },
    entry_points="""
    [console_scripts]
    update_locale = imio.prometheus.locales.update:update_locale
    """,
)

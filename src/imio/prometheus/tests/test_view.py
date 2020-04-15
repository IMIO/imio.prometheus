# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from imio.prometheus.testing import IMIO_PROMETHEUS_INTEGRATION_TESTING  # noqa: E501
from plone import api

import unittest


class TestView(unittest.TestCase):
    """Test that imio.prometheus is properly installed."""

    layer = IMIO_PROMETHEUS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.zope = self.portal.aq_parent

    def test_labels(self):
        """Test if imio.prometheus is installed."""
        view = api.content.get_view("metrics", self.zope, self.zope.REQUEST)
        self.assertEqual(
            {
                "plone_service_name": "local-plone",
                "compose_service": "localhost-instance",
            },
            view.labels(),
        )

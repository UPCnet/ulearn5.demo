# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from ulearn5.demo.testing import ULEARN5_DEMO_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that ulearn5.demo is properly installed."""

    layer = ULEARN5_DEMO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ulearn5.demo is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'ulearn5.demo'))

    def test_browserlayer(self):
        """Test that IUlearn5DemoLayer is registered."""
        from ulearn5.demo.interfaces import (
            IUlearn5DemoLayer)
        from plone.browserlayer import utils
        self.assertIn(IUlearn5DemoLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = ULEARN5_DEMO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(username=TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['ulearn5.demo'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if ulearn5.demo is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'ulearn5.demo'))

    def test_browserlayer_removed(self):
        """Test that IUlearn5DemoLayer is removed."""
        from ulearn5.demo.interfaces import \
            IUlearn5DemoLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IUlearn5DemoLayer,
            utils.registered_layers(),
        )

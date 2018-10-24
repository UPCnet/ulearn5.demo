# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces.controlpanel import ISiteSchema
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.interface import implementer

from ulearn5.core.controlpanel import IUlearnControlPanelSettings
from base5.core.controlpanel.core import IBaseCoreControlPanelSettings

import transaction


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'ulearn5.demo:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('ulearn5.demo_various.txt') is None:
        return

    registry = queryUtility(IRegistry)

    # Define colors of site
    context.settings = registry.forInterface(IUlearnControlPanelSettings)
    context.settings.main_color = u'#003556'
    context.settings.secondary_color = u'#003556'
    context.settings.background_property = u'transparent'
    context.settings.background_color = u'#EDF1F2'
    context.settings.buttons_color_primary = u'#003556'
    context.settings.buttons_color_secondary = u'#003556'
    context.settings.maxui_form_bg = u'#E8E8E8'
    context.settings.alt_gradient_start_color = u'#FFFFFF'
    context.settings.alt_gradient_end_color = u'#FFFFFF'
    context.settings.color_community_closed = u'#08C2B1'
    context.settings.color_community_organizative = u'#C4B408'
    context.settings.color_community_open = u'#556B2F'

    # Define logo for the toolbar
    site_tool = registry.forInterface(ISiteSchema, prefix='plone')
    site_tool.toolbar_logo = u'/++theme++ulearn5.demo/assets/images/toolbarlogo.svg'

    # Define user properties extender
    base_tool = registry.forInterface(IBaseCoreControlPanelSettings)
    base_tool.user_properties_extender = 'user_properties_demo'

    transaction.commit()

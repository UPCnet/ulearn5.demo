# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import implements
from zope.component import getUtility
from zope.publisher.interfaces import IPublishTraverse
from zope.component import getUtilitiesFor
from souper.interfaces import ICatalogFactory
from plone import api

from ulearn5.demo import _
from ulearn5.theme.browser.user_profile import userProfile as userProfileBase


class userProfile(userProfileBase):
    """ Return an user profile ../profile/{username} """
    implements(IPublishTraverse)

    index = ViewPageTemplateFile('views_templates/user_profile.pt')

    def get_user_info_for_display(self):
        user_properties_utility = getUtility(ICatalogFactory, name='user_properties')

        extender_name = api.portal.get_registry_record('base5.core.controlpanel.core.IBaseCoreControlPanelSettings.user_properties_extender')

        portal = api.portal.get()
        current_user = api.user.get_current().id
        roles = api.user.get_roles(username=current_user, obj=portal)
        can_view_properties = True if current_user == self.username or 'WebMaster' in roles or 'Manager' in roles else False

        rendered_properties = []
        if extender_name in [a[0] for a in getUtilitiesFor(ICatalogFactory)]:
            extended_user_properties_utility = getUtility(ICatalogFactory, name=extender_name)
            for prop in extended_user_properties_utility.profile_properties:
                check = self.user_info.getProperty('check_' + prop, '')
                if can_view_properties or check == '' or check:
                    rendered_properties.append(dict(
                        name=_(prop),
                        value=self.user_info.getProperty(prop, '')
                    ))
            return rendered_properties
        else:
            # If it's not extended, then return the simple set of data we know
            # about the user using also the profile_properties field
            for prop in user_properties_utility.profile_properties:
                check = self.user_info.getProperty('check_' + prop, '')
                if can_view_properties or check == '' or check:
                    rendered_properties.append(dict(
                        name=_(prop),
                        value=self.user_info.getProperty(prop, '')
                    ))
            return rendered_properties

    def get_public_user_info_for_display(self):
        extender_name = api.portal.get_registry_record('base5.core.controlpanel.core.IBaseCoreControlPanelSettings.user_properties_extender')

        rendered_properties = []

        if extender_name in [a[0] for a in getUtilitiesFor(ICatalogFactory)]:
            extended_user_properties_utility = getUtility(ICatalogFactory, name=extender_name)
            for prop in extended_user_properties_utility.public_properties:
                rendered_properties.append(dict(
                    name=_(prop),
                    value=self.user_info.getProperty(prop, '')
                ))
        return rendered_properties

    def get_private_user_info_for_display(self):
        extender_name = api.portal.get_registry_record('base5.core.controlpanel.core.IBaseCoreControlPanelSettings.user_properties_extender')

        portal = api.portal.get()
        current_user = api.user.get_current().id
        roles = api.user.get_roles(username=current_user, obj=portal)
        can_view_properties = True if current_user == self.username or 'WebMaster' in roles or 'Manager' in roles else False

        rendered_properties = []

        if extender_name in [a[0] for a in getUtilitiesFor(ICatalogFactory)]:
            extended_user_properties_utility = getUtility(ICatalogFactory, name=extender_name)
            for prop in extended_user_properties_utility.profile_properties:
                if can_view_properties and prop not in extended_user_properties_utility.public_properties:
                    rendered_properties.append(dict(
                        name=_(prop),
                        value=self.user_info.getProperty(prop, '')
                    ))
        return rendered_properties

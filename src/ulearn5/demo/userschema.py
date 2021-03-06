# -*- coding: utf-8 -*-
from plone import api
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.register import BaseRegistrationForm
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.registry.interfaces import IRegistry
from plone.supermodel import model
from plone.z3cform.fieldsets import extensible
from z3c.form import field
from zope import schema
from zope.component import adapts
from zope.component import queryUtility
from zope.interface import Interface

from ulearn5.core.controlpanel import IUlearnControlPanelSettings
from ulearn5.core.hooks import packages_installed
from ulearn5.core.utils import isValidTwitterUsername
from ulearn5.core.utils import stripTwitterUsername
from ulearn5.core.widgets.max_portrait_widget import MaxPortraitFieldWidget
from ulearn5.core.widgets.private_policy_widget import PrivatePolicyFieldWidget
from ulearn5.core.widgets.visibility_widget import VisibilityFieldWidget
from ulearn5.demo import _
from ulearn5.demo.interfaces import IUlearn5DemoLayer

import datetime


class IDemoUserSchema(model.Schema):
    dni = schema.TextLine(
        title=_(u'label_dni', default=u'DNI'),
        description=_(u'help_dni',
                      default=u"Indica el teu DNI."),
        required=False,
    )

    user_type = schema.Bool(
        title=_(u'label_user_type', default=u'Tipus empleat'),
        description=_(u'Si la opcio esta marcada, usuari te nomina'),
        required=False,
        default=False
    )

    check_twitter_username = schema.Bool(
        title=_(u'', default=u''),
        required=False,
        default=True,
    )

    twitter_username = schema.TextLine(
        title=_(u'label_twitter', default=u'Twitter username'),
        description=_(u'help_twitter',
                      default=u'Fill in your Twitter username.'),
        required=False,
        constraint=isValidTwitterUsername
    )

    check_ubicacio = schema.Bool(
        title=_(u'', default=u''),
        required=False,
        default=True,
    )

    ubicacio = schema.TextLine(
        title=_(u'label_ubicacio', default=u'Ubicació'),
        description=_(u'help_ubicacio',
                      default=u'Equip, Àrea / Companyia / Departament'),
        required=False,
    )

    check_telefon = schema.Bool(
        title=_(u'', default=u''),
        required=False,
        default=True,
    )

    telefon = schema.TextLine(
        title=_(u'label_telefon', default=u'Telèfon'),
        description=_(u'help_telefon',
                      default=u'Contacte telefònic'),
        required=False,
    )

    # fieldset_private = schema.TextLine(
        # title=_(u'fieldset_private'),
        # description=_(u'help_fieldset_private'),
        # required=False,
        # readonly=True,
    # )

    private_policy = schema.Bool(
        title=_(u'private_policy'),
        required=True
    )

    time_accepted_private_policy = schema.Text(
        title=_(u'', default=u''),
    )


class DemoUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IDemoUserSchema

    def get_twitter_username(self):
        return self._getProperty('twitter_username')

    def set_twitter_username(self, value):
        if value:
            value = stripTwitterUsername(value)
        return self._setProperty('twitter_username', value)

    twitter_username = property(get_twitter_username, set_twitter_username)

    def get_check_twitter_username(self):
        return self._getProperty('check_twitter_username')

    def set_check_twitter_username(self, value):
        return self._setProperty('check_twitter_username', value is not False)

    check_twitter_username = property(get_check_twitter_username, set_check_twitter_username)

    def get_check_ubicacio(self):
        return self._getProperty('check_ubicacio')

    def set_check_ubicacio(self, value):
        return self._setProperty('check_ubicacio', value is not False)

    check_ubicacio = property(get_check_ubicacio, set_check_ubicacio)

    def get_check_telefon(self):
        return self._getProperty('check_telefon')

    def set_check_telefon(self, value):
        return self._setProperty('check_telefon', value is not False)

    check_telefon = property(get_check_telefon, set_check_telefon)

    def get_private_policy(self):
        return self._getProperty('private_policy')

    def set_private_policy(self, value):
        self._setProperty('time_accepted_private_policy', datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        return self._setProperty('private_policy', value is not False)

    private_policy = property(get_private_policy, set_private_policy)


class DemoUserDataPanelExtender(extensible.FormExtender):
    adapts(Interface, IUlearn5DemoLayer, UserDataPanel)

    def update(self):
        fields = field.Fields(IDemoUserSchema)
        # fields['fieldset_private'].widgetFactory = FieldsetFieldWidget
        # fields = fields.omit('telefon') # Si queremos quitar alguno de los que hemos añadido
        # self.remove('home_page') # Si queremos quitar los de la base (plone.app.users)
        fields['check_twitter_username'].widgetFactory = VisibilityFieldWidget
        fields['check_ubicacio'].widgetFactory = VisibilityFieldWidget
        fields['check_telefon'].widgetFactory = VisibilityFieldWidget

        # Private policy
        fields['private_policy'].widgetFactory = PrivatePolicyFieldWidget
        fields = fields.omit('time_accepted_private_policy')
        registry = queryUtility(IRegistry)
        ulearn_tool = registry.forInterface(IUlearnControlPanelSettings)
        if ulearn_tool.url_private_policy == None or ulearn_tool.url_private_policy == '' or api.user.get_current().getProperty('private_policy', False):
            fields = fields.omit('private_policy')

        installed = packages_installed()
        if 'ulearn5.nomines' in installed:
            roles = api.user.get_roles(username=api.user.get_current().id)
            isAdmin = 'WebMaster' in roles or 'Manager' in roles or 'Gestor Nomines' in roles
            if not isAdmin:
                fields['dni'].field.readonly = True
                fields = fields.omit('user_type')
            else:
                fields['dni'].field.readonly = False
        else:
            fields = fields.omit('user_type')
            fields = fields.omit('dni')

        self.form.fields['portrait'].widgetFactory = MaxPortraitFieldWidget
        self.add(fields)


class DemoRegistrationPanelExtender(extensible.FormExtender):
    adapts(Interface, IUlearn5DemoLayer, BaseRegistrationForm)

    def update(self):
        fields = field.Fields(IDemoUserSchema)
        # fields['fieldset_private'].widgetFactory = FieldsetFieldWidget
        fields['check_twitter_username'].widgetFactory = VisibilityFieldWidget
        fields['check_ubicacio'].widgetFactory = VisibilityFieldWidget
        fields['check_telefon'].widgetFactory = VisibilityFieldWidget
        fields = fields.omit('time_accepted_private_policy')
        fields = fields.omit('private_policy')

        installed = packages_installed()
        if 'ulearn5.nomines' in installed:
            roles = api.user.get_roles(username=api.user.get_current().id)
            isAdmin = 'WebMaster' in roles or 'Manager' in roles or 'Gestor Nomines' in roles
            if not isAdmin:
                fields['dni'].field.readonly = True
                fields = fields.omit('user_type')
            else:
                fields['dni'].field.readonly = False
        else:
            fields = fields.omit('user_type')
            fields = fields.omit('dni')

        self.add(fields)

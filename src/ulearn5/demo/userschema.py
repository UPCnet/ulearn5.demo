# -*- coding: utf-8 -*-
from five import grok
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.register import BaseRegistrationForm
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.directives import form
from plone.supermodel import model
from plone.z3cform.fieldsets import extensible
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from souper.interfaces import ICatalogFactory
from souper.soup import NodeAttributeIndexer
from z3c.form import field
from zope import schema
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implementer

from ulearn5.demo import _
from ulearn5.demo.interfaces import IUlearn5DemoLayer
from ulearn5.core.widgets.max_portrait_widget import MaxPortraitFieldWidget
from ulearn5.core.widgets.visibility_widget import VisibilityFieldWidget


class IDemoUserSchema(model.Schema):
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


class DemoUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IDemoUserSchema

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
        self.form.fields['portrait'].widgetFactory = MaxPortraitFieldWidget
        self.add(fields)


class DemoRegistrationPanelExtender(extensible.FormExtender):
    adapts(Interface, IUlearn5DemoLayer, BaseRegistrationForm)

    def update(self):
        fields = field.Fields(IDemoUserSchema)
        self.add(fields)

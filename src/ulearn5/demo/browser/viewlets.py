# -*- coding: utf-8 -*-
from five import grok
from plone.app.layout.viewlets.interfaces import IPortalHeader
from zope.interface import Interface

from ulearn5.theme.browser.viewlets import viewletHeaderUlearn
from ulearn5.demo.interfaces import IUlearn5DemoLayer

grok.context(Interface)


class viewletHeaderUlearnDemo(viewletHeaderUlearn):
    grok.name('demo.header')
    grok.template('header')
    grok.viewletmanager(IPortalHeader)
    grok.layer(IUlearn5DemoLayer)

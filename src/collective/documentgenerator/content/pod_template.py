# -*- coding: utf-8 -*-

from collective.documentgenerator import _

from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.formwidget.namedfile import NamedFileWidget
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model

from zope.interface import implements


class IPODTemplate(model.Schema):
    """
    PODTemplate dexterity schema.
    """

    form.widget('odt_file', NamedFileWidget)
    odt_file = NamedBlobFile(
        title=_(u'ODT File'),
    )


class PODTemplate(Container):
    """
    PODTemplate dexterity class.
    """

    implements(IPODTemplate)

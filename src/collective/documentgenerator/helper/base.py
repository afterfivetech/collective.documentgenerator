# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter
from zope.interface import implements

from collective.documentgenerator.interfaces import IDisplayProxyObject
from collective.documentgenerator.interfaces import IDocumentGenerationHelper


class DocumentGenerationHelperView(object):
    """
    See IDocumentGenerationHelper.
    """

    implements(IDocumentGenerationHelper)

    def __init__(self, context, request):
        self.real_context = context
        self.request = request
        self.context = self._get_proxy_object(context)
        self.appy_renderer = None

    def _get_proxy_object(self, context):
        proxy_obj = getMultiAdapter((self.real_context, self.display), IDisplayProxyObject)
        return proxy_obj

    def display(self, field_name, context=None, no_value=''):
        """See IDocumentGenerationHelper. To implements."""

    def display_date(self, field_name, context=None, format='%d/%m/%Y %H:%M'):
        """See IDocumentGenerationHelper. To implements."""

    def display_voc(self, field_name, context=None, separator=','):
        """See IDocumentGenerationHelper. To implements."""

    def display_html(self, field_name, context=None):
        """See IDocumentGenerationHelper. To implements."""

    def list_voc(self, field_name, context=None, list_keys=False, list_values=True):
        """See IDocumentGenerationHelper. To implements."""

    def _set_appy_renderer(self, appy_renderer):
        self.appy_renderer = appy_renderer


class DisplayProxyObject(object):
    """
    See IDisplayProxyObject.
    """

    implements(IDisplayProxyObject)

    def __init__(self, context, display_method):
        self.context = context
        self.display = display_method

    def __getattr__(self, attr_name):
        """
        Delegate field attribute access to display() method.
        """
        if self.is_field(attr_name):
            display_value = self.display(field_name=attr_name)
            return display_value

        attr = getattr(self.context, attr_name)
        return attr

    def is_field(self, attr_name):
        """To Override."""

# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Acquisition import aq_parent
from collective.documentgenerator.browser.table import TemplatesTable
from collective.documentgenerator.content.pod_template import IPODTemplate
from collective.documentgenerator.content.style_template import IStyleTemplate
from OFS.interfaces import IOrderedContainer
from plone import api
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.browser.view import DefaultView
from Products.Five import BrowserView
from z3c.form.contentprovider import ContentProviders
from z3c.form.interfaces import IFieldsAndContentProvidersForm
from zope.browserpage import ViewPageTemplateFile
from zope.contentprovider.provider import ContentProviderBase
from zope.interface import implementer

import os


class ResetMd5(BrowserView):
    def __call__(self):
        self.context.style_modification_md5 = self.context.current_md5


class TemplatesListing(BrowserView):

    __table__ = TemplatesTable
    provides = [IPODTemplate.__identifier__, IStyleTemplate.__identifier__]
    depth = None
    local_search = True

    def __init__(self, context, request):
        super(TemplatesListing, self).__init__(context, request)

    def query_dict(self):
        crit = {'object_provides': self.provides}
        if self.local_search:
            container_path = '/'.join(self.context.getPhysicalPath())
            crit['path'] = {'query': container_path}
            if self.depth is not None:
                crit['path']['depth'] = self.depth
        # crit['sort_on'] = ['path', 'getObjPositionInParent']
        # how to sort by parent path
        # crit['sort_on'] = 'path'
        return crit

    def update(self):
        self.table = self.__table__(self.context, self.request)
        self.table.__name__ = u'dg-templates-listing'
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog.searchResults(**self.query_dict())
        res = [(brain.getObject(), os.path.dirname(brain.getPath())) for brain in brains]

        def keys(param):
            """ Goal: order by level of folder, parent folder, position in folder,"""
            (obj, path) = param
            level = len(path.split('/'))
            parent = aq_parent(aq_inner(obj))
            ordered = IOrderedContainer(parent, None)
            if ordered is not None:
                return (level, path, ordered.getObjectPosition(obj.getId()))
            return (level, path, 0)

        # sort by parent path and by position
        self.table.results = [tup[0] for tup in sorted(res, key=keys)]
        self.table.update()

    def __call__(self, local_search=None, search_depth=None):
        """
            search_depth = int value (0)
            local_search = bool value
        """
        if search_depth is not None:
            self.depth = search_depth
        else:
            sd = self.request.get('search_depth', '')
            if sd:
                self.depth = int(sd)
        if local_search is not None:
            self.local_search = local_search
        else:
            self.local_search = 'local_search' in self.request or self.local_search
        self.update()
        return self.index()


class DisplayChildrenPodTemplateProvider(ContentProviderBase):
    template = ViewPageTemplateFile('children_pod_template.pt')

    @property
    def name(self):
        """ """
        return self.__name__

    @property
    def value(self):
        """ """
        return self.render()

    @property
    def label(self):
        return ''

    def get_children(self):
        return self.context.get_children_pod_template()

    def render_child(self, child):
        return '{0} ({1})'.format(child.Title(), child.absolute_url())

    def render(self):
        return self.template()


@implementer(IFieldsAndContentProvidersForm)
class ViewConfigurablePodTemplate(DefaultView):
    contentProviders = ContentProviders()

    contentProviders['children_pod_template'] = DisplayChildrenPodTemplateProvider
    contentProviders['children_pod_template'].position = 4


@implementer(IFieldsAndContentProvidersForm)
class EditConfigurablePodTemplate(DefaultEditForm):
    contentProviders = ContentProviders()

    contentProviders['children_pod_template'] = DisplayChildrenPodTemplateProvider
    contentProviders['children_pod_template'].position = 4

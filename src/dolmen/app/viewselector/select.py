# -*- coding: utf-8 -*-

import grok
import megrok.menu

from zope.schema import TextLine
from zope.interface import Interface
from zope.component import getMultiAdapter, getUtility
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.app.publisher.interfaces.browser import IBrowserMenu

from megrok.z3cform.base import IGrokForm
from dolmen.app.layout import Page, MenuViewlet, master


class IViewSelector(Interface):
    selected_view = TextLine(
        title = u"View",
        default = u"base_view",
        required = True
        )


class SelectedView(Page):
    grok.name("index")
    grok.context(IViewSelector)
    grok.require("dolmen.content.View")

    def render(self):
        rendering = getMultiAdapter(
            (self.context, self.request),
            name = self.context.selected_view
            )
        rendering.update()
        if IGrokForm.providedBy(rendering): rendering.updateForm()
        return rendering.content()


class SelectablePage(Page):
    grok.baseclass()
    megrok.menu.menuitem(u"selectable-views")


class ApplyView(grok.View):
    grok.name('viewselector')
    grok.context(IViewSelector)
    grok.require("dolmen.content.Edit")

    def render(self):
        name = self.request.form.get('name')
        if not name or name == 'index':
            self.flash("This element can't be selected as the default view.")
        else:
            self.context.selected_view = name
            self.flash("%r has been selected as the default view." % name)
        return self.redirect(self.url(self.context))


class SelectableViews(MenuViewlet):
    grok.order(80)
    grok.context(IViewSelector)
    grok.viewletmanager(master.DolmenAboveBody)
    grok.require("dolmen.content.Edit")

    menu_name = u"selectable-views"
    menu_class = u"additional-actions"

    def update(self):
        self.title, actions = self.get_actions(self.context)
        
        if actions:
            url = self.view.url(self.context, name='viewselector')
            selected = self.context.selected_view
            self.actions = [{'url': "%s?name=%s" % (url, action['action']),
                             'title': action['title'],
                             'selected': action['action'] == selected,
                             'css': (action['action'] == selected
                                     and self.entry_class + ' selected'
                                     or self.entry_class)}
                            for action in actions]

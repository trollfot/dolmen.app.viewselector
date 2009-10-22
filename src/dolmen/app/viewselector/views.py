import megrok.menu
import grokcore.component as grok
from dolmen.app.layout import Page


class AlternateView(Page):
    """An alternative view for an object.
    """
    grok.baseclass()
    megrok.menu.menuitem('selectable-views')

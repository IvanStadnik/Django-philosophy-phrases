from django import template
from philosophy_phrases.phrase import get_random_phrase
register = template.Library()


@register.tag(name='phrase_in_popup')
def phrase_in_popup(parser, token):
    return PopupPhraseNode()


class PopupPhraseNode(template.Node):
    def __init__(self):
        self.phrase = get_random_phrase(True)

    def render(self, context):
        """
        If there is no any published phrases in db, it would return
        an empty string, else it would return a phrase in popup
        :param context:
        :return:
        """
        if not self.phrase:
            return ''
        t = context.template.engine.get_template('philosophy_phrases/phrase_popup.html')
        return t.render(template.Context({'phrase': self.phrase}))


@register.assignment_tag
def philosophy_phrase():
    """
    If there is no any published phrases in db, it would return the
    empty strings in variables, else it would return a text of the
    phrase and author of the phrase.
    :param context:
    :return:
    """
    phrase = get_random_phrase()
    if not phrase:
        phrase = {'author': '', 'phrase': ''}
    return phrase

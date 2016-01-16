from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PhilosophyAppName(AppConfig):
    name = 'philosophy_phrases'
    verbose_name = _('Philosophy Phrases')

from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _


class Author(models.Model):
    """
    The model of authors. Biographies data will be in the next version of app.
    """
    name_en = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Name in English'), unique=True)
    name_uk = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Name in Ukrainian'), unique=True)
    name_ru = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Name in Russian'), unique=True)
    biography_en = models.TextField(null=True, blank=True, verbose_name=_('Biography in English'))
    biography_uk = models.TextField(null=True, blank=True, verbose_name=_('Biography in Ukrainian'))
    biography_ru = models.TextField(null=True, blank=True, verbose_name=_('Biography in Russian'))

    def __str__(self):
        try:
            showed_field = PhraseSettings.objects.all()[0]
        except IndexError:
            showed_field = PhraseSettings(status='on', lang_detect='auto')
            showed_field.save()
        lang = get_language()[0:2] if showed_field.lang_detect == 'auto' else showed_field.lang_detect
        if lang == 'uk':
            author = self.name_uk
        elif lang == 'ru':
            author = self.name_ru
        else:
            author = self.name_en
        return author

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Phrases(models.Model):
    """
    The model of phrases.
    """
    phrase_en = models.TextField(null=True, blank=True, verbose_name=_('Phrase in English'), unique=True)
    phrase_uk = models.TextField(null=True, blank=True, verbose_name=_('Phrase in Ukrainian'), unique=True)
    phrase_ru = models.TextField(null=True, blank=True, verbose_name=_('Phrase in Russian'), unique=True)
    author = models.ForeignKey(Author, verbose_name=_('Author'))
    PHRASE_STATUS = (
        ('published', _('Published')),
        ('draft', _('Draft')),
        ('unpublished', _('Unpublished')),
    )
    showed = models.BooleanField(default=False)
    phrase_status = models.CharField(
            max_length=11,
            choices=PHRASE_STATUS,
            default='published',
            verbose_name=_('Status'))
    pub_date = models.DateTimeField('Date published', auto_now_add=True)

    def __str__(self):
        try:
            showed_field = PhraseSettings.objects.all()[0]
        except IndexError:
            showed_field = PhraseSettings(status='on', lang_detect='auto')
            showed_field.save()
        lang = get_language()[0:2] if showed_field.lang_detect == 'auto' else showed_field.lang_detect
        if lang == 'uk':
            phrase = self.phrase_uk
        elif lang == 'ru':
            phrase = self.phrase_ru
        else:
            phrase = self.phrase_en
        return ''.join([phrase[:30], '...'])

    class Meta:
        verbose_name = _('Phrase')
        verbose_name_plural = _('Phrases')

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('philosophy_phrase:philosophy_phrase_view', kwargs={'ph_id': str(self.id)})


class PhraseSettings(models.Model):
    """
    The model of displaying phrases on a page.
    """
    STATUS_CHOICES = (
        ('on', _('Enabled')),
        ('off', _('Disabled'))
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='on', verbose_name=_('Status'))
    LANG_DETECT = (
        ('en', _('English')),
        ('uk', _('Ukrainian')),
        ('ru', _('Russian')),
        ('auto', _('Auto'))
    )
    lang_detect = models.CharField(max_length=10, choices=LANG_DETECT, default='auto',
                                   verbose_name=_('Language of phrases'))
    background_color = models.CharField(max_length=6, default="383636", verbose_name=_('Background color of window'))
    phrase_color = models.CharField(max_length=6, default="bdefac", verbose_name=_('Phrase text color'))
    author_color = models.CharField(max_length=6, default="21ff00", verbose_name=_('Author text color'))

    def __str__(self):
        lang = get_language()[0:2]
        if lang == 'uk':
            title = 'Зміна налаштувань'
        elif lang == 'ru':
            title = 'Изменение настроек'
        else:
            title = 'Change settings'
        return title

    class Meta:
        verbose_name = _('Phrases settings')
        verbose_name_plural = _('Phrases settings')

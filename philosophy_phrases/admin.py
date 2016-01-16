from django.contrib import admin
from .models import Phrases, Author, PhraseSettings
from django.utils.html import format_html
from django.utils.translation import get_language, ugettext_lazy as _
from .forms import PhraseSettingsForm, PhrasesForm, AuthorForm


@admin.register(Phrases)
class PhilosophyAllPhrases(admin.ModelAdmin):
    """
    Settings of displaying and editing phrases in admin panel.
    """
    model = Phrases
    actions_on_bottom = True
    actions_on_top = True
    actions_selection_counter = True
    date_hierarchy = 'pub_date'
    list_display = ('phrase_content', 'phrase_author', 'phrase_status')
    form = PhrasesForm

    def phrase_author(self, obj):
        """
        This function is for displaying author name in English
        and for filtering by "author" field in a table
        :param obj:
        :return:
        """
        author = obj.author.name_en
        return format_html('<span class="pp_author">%s</span>' % author)

    def phrase_author_uk(self, obj):
        """
        This function is for displaying author name in Ukrainian
        and for filtering by "author" field in a table
        :param obj:
        :return:
        """
        author = obj.author.name_uk
        return format_html('<span class="pp_author">%s</span>' % author)

    def phrase_author_ru(self, obj):
        """
        This function is for displaying author name in Russian
        and for filtering by "author" field in a table
        :param obj:
        :return:
        """
        author = obj.author.name_ru
        return format_html('<span class="pp_author">%s</span>' % author)

    def phrase_content(self, obj):
        """
        This function is for displaying phrase in English
        and for filtering by "phrase" field in a table
        :param obj:
        :return:
        """
        phrase = obj.phrase_en
        return format_html(('%s...' % phrase[:100]).upper())

    def phrase_content_uk(self, obj):
        """
        This function is for displaying phrase in Ukrainian
        and for filtering by "phrase" field in a table
        :param obj:
        :return:
        """
        phrase = obj.phrase_uk
        return format_html(('%s...' % phrase[:100]).upper())

    def phrase_content_ru(self, obj):
        """
        This function is for displaying phrase in Russian
        and for filtering by "phrase" field in a table
        :param obj:
        :return:
        """
        phrase = obj.phrase_ru
        return format_html(('%s...' % phrase[:100]).upper())

    phrase_author.admin_order_field = 'author__name_en'
    phrase_author_uk.admin_order_field = 'author__name_uk'
    phrase_author_ru.admin_order_field = 'author__name_ru'
    phrase_content.admin_order_field = 'phrase_en'
    phrase_content_uk.admin_order_field = 'phrase_uk'
    phrase_content_ru.admin_order_field = 'phrase_ru'
    phrase_author.short_description = _('Author')
    phrase_author_uk.short_description = _('Author')
    phrase_author_ru.short_description = _('Author')
    phrase_content.short_description = _('Phrase')
    phrase_content_uk.short_description = _('Phrase')
    phrase_content_ru.short_description = _('Phrase')

    def changelist_view(self, request, extra_context=None):
        """
        This method displays fields in admin panel depending on language
        :param request:
        :param extra_context:
        :return:
        """
        try:
            showed_field = PhraseSettings.objects.all()[0]
        except IndexError:
            showed_field = PhraseSettings()
            showed_field.save()
        lang_detect = get_language()[0:2] if showed_field.lang_detect == 'auto' else showed_field.lang_detect
        if lang_detect == 'ru':
            phrase = (
                _('Phrase'), {
                    'fields': ['phrase_ru'],
                    'classes': ['collapses']
                }
            )
            self.list_display = ('phrase_content_ru', 'phrase_author_ru', 'phrase_status')
        elif lang_detect == 'uk':
            phrase = (
                _('Phrase'), {
                    'fields': ['phrase_uk'],
                    'classes': ['collapses']
                }
            )
            self.list_display = ('phrase_content_uk', 'phrase_author_uk', 'phrase_status')
        elif lang_detect == 'en':
            phrase = (
                _('Phrase'), {
                    'fields': ['phrase_en'],
                    'classes': ['collapses']
                }
            )
            self.list_display = ('phrase_content', 'phrase_author', 'phrase_status')
        else:
            phrase = (
                _('Phrase'), {
                    'fields': ['phrase_en', 'phrase_uk', 'phrase_ru'],
                    'classes': ['collapses']
                }
            )
            self.list_display = ('phrase_content', 'phrase_author', 'phrase_status')
        if showed_field.lang_detect == 'auto':
            phrase = (
                _('Phrase'), {
                    'fields': ['phrase_en', 'phrase_uk', 'phrase_ru'],
                    'classes': ['collapses']
                }
            )
        settings = (
                _('Settings'), {
                    'fields': ['author', 'phrase_status']
                }
            )
        self.fieldsets = [phrase, settings]

        return super(PhilosophyAllPhrases, self).changelist_view(request, extra_context=extra_context)

    list_editable = ['phrase_status']
    list_per_page = 20


@admin.register(Author)
class AllAuthors(admin.ModelAdmin):
    model = Author
    form = AuthorForm

    def changelist_view(self, request, extra_context=None):
        """
        This method displays fields in admin panel depending on language
        :param request:
        :param extra_context:
        :return:
        """
        try:
            showed_field = PhraseSettings.objects.all()[0]
        except IndexError:
            showed_field = PhraseSettings()
            showed_field.save()
        lang_detect = get_language()[0:2] if showed_field.lang_detect == 'auto' else showed_field.lang_detect
        if lang_detect == 'uk':
            self.fields = ('name_uk',)
            author_name = (
                _('Author name'), {'fields': ['name_uk']}
            )
        elif lang_detect == 'ru':
            self.fields = ('name_ru',)
            author_name = (
                _('Author name'), {'fields': ['name_ru']}
            )
        elif lang_detect == 'en':
            self.fields = ('name_en',)
            author_name = (
                _('Author name'), {'fields': ['name_en']}
            )
        if showed_field.lang_detect == 'auto':
            author_name = (
                _('Author name'), {'fields': ['name_en', 'name_uk', 'name_ru']}
            )
        self.fieldsets = [author_name]
        return super(AllAuthors, self).changelist_view(request, extra_context=extra_context)


@admin.register(PhraseSettings)
class PhrasesSettings(admin.ModelAdmin):
    change_form_template = 'admin/philosophy_phrases/phrasesettings/change_form.html'
    form = PhraseSettingsForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        try:
            queryset = PhraseSettings.objects.all()[0]
        except IndexError:
            queryset = PhraseSettings.objects.create()
        return self.change_view(request, str(queryset.id), extra_context)

    class Media:
        css = {
            "all": ("philosophy_phrases/admin_styles/style.css",)
        }
        js = ("philosophy_phrases/js/pp_admin.js", "philosophy_phrases/js/jscolor.min.js")

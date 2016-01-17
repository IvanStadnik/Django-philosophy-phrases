from django import forms
from .models import PhraseSettings, Phrases, Author
from django.utils.translation import ugettext_lazy as _


class PhraseSettingsForm(forms.ModelForm):
    """
    This form is for adding class for color picker in phrases settings
    """
    class Meta:
        model = PhraseSettings
        fields = '__all__'
        widgets = {
            'background_color': forms.TextInput(attrs={'class': 'jscolor'}),
            'phrase_color': forms.TextInput(attrs={'class': 'jscolor'}),
            'author_color': forms.TextInput(attrs={'class': 'jscolor'}),
        }


class PhrasesForm(forms.ModelForm):
    """
    This form checks phrase field depending on language
    """
    class Meta:
        model = Phrases
        fields = '__all__'

    def clean_phrase_uk(self):
        data = self.cleaned_data['phrase_uk']
        lang = PhraseSettings.objects.all()[0].lang_detect
        if not data and (lang == 'uk' or lang == 'auto'):
            raise forms.ValidationError(_('This field is required.'))
        return data

    def clean_phrase_en(self):
        data = self.cleaned_data['phrase_en']
        lang = PhraseSettings.objects.all()[0].lang_detect
        if not data and (lang == 'en' or lang == 'auto'):
            raise forms.ValidationError(_('This field is required.'))
        return data

    def clean_phrase_ru(self):
        data = self.cleaned_data['phrase_ru']
        lang = PhraseSettings.objects.all()[0].lang_detect
        if not data and (lang == 'ru' or lang == 'auto'):
            raise forms.ValidationError(_('This field is required.'))
        return data


class AuthorForm(forms.ModelForm):
    """
    This form checks author name field depending on language
    """
    class Meta:
        model = Author
        fields = '__all__'

    def clean_name_en(self):
        data = self.cleaned_data['name_en']
        lang = PhraseSettings.objects.all()[0].lang_detect
        if not data and (lang == 'en' or lang == 'auto'):
            raise forms.ValidationError(_('This field is required.'))
        return data

    def clean_name_uk(self):
        data = self.cleaned_data['name_uk']
        lang = PhraseSettings.objects.all()[0].lang_detect
        if not data and (lang == 'uk' or lang == 'auto'):
            raise forms.ValidationError(_('This field is required.'))
        return data

    def clean_name_ru(self):
        data = self.cleaned_data['name_ru']
        lang = PhraseSettings.objects.all()[0].lang_detect
        if not data and (lang == 'ru' or lang == 'auto'):
            raise forms.ValidationError(_('This field is required.'))
        return data

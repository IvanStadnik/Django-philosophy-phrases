from philosophy_phrases.models import PhraseSettings, Phrases
from django.utils.translation import get_language


def get_phrase_in_popup():
    """
    This function returns random phrase in pop up window
    :return: phrase in pop up window
    """
    data = get_random_phrase(True)
    if data:
        phrase_content = generate_html_popup(data)
    else:
        return ''
    return phrase_content


def get_phrase_by_id(id):
    """
    This function returns phrase by id
    :param id: phrase id
    :return: phrase
    """
    try:
        settings = PhraseSettings.objects.all()[0]
    except IndexError:
        settings = PhraseSettings()
        settings.save()
    try:
        phrase = Phrases.objects.get(pk=int(id))
    except Phrases.DoesNotExist:
        return ''
    if settings.lang_detect == 'auto':
        lang = get_language()[0:2]
    else:
        lang = settings.lang_detect
    data = {}
    data['bg_color'] = ''.join(['#', settings.background_color])
    data['phrase_color'] = ''.join(['#', settings.phrase_color])
    data['author_color'] = ''.join(['#', settings.author_color])
    if lang == 'uk':
        data['phrase'] = phrase.phrase_uk
        data['author'] = phrase.author.name_uk
    elif lang == 'ru':
        data['phrase'] = phrase.phrase_ru
        data['author'] = phrase.author.name_ru
    else:
        data['phrase'] = phrase.phrase_en
        data['author'] = phrase.author.name_en
    return data


def get_random_phrase(pop_up=False):
    """
    This function returns random phrase depending of admin settings and site language.
    If there is no settings data in db, it would create them by default
    :param pop_up:
    :return: phrase with html or without
    """
    try:                                            # if settings are not exist we must create them
        settings = PhraseSettings.objects.all()[0]
    except IndexError:
        settings = PhraseSettings()
        settings.save()
    if settings.status == 'off':                    # if status of settings disabled we must return empty string
        return False
    if settings.lang_detect == 'auto':
        lang = get_language()[0:2]
    else:
        lang = settings.lang_detect
    try:
        if lang == 'uk':
            phrase = Phrases.objects.filter(showed=False,
                                            phrase_status='published',
                                            phrase_uk__isnull=False).order_by('?')[0]
        elif lang == 'ru':
            phrase = Phrases.objects.filter(showed=False,
                                            phrase_status='published',
                                            phrase_ru__isnull=False).order_by('?')[0]
        elif lang == 'en':
            phrase = Phrases.objects.filter(showed=False,
                                            phrase_status='published',
                                            phrase_en__isnull=False).order_by('?')[0]
        phrase.showed = True
        phrase.save()
    except IndexError:          # if all phrases were shown, we must update all as 'not shown'
        Phrases.objects.filter(showed=True).update(showed=False)
        try:
            if lang == 'uk':
                phrase = Phrases.objects.filter(showed=False,
                                                phrase_status='published',
                                                phrase_uk__isnull=False).order_by('?')[0]
            elif lang == 'ru':
                phrase = Phrases.objects.filter(showed=False,
                                                phrase_status='published',
                                                phrase_ru__isnull=False).order_by('?')[0]
            elif lang == 'en':
                phrase = Phrases.objects.filter(showed=False,
                                                phrase_status='published',
                                                phrase_en__isnull=False).order_by('?')[0]
            phrase.showed = True
            phrase.save()
        except IndexError:      # this means that we have no published phrases in db
            return False
    data = {}
    if pop_up:
        data['bg_color'] = ''.join(['#', settings.background_color])
        data['phrase_color'] = ''.join(['#', settings.phrase_color])
        data['author_color'] = ''.join(['#', settings.author_color])
    if lang == 'uk':
        data['phrase'] = phrase.phrase_uk
        data['author'] = phrase.author.name_uk
    elif lang == 'ru':
        data['phrase'] = phrase.phrase_ru
        data['author'] = phrase.author.name_ru
    else:
        data['phrase'] = phrase.phrase_en
        data['author'] = phrase.author.name_en
    return data


def generate_html_popup(data):
    """
    This function returns html code for pop up window.
    But you must include jQuery library into a template yourself.
    :param data: params for phrase displaying
    :return: phrase with html
    """
    content = '<div id="pp_fixed_block" style="position: fixed;bottom: 5px;right: 5px;' \
              'border-radius: 3px;padding: 20px 20px 30px 10px;font-style: italic;max-width: 650px;' \
              'opacity: 0;box-shadow: 0 0 9px rgba(0, 0, 0, 1);display: block;min-width: 300px;' \
              'z-index: 1000;min-width: 350px;background-color: %s">' \
              '<div id="dialog_close" style="position: absolute;top: 5px;right: 5px;width: 20px;' \
              'height: 20px;cursor: pointer;color:%s">&#10006;</div>' \
              '<div id="pp_fixed_phrase" style="color: %s">' \
              '%s<div id="pp_fixed_author" style="position: absolute;bottom: 5px;right: 25px;color: %s">' \
              '%s</div></div>' \
              '</div><script>!function(){var t={easing:{linear:function(t){return t},quadratic:function(t){' \
              'return Math.pow(t,2)},swing:function(t){return.5-Math.cos(t*Math.PI)/2},circ:function(t){' \
              'return 1-Math.sin(Math.acos(t))},back:function(t,e){return Math.pow(t,2)*((e+1)*t-e)},' \
              'bounce:function(t){for(var e=0,n=1;1;e+=n,n/=2)if(t>=(7-4*e)/11)return-Math.pow((11-6*e-11*t)/4,2)' \
              '+Math.pow(n,2)},elastic:function(t,e){return Math.pow(2,10*(t-1))*Math.cos(20*Math.PI*e/3*t)}},' \
              'animate:function(t){var e=new Date,n=setInterval(function(){var o=new Date-e,a=o/t.duration;a>1&&(a=1)' \
              ',t.progress=a;var i=t.delta(a);t.step(i),1==a&&(clearInterval(n),t.complete())},t.delay||10)},' \
              'fadeOut:function(e,n){var o=1;this.animate({duration:n.duration,delta:function(e){' \
              'return e=this.progress,t.easing.swing(e)},complete:n.complete,step:function(t){' \
              'e.style.opacity=o-t}})},fadeIn:function(e,n){var o=0;this.animate({' \
              'duration:n.duration,delta:function(e){return e=this.progress,t.easing.swing(e)}' \
              ',complete:n.complete,step:function(t){e.style.opacity=o+t}})}};window.FX=t}(),setTimeout(function(){' \
              'FX.fadeIn(document.getElementById("pp_fixed_block"),{duration:800,complete:function(){' \
              '}})},2e3),document.getElementById("dialog_close").addEventListener("click",function(){' \
              'FX.fadeOut(document.getElementById("pp_fixed_block"),{duration:800,complete:function(){' \
              'document.getElementById("pp_fixed_block").remove()}})},!1);' \
              '</script>' % (data['bg_color'], data['phrase_color'],
                            data['phrase_color'], data['phrase'],
                            data['author_color'], data['author'])
    return content


def get_phrase():
    """
    This function returns simply a random phrase and its author.
    :return:  data['phrase'], data['author']
    """
    data = get_random_phrase()
    if not data:
        return ''
    return data

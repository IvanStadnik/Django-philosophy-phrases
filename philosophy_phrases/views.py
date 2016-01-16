from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods


def philosophy_phrase_view(request, ph_id):
    """
    This function shows phrase for admin when clicking on 'view on site'.
    :param request:
    :param ph_id:
    :return:
    """
    from philosophy_phrases.phrase import get_phrase_by_id
    data = get_phrase_by_id(ph_id)
    if not data:
        raise Http404('Phrase does not exist.')
    return render(request, 'philosophy_phrases/details.html', {'phrase': data})


@require_http_methods(['POST'])
def import_default_data(request):
    """
    This function is for post request from admin to import default phrases.
    :param request:
    :return:
    """
    data = dict()
    from .action_data import import_phrases
    result = import_phrases()
    data['result'] = result
    data['class'] = 'error'
    if result:
        data['message'] = _('Phrases imported successfully.')
        data['class'] = 'success'
    else:
        data['message'] = _('Import of phrases failed.')
    return JsonResponse(data)

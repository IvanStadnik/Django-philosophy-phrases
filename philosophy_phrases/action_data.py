import os
from .models import Phrases, Author
from django.db.models import Q


def import_phrases():
    """
    This function imports default data from a file in the root
    directory of app.
    :return:
    """
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'phrases')
    phrase, author = {}, {}
    result = True
    try:
        for x in open(file_path):
            if x[0] == 'A':
                if x[:3] == 'ARU':
                    author['author_ru'] = x.rstrip()[4:]
                elif x[:3] == 'AUA':
                    author['author_uk'] = x.rstrip()[4:]
                elif x[:3] == 'AEN':
                    author['author_en'] = x.rstrip()[4:]
            elif x[0] == 'P':
                if len(author) == 3:
                    phrases_author = insert_author(author.copy())
                    author.clear()
                if x[:3] == 'PRU':
                    phrase['phrase_ru'] = x.rstrip()[4:]
                elif x[:3] == 'PUA':
                    phrase['phrase_uk'] = x.rstrip()[4:]
                elif x[:3] == 'PEN':
                    phrase['phrase_en'] = x.rstrip()[4:]
            if len(phrase) == 3:
                insert_phrase(phrase.copy(), phrases_author)
                phrase.clear()
    except:
        result = False
    del author, phrase
    return result


def insert_author(author):
    """
    This function inserts author into db.
    If the author exists this function will update it.
    :param author:
    :return:
    """
    try:
        philosopher = Author.objects.get(Q(name_ru__exact=author['author_ru']) | Q(name_uk__exact=author[
            'author_uk']) | Q(name_en__exact=author['author_en']))
        philosopher.name_ru = author['author_ru']
        philosopher.name_uk = author['author_uk']
        philosopher.name_en = author['author_en']
    except Author.DoesNotExist:
        philosopher = Author(name_ru=author['author_ru'], name_uk=author['author_uk'], name_en=author['author_en'])
    philosopher.save()
    return philosopher


def insert_phrase(phrase, phrases_author):
    """
    This function inserts default phrase into the db.
    If the phrase exists this function will update it.
    :param phrase:
    :param phrases_author:
    :return:
    """
    try:
        phrase_save = Phrases.objects.get(Q(phrase_en__exact=phrase['phrase_en']) | Q(phrase_uk__exact=phrase[
            'phrase_uk']) | Q(phrase_ru__exact=phrase['phrase_ru']))
        phrase_save.phrase_en = phrase['phrase_en']
        phrase_save.phrase_uk = phrase['phrase_uk']
        phrase_save.phrase_ru = phrase['phrase_ru']
        phrase_save.author = phrases_author
    except Phrases.DoesNotExist:
        phrase_save = Phrases(
            phrase_en=phrase['phrase_en'],
            phrase_uk=phrase['phrase_uk'],
            phrase_ru=phrase['phrase_ru'],
            phrase_status='published',
            author=phrases_author
        )
    phrase_save.save()


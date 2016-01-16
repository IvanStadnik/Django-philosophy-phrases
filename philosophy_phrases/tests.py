from django.test import TestCase
from .models import PhraseSettings, Phrases, Author
from .action_data import import_phrases
from .phrase import get_phrase_by_id, get_phrase_in_popup, get_random_phrase, get_phrase


class PhrasesImportTest(TestCase):
    def test_import_default_phrases(self):
        """
        Import phrases must return True
        :return:
        """
        result = import_phrases()
        self.assertEqual(result, True)

    def test_second_import_phrases(self):
        """
        Function import_phrases should not make
        copies of phrases
        :return:
        """
        import_phrases()
        count_first = Phrases.objects.all().count()
        import_phrases()
        count_second = Phrases.objects.all().count()
        self.assertEqual(count_first, count_second)

    def test_second_import_phrases_after_delete_an_object(self):
        """
        Function import_phrases should recover deleted phrases
        :return:
        """
        import_phrases()
        count_first = Phrases.objects.all().count()
        Phrases.objects.all()[0].delete()
        import_phrases()
        count_second = Phrases.objects.all().count()
        self.assertEqual(count_first, count_second)

    def test_second_import_authors(self):
        """
        Function import_phrases should not make
        copies of authors
        :return:
        """
        import_phrases()
        count_first = Author.objects.all().count()
        import_phrases()
        count_second = Author.objects.all().count()
        self.assertEqual(count_first, count_second)

    def test_second_import_authors_after_delete_an_object(self):
        """
        Function import_phrases should recover deleted authors
        :return:
        """
        import_phrases()
        count_first = Author.objects.all().count()
        Author.objects.all()[0].delete()
        import_phrases()
        count_second = Author.objects.all().count()
        self.assertEqual(count_first, count_second)


class PhrasesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.settings = PhraseSettings.objects.create()
        cls.author = Author.objects.create(name_en='Name in English',
                                           name_uk='Name in Ukrainian',
                                           name_ru='Name in Russian')
        cls.phrase_first = Phrases.objects.create(phrase_en='First phrase in English',
                                                  phrase_uk='First phrase in Ukrainian',
                                                  phrase_ru='First phrase in Russian',
                                                  author=cls.author)
        cls.phrase_second = Phrases.objects.create(phrase_en='Second phrase in English',
                                                   phrase_uk='Second phrase in Ukrainian',
                                                   phrase_ru='Second phrase in Russian',
                                                   author=cls.author)
        cls.phrase_third = Phrases.objects.create(phrase_en='Third phrase in English',
                                                  phrase_uk='Third phrase in Ukrainian',
                                                  phrase_ru='Third phrase in Russian',
                                                  author=cls.author)
# from .phrase import get_phrase_by_id, get_phrase_in_popup, get_random_phrase, get_phrase

    def test_get_phrase_default_settings(self):
        """
        Function get_random_phrase should return published phrase
        and its author by default settings
        :return:
        """
        phrase = get_random_phrase()
        result = len(phrase)
        self.assertEqual(result, 2)

    def test_get_phrase_disabled_settings(self):
        """
        Function get_random_phrase should return False
        if phrases are disabled in 'phrases settings'
        :return:
        """
        self.settings.status = 'off'
        self.settings.save()
        result = get_random_phrase()
        self.assertEqual(result, False)

    def test_get_phrase_disabled(self):
        """
        Function get_random_phrase should return False
        if there is no published phrases in db
        :return:
        """
        Phrases.objects.all().update(phrase_status='draft')
        self.phrase_first.phrase_status = 'unpublished'
        self.phrase_first.save()
        result = get_random_phrase()
        self.assertEqual(result, False)

    def test_get_random_phrase_in_popup(self):
        """
        function get_random_phrase(pop_up=True), should return
        dictionary consists 5 elements.
        :return:
        """
        result = get_random_phrase(pop_up=True)
        self.assertEqual(len(result), 5)

    def test_get_phrase_by_id_if_not_exist(self):
        """
        If phrase does not exist, function get_phrase_by_id
        should return empty string
        :return:
        """
        phrase = get_phrase_by_id(1000)
        self.assertEqual(phrase, '')

    def test_get_phrase(self):
        """
        Function get_phrase() should return a dictionary consists
        2 elements
        :return:
        """
        result = get_phrase()
        self.assertEqual(len(result), 2)

    def test_get_phrase_no_phrases(self):
        """
        Function get_phrase() should return an empty string
        if there is no published phrases in the db
        :return:
        """
        Phrases.objects.all().update(phrase_status='draft')
        result = get_phrase()
        self.assertEqual(result, '')

    def test_get_phrase_in_popup(self):
        """
        Function get_phrase_in_popup() should return an empty
        string if there is no published phrases in the db
        :return:
        """
        Phrases.objects.all().update(phrase_status='draft')
        result = get_phrase_in_popup()
        self.assertEqual(result, '')

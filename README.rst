=====
Philosophy phrases
=====

Django-philosophy-phrases is an application for django project on three languages ( English, Ukrainian and Russian ). Using it you can add any philosophy phrases on your website. It has default phrases which you can simply import in admin part. And then you have to add variable to your view and insert it into your template. You can add just phrase and its author, or popup. In phrase settings in your admin part ( you'll need the Admin app enabled ) you can choose background color of popup, color of phrases text and  color of authors text. Also you have to choose language of phrases. If you choose 'auto', app will be detecting language using django. 

Quick start
-----------

1. Add "philosophy_phrases" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = (
        ...
        'philosophy_phrases',
    )

2. Include the polls URLconf in your project urls.py like this:
    
    from django.conf.urls import include, url
    ...

    url(r'^philosophy', include('philosophy_phrases.urls', namespace='philosophy_phrase')),

3. Run 'python manage.py migrate' to create the philosophy_phrases models.

4. For adding phrases into your template you can use one of the template tags:

	a. {% phrase_in_popup %} - it will return a string with html.

		...
		<body>
		...
		{% load philosophy_extras %}
		{% phrase_in_popup %} 
		</body>

	b. {% philosophy_phrase as phrase %}  - it would return adictionary with two variables:

		...
		{% load philosophy_extras %}
		{% philosophy_phrase as phrase %} 
		    <p> {{ phrase.phrase }}</p>      # text of the phrase
		    <p>{{ phrase.author }}</p>       # author of the phrase
		...

Or you can use one of the functions in your view like this:

	a. function get_phrase() will return a dictionary consist phrase and its author.

		from philosophy_phrases.phrase import get_phrase
		    ...

		    def Your_view_name(request):
			phrase = get_phrase()
			...

		    and then insert it into your template:

		    {{ phrase.phrase }}
		    {{ phrase.author }}
	    
	b. function get_phrase_in_popup() will return html code for popup.

		from philosophy_phrases.phrase import get_phrase_in_popup()
		...

		def Your_view_name(request):
		phrase = get_phrase_in_popup()
		...

		and then insert it into your template (you have to use filter 'safe' for correct displaying html and js in your template):

		{{ phrase|safe }}

5. If there is no any phrase in your db, functions get_phrase_in_popup() and get_phrase() will return an empty string.

6. Start the development server and visit http://127.0.0.1:8000/admin/
   to create your owne phrase or import phrases by default (you'll need the Admin app enabled).

7. For importing phrases visit http://127.0.0.1:8000/admin/philosophy_phrases/phrasesettings/, and click on 'Import default phrases'. If you click on it second time it will not create copy of phrases or authors, but will add phrases by default if there is no any of them.

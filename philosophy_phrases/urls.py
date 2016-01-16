from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^import_default_data/', views.import_default_data, name='import_default_data'),
    url(r'^philosophy_phrase_view/(?P<ph_id>[0-9]+)/$', views.philosophy_phrase_view, name='philosophy_phrase_view'),
]
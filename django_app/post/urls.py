from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^post-create/$', views.post_create, name='create'),
]

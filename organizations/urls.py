from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_organizations, name='organizations'),
    url(r'^(?P<organization_name>[a-zA-Z0-9]+-?[a-zA-Z0-9_-]+)$', views.get_repos, name='repos')
]
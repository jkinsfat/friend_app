from django.conf.urls import url
from . import views

app_name = 'friends'
urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^add', views.add, name="add"),
    url(r'^user/(?P<user_id>\w)', views.user, name="user"),
    url(r'^remove/(?P<friend_id>\w)', views.remove, name="remove")
]

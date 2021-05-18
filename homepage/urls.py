from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('login', views.login, name='login'),
    path('logout',views.logout,name='logout'),
    path('feed', views.feed, name='feed'),
    path('specific/<int:category>', views.specific, name='specific'),
    path('answer', views.answer, name='answer'),
    path('answerpage/<int:id>', views.answerpage, name='answerpage'),
    path('ask', views.ask, name='ask'),
    path('question', views.question, name='question'),
    url(r'^like/$', views.like, name='like'),
]
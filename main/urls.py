from . import views
from  django.urls import path
app_name = 'main'

urlpatterns = [
    path("",views.homepage,name = 'homepage'),
    path("login/", views.login_request, name='login'),
    path("register/", views.register ,name='register'),
    path("game/",views.game, name='game'),
    path("logout/",views.logout_request, name = 'logout')
]
from . import views
from  django.urls import path
app_name = 'main'

urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("creator/", views.gameroom_creator, name='creator'),
    path("game/<str:gameroom_id>/", views.game, name='game'),
    path("gameroom/", views.gameroom, name='gameroom'),
    path("login/", views.login_request, name='login'),
    path("logout/", views.logout_request, name='logout'),
    path("profile/<str:user_id>/", views.profile, name='profile'),
    path("register/", views.register, name='register')
]
from django.urls import path
from authentication import views

urlpatterns = [
    path('signin/', views.user_login, name='signin'),
    # path('signin/', views.signin,name='signin'),

    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]
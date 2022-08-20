from django.urls import path
from . import views
from django.contrib.auth import views as authviews

urlpatterns = [
    path('',views.topics,name='topics'),
    path('<int:pk>/',views.topic,name='topic'),
    path('<int:pk>/update/',views.update_topic,name='update-topic'),
    path('<int:pk>/delete/',views.delete_topic,name='delete-topic'),
    path('delete_option/<int:pk>/',views.delete_choice,name='delete-choice'),
    path('update_option/<int:pk>/',views.update_choice,name='update-choice'),
    path('add_choice/<int:pk>/',views.add_choice,name='add-choice'),
    path('add_topic/',views.add_topic,name='add-topic'),

    #user
    path('user/login/',views.login_user,name='login'),
    path('user/logout/',authviews.LogoutView.as_view(),name='logout'),
    path('user/signup/',views.signup,name='signup'),
    path('user/delete/',views.delete_account,name='delete-account'),
    path('user/privacy_settings/',views.privacy_settings,name='privacy-settings'),
    #path('user/change_password/',views.change_password,name='change-password'),
]

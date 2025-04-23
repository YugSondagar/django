from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.loginPage,name="login"),
    path("logout/",views.logoutUser,name="logout"),
    path("register/",views.registerUser,name="register"),
    path('',views.home,name="Home"),
    path('room/<str:pk>/',views.room,name="Room"),
    path('profile<str:pk>/',views.userProfile,name="user-profile"),
    path('create-room/',views.create_room,name="Create-Room"),
    path('update-room/<str:pk>/',views.update_room,name="Update-Room"),
    path('delete-room/<str:pk>/',views.delete_room,name="Delete-Room"),
    path('edit-message/<str:pk>/',views.Edit_message,name="edit-message"),
    path('delete-message/<str:pk>/',views.delete_message,name="delete-message"),
    path('update-user/',views.updateUser,name="update-user"),
    path('topics/',views.topicsPage,name="topics"),
    path('activity/',views.activitiesPage,name="activity"),
    
]


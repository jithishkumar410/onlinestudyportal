"""stdpor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboard import views
from dashboard import views as dash_views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('notes',views.notes,name='notes'),
    path("dele/<int:pk>",views.dele,name='dele'),
    path('notesview/<int:pk>',views.NotesView.as_view(),name='notesview'),
    path('youtube',views.youtube,name='youtube'),
    path('todo',views.todo,name='todo'),
    path('update/<int:pk>',views.update,name='update'),
    path('deleteT/<int:pk>',views.deleteT,name='deleteT'),
    path("books",views.books,name="books"),
    path('chatbot',views.chatbot,name='chatbot'),
    path("diction",views.diction,name="diction"),
    path("wiki",views.wiki,name="wiki"),
    path('register',dash_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='dashboard/login.html'),name='login'),
    path('pro',dash_views.pro,name='profile'),
    path('logout',auth_views.LogoutView.as_view(template_name='dashboard/logout.html'),name='logout'),

]

from django.urls import path
from todoapp import views
urlpatterns =[
    path('',views.home),
    path('dashboard',views.dashboard),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('register',views.user_register),
    path('edit/<rid>',views.edit),
    path('delete/<rid>',views.delete),
    path('catfilter/<cv>',views.catfilter),
    path('statfilter/<cv>',views.statfilter),
    path('datefilter',views.datefilter),
    path('datesort/<ds>',views.datesort),
]
from django.urls import path
from . import views

urlpatterns=[
    path('',views.homePage, name = "user-home"),
    path('search',views.search_results, name = "search-results"),
]
# bkapp/urls.py
from django.urls import path

from .views.strategiesView import list_strategies

urlpatterns = [

    path('strategies/', list_strategies),
]

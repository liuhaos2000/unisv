# bkapp/urls.py
from django.urls import path

from .views.strategiesView import list_strategies
from .views.strategies2View import list_strategies2

urlpatterns = [

    path('strategies/', list_strategies),
    path('strategies2/', list_strategies2),
]

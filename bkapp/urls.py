# bkapp/urls.py
from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from .views.strategiesView import list_strategies
from .views.strategies2View import list_strategies2


urlpatterns = [

    path('strategies/', list_strategies),
    path('strategies2/', list_strategies2),

    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]

# bkapp/urls.py
from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from .views.strategiesView import list_strategies
from .views.strategies2View import list_strategies2
from .views.userView import get_user_first_stock


urlpatterns = [

    path('sk/strategies/', list_strategies),


    #find
    path('find/strategies2/', list_strategies2),
    path('find/stock/', list_strategies2),

    #mypage
    path('my/firststock/', get_user_first_stock),

    #user login
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]

from django.urls import path
from . import views

app_name = 'betting'

urlpatterns = [
    path('', views.match_list, name='match_list'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
    path('bet-slip/', views.bet_slip, name='bet_slip'),
    path('bet-history/', views.bet_history, name='bet_history'),
]

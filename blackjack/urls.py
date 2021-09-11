from django.urls import path

from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('input_money/', input_money_view, name='input_money'),
    path('input_money/input_bet/', input_bet_view, name='input_bet'),
    path('game/', base_view, name='base_view'),
    path('game/hit/', hit, name='hit'),
    path('game/end_of_round/', end_of_round, name='end_of_round')
]

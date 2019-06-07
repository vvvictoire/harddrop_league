"""Manage the app urls"""

from django.urls import path
from . import views

app_name = 'read_only_site'
urlpatterns = [
    path('', views.index, name='index'),
    # Player stats (ex: /player/trucy)
    path('player/<str:player_name>/', views.player, name='player'),
    # Match view (ex: /match/1337)
    path('match/<int:match_pk>', views.match, name='match'),
    # Leaderboard
    path('leaderboard', views.leaderboard, name='leaderboard'),
    # Latest matches
    path('latest_matches', views.latest_matches, name='latest_matches')
]

"""Manage the read_only_site views"""

from django.shortcuts import get_object_or_404, render
from .models import Player, Match

# Create your views here.
def index(request):
    """Home page"""
    return render(request, 'read_only_site/index.html')

def player(request, player_name):
    """Stats for a single player"""
    player_to_get = get_object_or_404(Player, jstris_handle=player_name)
    context = {'player': player_to_get}
    return render(request, 'read_only_site/player.html', context)

def match(request, match_pk):
    """Stats for a single match"""
    match_to_get = get_object_or_404(Match, pk=match_pk)
    context = {'match': match_to_get}
    return render(request, 'read_only_site/match.html', context)

def leaderboard(request):
    """Leaderboard, based on trueskill_mu"""
    players = Player.objects.order_by('-trueskill_mu')
    context = {'players': players}
    return render(request, 'read_only_site/leaderboard.html', context)

def latest_matches(request):
    """All matches, from latest to oldest"""
    matches = Match.objects.order_by('-played_on')
    context = {'matches': matches}
    return render(request, 'read_only_site/latest_matches.html', context)
